"""Vision Solver API Router.

WebSocket endpoint for real-time image analysis with GeoGebra visualization.
"""

import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from deeptutor.agents.vision_solver import VisionSolverAgent
from deeptutor.logging import get_logger
from deeptutor.services.llm import get_llm_config
from deeptutor.services.settings.interface_settings import get_ui_language
from deeptutor.tools.vision import ImageError, resolve_image_input

logger = get_logger("VisionSolverAPI", level="INFO")

router = APIRouter()


# ==================== Request/Response Models ====================


class VisionAnalyzeRequest(BaseModel):
    """Request for image analysis."""

    question: str
    image_base64: str | None = None
    image_url: str | None = None
    session_id: str | None = None


class VisionAnalyzeResponse(BaseModel):
    """Response from image analysis."""

    session_id: str
    has_image: bool
    final_ggb_commands: list[dict] = []
    ggb_script: str | None = None
    analysis_summary: dict = {}


# ==================== REST Endpoints ====================


@router.post("/vision/analyze")
async def analyze_image(request: VisionAnalyzeRequest) -> VisionAnalyzeResponse:
    """Analyze a math problem image and return GeoGebra commands.

    Args:
        request: Analysis request with question and image

    Returns:
        Analysis response with GGB commands
    """
    session_id = request.session_id or f"vision_{id(request)}"

    try:
        # Resolve image input
        image_base64 = await resolve_image_input(
            image_base64=request.image_base64,
            image_url=request.image_url,
        )

        if not image_base64:
            return VisionAnalyzeResponse(
                session_id=session_id,
                has_image=False,
            )

        # Get LLM config
        try:
            llm_config = get_llm_config()
            api_key = llm_config.api_key
            base_url = llm_config.base_url
        except Exception as e:
            logger.error(f"Failed to get LLM config: {e}")
            raise HTTPException(status_code=500, detail=f"LLM configuration error: {e}")

        # Initialize agent
        language = get_ui_language(default="zh")
        agent = VisionSolverAgent(
            api_key=api_key,
            base_url=base_url,
            language=language,
        )

        # Process image
        result = await agent.process(
            question_text=request.question,
            image_base64=image_base64,
            session_id=session_id,
        )

        # Format GGB script
        ggb_script = None
        if result.get("final_ggb_commands"):
            ggb_script = agent.format_ggb_block(
                result["final_ggb_commands"],
                page_id="analysis",
                title="题目图形",
            )

        return VisionAnalyzeResponse(
            session_id=session_id,
            has_image=result.get("has_image", False),
            final_ggb_commands=result.get("final_ggb_commands", []),
            ggb_script=ggb_script,
            analysis_summary={
                "image_is_reference": result.get("image_is_reference", False),
                "elements_count": len(result.get("bbox_output", {}).get("elements", [])),
                "commands_count": len(result.get("final_ggb_commands", [])),
            },
        )

    except ImageError as e:
        logger.error(f"Image error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== WebSocket Endpoint ====================


@router.websocket("/vision/solve")
async def websocket_vision_solve(websocket: WebSocket):
    """WebSocket endpoint for streaming image analysis.

    Protocol:
    1. Client sends: {"question": "...", "image_base64": "...", "session_id": "..."}
    2. Server streams:
       - {"type": "session", "session_id": "..."}
       - {"type": "analysis_start", "data": {...}}
       - {"type": "bbox_complete", "data": {...}}
       - {"type": "analysis_complete", "data": {...}}
       - {"type": "ggbscript_complete", "data": {...}}
       - {"type": "reflection_complete", "data": {...}}
       - {"type": "analysis_message_complete", "data": {...}}
       - {"type": "answer_start", "data": {...}}
       - {"type": "text", "content": "..."}
       - {"type": "done"}
    """
    await websocket.accept()

    connection_closed = asyncio.Event()

    async def safe_send_json(data: dict[str, Any]) -> bool:
        """Safely send JSON, checking if connection is closed."""
        if connection_closed.is_set():
            return False
        try:
            await websocket.send_json(data)
            return True
        except (WebSocketDisconnect, RuntimeError, ConnectionError) as e:
            logger.debug(f"WebSocket connection closed: {e}")
            connection_closed.set()
            return False
        except Exception as e:
            logger.debug(f"Error sending WebSocket message: {e}")
            return False

    session_id = None

    try:
        # 1. Receive initial message
        data = await websocket.receive_json()
        question = data.get("question")
        image_base64 = data.get("image_base64")
        image_url = data.get("image_url")
        session_id = data.get("session_id", f"vision_{id(data)}")

        if not question:
            await safe_send_json({"type": "error", "content": "Question is required"})
            return

        # Send session ID
        await safe_send_json({"type": "session", "session_id": session_id})

        # 2. Resolve image input
        try:
            resolved_image = await resolve_image_input(
                image_base64=image_base64,
                image_url=image_url,
            )
        except ImageError as e:
            await safe_send_json({"type": "error", "content": str(e)})
            return

        if not resolved_image:
            await safe_send_json({"type": "no_image", "data": {}})
            await safe_send_json({"type": "done"})
            return

        # 3. Initialize agent
        try:
            llm_config = get_llm_config()
            api_key = llm_config.api_key
            base_url = llm_config.base_url
        except Exception as e:
            logger.error(f"Failed to get LLM config: {e}")
            await safe_send_json({"type": "error", "content": f"LLM configuration error: {e}"})
            return

        language = get_ui_language(default="zh")
        agent = VisionSolverAgent(
            api_key=api_key,
            base_url=base_url,
            language=language,
        )

        logger.info(f"[{session_id}] Starting vision analysis: {question[:50]}...")

        # 4. Stream analysis and tutor response
        async for event in agent.stream_process_with_tutor(
            question_text=question,
            image_base64=resolved_image,
            session_id=session_id,
        ):
            event_type = event.get("event", "unknown")
            event_data = event.get("data", {})

            if not await safe_send_json({"type": event_type, "data": event_data}):
                break

        logger.info(f"[{session_id}] Vision analysis and tutor response completed")

    except WebSocketDisconnect:
        logger.info(f"[{session_id}] WebSocket disconnected")
    except Exception as e:
        connection_closed.set()
        await safe_send_json({"type": "error", "content": str(e)})
        logger.error(f"[{session_id}] Vision solve failed: {e}", exc_info=True)
    finally:
        connection_closed.set()
        try:
            if hasattr(websocket, "client_state"):
                state = websocket.client_state
                if hasattr(state, "name") and state.name != "DISCONNECTED":
                    await websocket.close()
            else:
                await websocket.close()
        except (WebSocketDisconnect, RuntimeError, ConnectionError):
            pass
        except Exception as e:
            logger.debug(f"Error closing WebSocket: {e}")
