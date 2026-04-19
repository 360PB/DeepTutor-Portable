"""Vision Solver Agent - Main orchestrator for image analysis pipeline.

Implements a four-stage analysis workflow:
1. BBox - Visual element detection
2. Analysis - Geometric semantic analysis
3. GGBScript - Generate GeoGebra commands
4. Reflection - Validate and fix commands
"""

import json
from pathlib import Path
import re
import traceback
from typing import Any, AsyncGenerator

from deeptutor.agents.base_agent import BaseAgent
from deeptutor.agents.vision_solver.models import (
    AnalysisOutput,
    BBoxOutput,
    GGBCommand,
    GGBScriptOutput,
    ImageAnalysisState,
    ReflectionOutput,
    create_empty_analysis_output,
    create_empty_bbox_output,
    create_empty_ggbscript_output,
    create_empty_reflection_output,
)


class VisionSolverAgent(BaseAgent):
    """Agent for analyzing math problem images and generating GeoGebra visualizations."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        vision_model: str | None = None,
        language: str = "zh",
        **kwargs,
    ):
        """Initialize the Vision Solver Agent.

        Args:
            api_key: API key for LLM provider
            base_url: Base URL for LLM API
            model: Model name for text generation
            vision_model: Model name for vision tasks (defaults to model)
            language: Language setting ('zh' or 'en')
            **kwargs: Additional arguments passed to BaseAgent
        """
        super().__init__(
            module_name="vision_solver",
            agent_name="vision_solver_agent",
            api_key=api_key,
            base_url=base_url,
            model=model,
            language=language,
            **kwargs,
        )

        self.vision_model = vision_model or model
        self._load_prompts()

    def _load_prompts(self):
        """Load prompt templates from files."""
        prompts_dir = Path(__file__).parent / "prompts"

        self.prompt_templates = {}
        for prompt_name in ["bbox", "analysis", "ggbscript", "reflection", "tutor"]:
            prompt_file = prompts_dir / f"{prompt_name}.md"
            if prompt_file.exists():
                self.prompt_templates[prompt_name] = prompt_file.read_text(encoding="utf-8")
            else:
                self.logger.warning(f"Prompt file not found: {prompt_file}")
                self.prompt_templates[prompt_name] = ""

    def _render_prompt(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a prompt template with context variables.

        Args:
            template_name: Name of the template (bbox, analysis, etc.)
            context: Dictionary of variables to substitute

        Returns:
            Rendered prompt string
        """
        template = self.prompt_templates.get(template_name, "")

        # Simple Jinja2-like variable substitution
        for key, value in context.items():
            placeholder = "{{ " + key + " }}"
            if isinstance(value, (dict, list)):
                template = template.replace(
                    placeholder, json.dumps(value, ensure_ascii=False, indent=2)
                )
            else:
                template = template.replace(placeholder, str(value))

        return template

    def _extract_json_from_response(self, response: str) -> dict:
        """Extract JSON from LLM response, handling markdown code blocks.

        Args:
            response: Raw LLM response text

        Returns:
            Parsed JSON dictionary

        Raises:
            json.JSONDecodeError: If JSON parsing fails
        """
        # Try to extract from markdown code block
        json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        matches = re.findall(json_pattern, response)

        if matches:
            json_str = matches[0]
        else:
            json_str = response

        # Remove JSON comments
        json_str = re.sub(r"//.*?$", "", json_str, flags=re.MULTILINE)
        json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try fixing common issues
            json_str = re.sub(r",\s*([}\]])", r"\1", json_str)  # Remove trailing commas
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                self.logger.error(f"JSON parsing failed, response: {response[:500]}...")
                raise

    async def _call_vision_llm(
        self,
        prompt: str,
        image_base64: str,
        temperature: float = 0.3,
    ) -> str:
        """Call vision LLM with image input.

        Args:
            prompt: Text prompt
            image_base64: Base64 encoded image (data:image/...;base64,...)
            temperature: Temperature for generation

        Returns:
            LLM response text
        """
        # Build multimodal message
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64}},
                ],
            }
        ]

        _chunks: list[str] = []
        async for _c in self.stream_llm(
            user_prompt="",
            system_prompt="",
            messages=messages,
            temperature=temperature,
            model=self.vision_model or self.get_model(),
            verbose=False,
        ):
            _chunks.append(_c)
        response = "".join(_chunks)

        return response

    # ==================== Stage Processors ====================

    async def _process_bbox(self, state: ImageAnalysisState) -> BBoxOutput:
        """BBox stage: Extract pixel coordinates of geometric elements.

        Args:
            state: Current pipeline state

        Returns:
            BBox output with element coordinates
        """
        self.logger.info(f"BBox stage - session: {state.session_id}")

        try:
            prompt = self._render_prompt(
                "bbox",
                {"question_text": state.question_text},
            )

            response = await self._call_vision_llm(
                prompt=prompt,
                image_base64=state.image_base64,
                temperature=0.3,
            )

            bbox_output = self._extract_json_from_response(response)
            elements_count = len(bbox_output.get("elements", []))
            self.logger.info(f"BBox completed - elements: {elements_count}")

            return bbox_output

        except Exception as e:
            self.logger.error(f"BBox stage error: {e}")
            self.logger.error(traceback.format_exc())
            return create_empty_bbox_output()

    async def _process_analysis(self, state: ImageAnalysisState) -> tuple[AnalysisOutput, bool]:
        """Analysis stage: Extract geometric semantics.

        Args:
            state: Current pipeline state

        Returns:
            Tuple of (analysis output, image_is_reference flag)
        """
        self.logger.info(f"Analysis stage - session: {state.session_id}")

        try:
            prompt = self._render_prompt(
                "analysis",
                {
                    "question_text": state.question_text,
                    "bbox_output_json": state.bbox_output,
                },
            )

            response = await self._call_vision_llm(
                prompt=prompt,
                image_base64=state.image_base64,
                temperature=0.3,
            )

            analysis_output = self._extract_json_from_response(response)
            image_is_reference = analysis_output.get("image_reference_detected", False)

            if image_is_reference:
                keywords = analysis_output.get("image_reference_keywords", [])
                self.logger.info(f"Image reference detected - keywords: {keywords}")

            return analysis_output, image_is_reference

        except Exception as e:
            self.logger.error(f"Analysis stage error: {e}")
            self.logger.error(traceback.format_exc())
            return create_empty_analysis_output(), False

    async def _process_ggbscript(self, state: ImageAnalysisState) -> GGBScriptOutput:
        """GGBScript stage: Generate GeoGebra commands.

        Args:
            state: Current pipeline state

        Returns:
            GGBScript output with command list
        """
        self.logger.info(f"GGBScript stage - session: {state.session_id}")

        try:
            prompt = self._render_prompt(
                "ggbscript",
                {
                    "question_text": state.question_text,
                    "bbox_output_json": state.bbox_output,
                    "analysis_output_json": state.analysis_output,
                },
            )

            response = await self._call_vision_llm(
                prompt=prompt,
                image_base64=state.image_base64,
                temperature=0.3,
            )

            ggbscript_output = self._extract_json_from_response(response)
            commands_count = len(ggbscript_output.get("commands", []))
            self.logger.info(f"GGBScript completed - commands: {commands_count}")

            return ggbscript_output

        except Exception as e:
            self.logger.error(f"GGBScript stage error: {e}")
            self.logger.error(traceback.format_exc())
            return create_empty_ggbscript_output()

    async def _process_reflection(
        self, state: ImageAnalysisState
    ) -> tuple[ReflectionOutput, list[GGBCommand]]:
        """Reflection stage: Validate and fix commands.

        Args:
            state: Current pipeline state

        Returns:
            Tuple of (reflection output, final commands)
        """
        self.logger.info(f"Reflection stage - session: {state.session_id}")

        try:
            prompt = self._render_prompt(
                "reflection",
                {
                    "question_text": state.question_text,
                    "bbox_output_json": state.bbox_output,
                    "analysis_output_json": state.analysis_output,
                    "ggbscript_output_json": state.ggbscript_output,
                },
            )

            response = await self._call_vision_llm(
                prompt=prompt,
                image_base64=state.image_base64,
                temperature=0.3,
            )

            reflection_output = self._extract_json_from_response(response)

            # Extract final commands
            final_commands = reflection_output.get("corrected_commands", [])
            if not final_commands:
                # If no corrections, use original commands
                final_commands = state.ggbscript_output.get("commands", [])

            issues_count = len(reflection_output.get("issues_found", []))
            self.logger.info(
                f"Reflection completed - issues: {issues_count}, final commands: {len(final_commands)}"
            )

            return reflection_output, final_commands

        except Exception as e:
            self.logger.error(f"Reflection stage error: {e}")
            self.logger.error(traceback.format_exc())
            return create_empty_reflection_output(), state.ggbscript_output.get("commands", [])

    # ==================== Main Pipeline ====================

    async def process(
        self,
        question_text: str,
        image_base64: str | None = None,
        session_id: str = "default",
    ) -> dict[str, Any]:
        """Process a math problem with optional image.

        Args:
            question_text: The problem text
            image_base64: Optional base64 encoded image
            session_id: Session identifier

        Returns:
            Dictionary with analysis results and final GGB commands
        """
        state = ImageAnalysisState(
            session_id=session_id,
            question_text=question_text,
            image_base64=image_base64,
            has_image=bool(image_base64),
        )

        if not state.has_image:
            return {
                "has_image": False,
                "final_ggb_commands": [],
            }

        # Run pipeline
        state.bbox_output = await self._process_bbox(state)
        state.analysis_output, state.image_is_reference = await self._process_analysis(state)
        state.ggbscript_output = await self._process_ggbscript(state)
        state.reflection_output, state.final_ggb_commands = await self._process_reflection(state)

        return {
            "has_image": True,
            "bbox_output": state.bbox_output,
            "analysis_output": state.analysis_output,
            "ggbscript_output": state.ggbscript_output,
            "reflection_output": state.reflection_output,
            "final_ggb_commands": state.final_ggb_commands,
            "image_is_reference": state.image_is_reference,
        }

    async def stream_process(
        self,
        question_text: str,
        image_base64: str | None = None,
        session_id: str = "default",
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream the analysis process with stage-by-stage events.

        Args:
            question_text: The problem text
            image_base64: Optional base64 encoded image
            session_id: Session identifier

        Yields:
            Event dictionaries for each stage completion
        """
        state = ImageAnalysisState(
            session_id=session_id,
            question_text=question_text,
            image_base64=image_base64,
            has_image=bool(image_base64),
        )

        if not state.has_image:
            yield {"event": "no_image", "data": {}}
            return

        yield {"event": "analysis_start", "data": {"session_id": session_id}}

        # BBox stage
        state.bbox_output = await self._process_bbox(state)
        elements = state.bbox_output.get("elements", [])
        yield {
            "event": "bbox_complete",
            "data": {
                "stage": "bbox",
                "elements_count": len(elements),
                "elements": [
                    {"type": e.get("type", "unknown"), "label": e.get("label", "")}
                    for e in elements[:10]
                ],
            },
        }

        # Analysis stage
        state.analysis_output, state.image_is_reference = await self._process_analysis(state)
        constraints = state.analysis_output.get("constraints", [])
        relations = state.analysis_output.get("geometric_relations", [])
        yield {
            "event": "analysis_complete",
            "data": {
                "stage": "analysis",
                "constraints_count": len(constraints),
                "relations_count": len(relations),
                "image_is_reference": state.image_is_reference,
                "constraints": constraints[:10] if isinstance(constraints, list) else [],
            },
        }

        # GGBScript stage
        state.ggbscript_output = await self._process_ggbscript(state)
        commands = state.ggbscript_output.get("commands", [])
        yield {
            "event": "ggbscript_complete",
            "data": {
                "stage": "ggbscript",
                "commands_count": len(commands),
                "commands": [
                    {"command": c.get("command", ""), "description": c.get("description", "")}
                    for c in commands[:10]
                ],
            },
        }

        # Reflection stage
        state.reflection_output, state.final_ggb_commands = await self._process_reflection(state)
        issues = state.reflection_output.get("issues_found", [])
        yield {
            "event": "reflection_complete",
            "data": {
                "stage": "reflection",
                "issues_count": len(issues),
                "commands_count": len(state.final_ggb_commands),
                "final_commands": state.final_ggb_commands,
            },
        }

        # Final analysis message
        ggb_script_content = self._format_ggb_commands(state.final_ggb_commands)
        yield {
            "event": "analysis_message_complete",
            "data": {
                "ggb_block": {
                    "page_id": "image-analysis-restore",
                    "title": "题目配图还原",
                    "content": ggb_script_content,
                }
                if ggb_script_content
                else None,
                "analysis_summary": {
                    "constraints": constraints[:10] if isinstance(constraints, list) else [],
                    "relations": [
                        r.get("description", str(r)) if isinstance(r, dict) else str(r)
                        for r in relations[:10]
                    ],
                },
            },
        }

    def _format_ggb_commands(self, commands: list[GGBCommand]) -> str:
        """Format GGB commands into script content.

        Args:
            commands: List of GGB command dictionaries

        Returns:
            Formatted script string
        """
        if not commands:
            return ""

        lines = []
        for cmd in commands:
            if isinstance(cmd, dict):
                command = cmd.get("command", "")
                description = cmd.get("description", "")
                if description:
                    lines.append(f"# {description}")
                lines.append(command)
            else:
                lines.append(str(cmd))

        return "\n".join(lines)

    def format_ggb_block(
        self, commands: list[GGBCommand], page_id: str = "main", title: str = "题目图形"
    ) -> str:
        """Format commands into a ggbscript block.

        Args:
            commands: List of GGB commands
            page_id: Page identifier
            title: Block title

        Returns:
            Formatted ggbscript block string
        """
        content = self._format_ggb_commands(commands)
        if not content:
            return ""

        return f"```ggbscript[{page_id};{title}]\n{content}\n```"

    # ==================== Tutor Response ====================

    async def stream_tutor_response(
        self,
        question_text: str,
        final_ggb_commands: list[GGBCommand],
        analysis_output: dict | None = None,
        session_id: str = "default",
    ) -> AsyncGenerator[str, None]:
        """Stream the tutor's solution response based on image analysis.

        Args:
            question_text: The problem text
            final_ggb_commands: GeoGebra commands from image analysis
            analysis_output: Analysis stage output (optional)
            session_id: Session identifier

        Yields:
            Text chunks of the tutor's response
        """
        self.logger.info(f"[{session_id}] Starting tutor response stream")

        # Prepare context for tutor prompt
        ggb_commands_str = self._format_ggb_commands(final_ggb_commands)

        # Get analysis metrics
        elements_count = 0
        constraints_count = 0
        image_is_reference = False

        if analysis_output:
            constraints = analysis_output.get("constraints", [])
            constraints_count = len(constraints) if isinstance(constraints, list) else 0
            image_is_reference = analysis_output.get("image_reference_detected", False)

        # Render tutor prompt
        tutor_prompt = self._render_prompt(
            "tutor",
            {
                "question_text": question_text,
                "ggb_commands": ggb_commands_str,
                "elements_count": len(final_ggb_commands),
                "constraints_count": constraints_count,
                "image_is_reference": "是" if image_is_reference else "否",
            },
        )

        # Stream response from LLM
        try:
            async for chunk in self.stream_llm(
                user_prompt=tutor_prompt,
                system_prompt="你是一位专业的数学教师，善于使用可视化方式解释数学问题。请基于图像分析结果，为学生提供清晰、详细的解题过程。",
                temperature=0.7,
            ):
                yield chunk

        except Exception as e:
            self.logger.error(f"[{session_id}] Tutor response error: {e}")
            yield f"\n\n抱歉，解题过程生成出现错误：{e}"

    async def stream_process_with_tutor(
        self,
        question_text: str,
        image_base64: str | None = None,
        session_id: str = "default",
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream the full analysis and tutor response process.

        Args:
            question_text: The problem text
            image_base64: Optional base64 encoded image
            session_id: Session identifier

        Yields:
            Event dictionaries for each stage and tutor response chunks
        """
        state = ImageAnalysisState(
            session_id=session_id,
            question_text=question_text,
            image_base64=image_base64,
            has_image=bool(image_base64),
        )

        if not state.has_image:
            yield {"event": "no_image", "data": {}}
            # Even without image, we can still provide a solution
            yield {"event": "answer_start", "data": {"has_image_analysis": False}}
            async for chunk in self.stream_tutor_response(
                question_text=question_text,
                final_ggb_commands=[],
                analysis_output=None,
                session_id=session_id,
            ):
                yield {"event": "text", "data": {"content": chunk}}
            yield {"event": "done", "data": {}}
            return

        yield {"event": "analysis_start", "data": {"session_id": session_id}}

        # BBox stage
        state.bbox_output = await self._process_bbox(state)
        elements = state.bbox_output.get("elements", [])
        yield {
            "event": "bbox_complete",
            "data": {
                "stage": "bbox",
                "elements_count": len(elements),
                "elements": [
                    {"type": e.get("type", "unknown"), "label": e.get("label", "")}
                    for e in elements[:10]
                ],
            },
        }

        # Analysis stage
        state.analysis_output, state.image_is_reference = await self._process_analysis(state)
        constraints = state.analysis_output.get("constraints", [])
        relations = state.analysis_output.get("geometric_relations", [])
        yield {
            "event": "analysis_complete",
            "data": {
                "stage": "analysis",
                "constraints_count": len(constraints),
                "relations_count": len(relations),
                "image_is_reference": state.image_is_reference,
                "constraints": constraints[:10] if isinstance(constraints, list) else [],
            },
        }

        # GGBScript stage
        state.ggbscript_output = await self._process_ggbscript(state)
        commands = state.ggbscript_output.get("commands", [])
        yield {
            "event": "ggbscript_complete",
            "data": {
                "stage": "ggbscript",
                "commands_count": len(commands),
                "commands": [
                    {"command": c.get("command", ""), "description": c.get("description", "")}
                    for c in commands[:10]
                ],
            },
        }

        # Reflection stage
        state.reflection_output, state.final_ggb_commands = await self._process_reflection(state)
        issues = state.reflection_output.get("issues_found", [])
        yield {
            "event": "reflection_complete",
            "data": {
                "stage": "reflection",
                "issues_count": len(issues),
                "commands_count": len(state.final_ggb_commands),
                "final_commands": state.final_ggb_commands,
            },
        }

        # Analysis message with GGB block
        ggb_script_content = self._format_ggb_commands(state.final_ggb_commands)
        yield {
            "event": "analysis_message_complete",
            "data": {
                "ggb_block": {
                    "page_id": "image-analysis-restore",
                    "title": "题目配图还原",
                    "content": ggb_script_content,
                }
                if ggb_script_content
                else None,
                "analysis_summary": {
                    "constraints": constraints[:10] if isinstance(constraints, list) else [],
                    "relations": [
                        r.get("description", str(r)) if isinstance(r, dict) else str(r)
                        for r in relations[:10]
                    ],
                },
            },
        }

        # Start tutor response
        yield {"event": "answer_start", "data": {"has_image_analysis": True}}

        # Stream tutor response
        async for chunk in self.stream_tutor_response(
            question_text=question_text,
            final_ggb_commands=state.final_ggb_commands,
            analysis_output=state.analysis_output,
            session_id=session_id,
        ):
            yield {"event": "text", "data": {"content": chunk}}

        yield {"event": "done", "data": {}}
