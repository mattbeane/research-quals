"""SkillForge CLI - Competency-based training for mixed-methods management research."""

from .skillforge import main
from .competency_gate import check_competency, get_unlocked_commands, get_next_to_unlock
from . import evaluator

__all__ = ["main", "check_competency", "get_unlocked_commands", "get_next_to_unlock", "evaluator"]
