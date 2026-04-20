"""Block generators – one per ``BlockType``."""

from .base import (
    BlockContext,
    BlockGenerator,
    BlockGeneratorRegistry,
    GenerationFailure,
    get_block_registry,
)
from .callout import CalloutGenerator
from .quiz import QuizGenerator
from .text import TextGenerator, generate_bridge_text
from .user_note import UserNoteGenerator

# Phase 2+ generators
from .animation import AnimationGenerator
from .code import CodeGenerator
from .deep_dive import DeepDiveGenerator
from .figure import FigureGenerator
from .flash_cards import FlashCardsGenerator
from .interactive import InteractiveGenerator
from .timeline import TimelineGenerator

__all__ = [
    "BlockContext",
    "BlockGenerator",
    "BlockGeneratorRegistry",
    "GenerationFailure",
    "get_block_registry",
    "TextGenerator",
    "generate_bridge_text",
    "CalloutGenerator",
    "QuizGenerator",
    "UserNoteGenerator",
    "FigureGenerator",
    "InteractiveGenerator",
    "AnimationGenerator",
    "CodeGenerator",
    "TimelineGenerator",
    "FlashCardsGenerator",
    "DeepDiveGenerator",
]
