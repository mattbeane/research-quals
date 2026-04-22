"""
SkillForge Competency Gate - Integration with TheoryForge

This module provides competency checking for TheoryForge commands.
Import and call check_competency() before running gated commands.

Usage in TheoryForge:
    from skillforge.cli.competency_gate import check_competency

    allowed, message = check_competency("mine-qual")
    if not allowed:
        print(message)
        return
"""

import json
from pathlib import Path
from typing import Tuple

# Map TheoryForge commands to required competencies
# Format: {command: {domain: required_level}}
UNLOCK_MAP = {
    # Phase 1: Basic pattern finding
    "hunt-patterns": {"domain-1": 3},

    # Phase 2: Theory-building
    "find-theory": {"domain-1": 3, "domain-2": 3},
    "mine-qual": {"domain-2": 3, "domain-3": 3},

    # Phase 3: Framing and evaluation
    "smith-frames": {"domain-3": 3, "domain-4": 3},
    "eval-zuckerman": {"domain-3": 3, "domain-4": 3},
    "eval-genre": {"domain-4": 3, "domain-5": 3},

    # Phase 4: Paper drafting
    "draft-paper": {"domain-4": 3, "domain-5": 3},
    "audit-claims": {"domain-5": 3, "domain-6": 3},

    # Phase 5: Final verification
    "verify-claims": {"domain-5": 3, "domain-6": 3},
    "package-verification": {"domain-6": 3, "domain-7": 3},
}

DOMAIN_NAMES = {
    "domain-1": "Pattern Recognition",
    "domain-2": "Theoretical Positioning",
    "domain-3": "Qualitative Mechanism",
    "domain-4": "Theoretical Framing",
    "domain-5": "Epistemological Genre",
    "domain-6": "Adversarial Evidence",
    "domain-7": "Claim Verification",
}


def get_skillforge_home() -> Path:
    """Get SkillForge home directory."""
    return Path.home() / ".skillforge"


def get_student_record() -> dict:
    """Load student record if it exists."""
    record_path = get_skillforge_home() / "record.json"
    if record_path.exists():
        return json.loads(record_path.read_text())
    return None


def check_competency(command: str, student_id: str = None) -> Tuple[bool, str]:
    """
    Check if the current user has competency to run a command.

    Args:
        command: TheoryForge command name (e.g., "mine-qual")
        student_id: Optional student ID override

    Returns:
        (allowed, message): Whether allowed, and a message if not
    """
    # Ungated commands always allowed
    if command not in UNLOCK_MAP:
        return True, ""

    # Load student record
    record = get_student_record()

    # No record = faculty/expert mode (no restrictions)
    if record is None:
        return True, ""

    # Check if student ID matches (if provided)
    if student_id and record.get("student_id") != student_id:
        return True, ""  # Different user, no restrictions

    # Check requirements
    requirements = UNLOCK_MAP[command]
    missing = []

    for domain, required_level in requirements.items():
        student_level = record.get("domains", {}).get(domain, {}).get("level", 0)
        if student_level < required_level:
            domain_name = DOMAIN_NAMES.get(domain, domain)
            missing.append(f"{domain_name} Level {required_level}")

    if missing:
        msg = f"🔒 /{command} requires competency in:\n"
        for m in missing:
            msg += f"   • {m}\n"
        msg += f"\nRun 'skillforge status' to see your progress."
        msg += f"\nRun 'skillforge take <domain> --level 1' to begin."
        return False, msg

    return True, ""


def get_unlocked_commands() -> list:
    """Get list of commands the current student can run."""
    record = get_student_record()

    if record is None:
        # Faculty mode: all commands available
        return list(UNLOCK_MAP.keys())

    unlocked = []
    for command, requirements in UNLOCK_MAP.items():
        is_unlocked = all(
            record.get("domains", {}).get(domain, {}).get("level", 0) >= level
            for domain, level in requirements.items()
        )
        if is_unlocked:
            unlocked.append(command)

    return unlocked


def get_next_to_unlock() -> dict:
    """
    Get the next commands that could be unlocked and what's needed.

    Returns:
        {command: [missing_requirements]}
    """
    record = get_student_record()

    if record is None:
        return {}

    almost = {}
    for command, requirements in UNLOCK_MAP.items():
        missing = []
        for domain, level in requirements.items():
            student_level = record.get("domains", {}).get(domain, {}).get("level", 0)
            if student_level < level:
                missing.append({
                    "domain": domain,
                    "name": DOMAIN_NAMES.get(domain, domain),
                    "current": student_level,
                    "required": level,
                    "gap": level - student_level,
                })

        # Only show commands where 1-2 domains are missing
        if 0 < len(missing) <= 2:
            almost[command] = missing

    return almost


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        allowed, message = check_competency(command)
        if allowed:
            print(f"✅ /{command} is available")
        else:
            print(message)
    else:
        print("Available commands for current user:")
        for cmd in get_unlocked_commands():
            print(f"  /{cmd}")

        print("\nAlmost unlocked:")
        for cmd, missing in get_next_to_unlock().items():
            needs = ", ".join(f"{m['name']} L{m['required']}" for m in missing)
            print(f"  /{cmd} — needs: {needs}")
