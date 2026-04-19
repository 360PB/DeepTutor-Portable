"""Data models for Vision Solver image analysis pipeline.

Defines input/output structures for the four-stage analysis:
1. BBox - Coordinate detection
2. Analysis - Geometric semantic analysis
3. GGBScript - Drawing command generation
4. Reflection - Validation and correction
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict

# ==================== BBox Stage Models ====================


class ImageDimensions(TypedDict):
    """Image dimensions."""

    width: int
    height: int


class Coordinate(TypedDict):
    """Pixel coordinate."""

    x: int
    y: int


class CoordElement(TypedDict, total=False):
    """Coordinate element with different fields for different types.

    Types:
    - point: element_id, type, label, position
    - segment: element_id, type, label, start, end
    - polygon: element_id, type, label, vertices
    - circle: element_id, type, label, center, radius
    """

    element_id: str
    type: str  # point/segment/polygon/circle/arc/angle
    label: str
    position: Coordinate  # For points
    start: Coordinate  # For segments
    end: Coordinate  # For segments
    vertices: list[dict]  # For polygons
    center: Coordinate  # For circles/arcs
    radius: int  # Pixel radius for circles


class BBoxOutput(TypedDict):
    """BBox stage output: pure visual recognition results.

    Responsibility: Extract pixel coordinates of all geometric elements
    Coordinate system: Origin at top-left, Y-axis downward
    """

    image_dimensions: ImageDimensions
    elements: list[CoordElement]


# ==================== Analysis Stage Models ====================


class PointDefinition(TypedDict, total=False):
    """Point definition with three types.

    1. has_coordinate=True: Point with coordinates from problem text
    2. use_bbox=True: Visible in image but no coordinates in text
    3. type="derived": Derived point (only when explicitly stated)
    """

    label: str
    type: str  # "free" | "derived"
    has_coordinate: bool
    coordinate: Coordinate | None
    use_bbox: bool
    bbox_position: Coordinate | None
    estimated_ggb_coordinate: Coordinate | None
    estimation_method: str
    anchor_points: list[str]
    derivation_method: str
    derivation_params: list[str]
    source: str


class SegmentDefinition(TypedDict):
    """Segment definition."""

    label: str
    endpoints: list[str]
    is_auxiliary: bool


class ShapeDefinition(TypedDict, total=False):
    """Shape definition."""

    label: str
    type: str
    vertices: list[str]


class CircleDefinition(TypedDict, total=False):
    """Circle definition."""

    label: str
    center: str
    radius: float | None
    radius_segment: str | None
    through_point: str | None


class KeyElements(TypedDict, total=False):
    """Key geometric elements."""

    points: list[PointDefinition]
    segments: list[SegmentDefinition]
    shapes: list[ShapeDefinition]
    circles: list[CircleDefinition]
    special_points: list[PointDefinition]


class GeometricRelationType(str, Enum):
    """Types of geometric relations."""

    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"
    EQUAL_LENGTH = "equal_length"
    MIDPOINT = "midpoint"
    INTERSECTION = "intersection"
    TANGENT = "tangent"
    CONGRUENT = "congruent"
    SIMILAR = "similar"
    BISECTOR = "bisector"
    ON_LINE = "on_line"
    ON_CIRCLE = "on_circle"


class GeometricRelation(TypedDict):
    """Geometric relation."""

    type: str
    objects: list[str]
    description: str


class RelativePositionAnalysis(TypedDict, total=False):
    """Relative position analysis."""

    point: str
    observations: list[str]
    conclusions: dict


class AnalysisOutput(TypedDict, total=False):
    """Analysis stage output: geometric semantic analysis results.

    Responsibility: Extract geometric relations, constraints, special point definitions
    """

    image_reference_detected: bool
    image_reference_keywords: list[str]
    key_elements: KeyElements
    constraints: list
    geometric_relations: list[GeometricRelation]
    relative_position_analysis: list[RelativePositionAnalysis]
    element_positions: dict
    annotations: list[dict]
    construction_steps: list[dict]


# ==================== GGBScript Stage Models ====================


class GGBCommand(TypedDict):
    """GeoGebra command."""

    sequence: int
    command: str
    description: str


class GGBScriptOutput(TypedDict):
    """GGBScript stage output: GeoGebra drawing commands.

    Responsibility: Generate accurate GeoGebra command sequence
    Principle: Compass-and-ruler construction, prefer derived points
    """

    commands: list[GGBCommand]


# ==================== Reflection Stage Models ====================


class VerificationResult(TypedDict):
    """Verification result."""

    check_type: str
    target: str
    expected: str
    actual: str
    passed: bool


class IssueFound(TypedDict, total=False):
    """Issue found during verification."""

    issue_id: str
    severity: str  # "critical", "error", "warning"
    category: str
    description: str
    affected_commands: list[int]
    correction_needed: str


class Correction(TypedDict):
    """Correction for an issue."""

    issue_id: str
    action: str  # "replace", "insert", "delete"
    target_sequence: int | None
    new_command: str | None
    reason: str


class FinalVerification(TypedDict, total=False):
    """Final verification results."""

    no_wrong_assumptions: bool
    all_derived_points_use_commands: bool
    all_use_bbox_points_use_coordinates: bool
    all_constraints_satisfied: bool
    layout_matches_original: bool
    ready_for_rendering: bool


class ReflectionOutput(TypedDict):
    """Reflection stage output: validation and correction results.

    Responsibility: Verify command correctness, find issues and fix them
    """

    verification_results: list[VerificationResult]
    issues_found: list[IssueFound]
    corrections: list[Correction]
    final_verification: FinalVerification
    corrected_commands: list[GGBCommand]


# ==================== Pipeline State ====================


@dataclass
class ImageAnalysisState:
    """State for the image analysis pipeline."""

    session_id: str
    question_text: str
    image_base64: str | None = None

    # Stage outputs
    bbox_output: BBoxOutput | None = None
    analysis_output: AnalysisOutput | None = None
    ggbscript_output: GGBScriptOutput | None = None
    reflection_output: ReflectionOutput | None = None

    # Final results
    final_ggb_commands: list[GGBCommand] = field(default_factory=list)

    # Flags
    image_is_reference: bool = False
    has_image: bool = False


# ==================== Helper Functions ====================


def create_empty_bbox_output() -> BBoxOutput:
    """Create empty BBox output."""
    return {"image_dimensions": {"width": 0, "height": 0}, "elements": []}


def create_empty_analysis_output() -> AnalysisOutput:
    """Create empty Analysis output."""
    return {
        "image_reference_detected": False,
        "image_reference_keywords": [],
        "key_elements": {
            "points": [],
            "segments": [],
            "shapes": [],
            "circles": [],
            "special_points": [],
        },
        "constraints": [],
        "geometric_relations": [],
        "relative_position_analysis": [],
        "element_positions": {"relative_positions": [], "layout_description": ""},
        "annotations": [],
        "construction_steps": [],
    }


def create_empty_ggbscript_output() -> GGBScriptOutput:
    """Create empty GGBScript output."""
    return {"commands": []}


def create_empty_reflection_output() -> ReflectionOutput:
    """Create empty Reflection output."""
    return {
        "verification_results": [],
        "issues_found": [],
        "corrections": [],
        "final_verification": {
            "no_wrong_assumptions": False,
            "all_derived_points_use_commands": False,
            "all_use_bbox_points_use_coordinates": False,
            "all_constraints_satisfied": False,
            "layout_matches_original": False,
            "ready_for_rendering": False,
        },
        "corrected_commands": [],
    }
