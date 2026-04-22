#!/usr/bin/env python3
"""
SkillForge Evaluation Engine - Level 2-3 Assessment Scoring

Uses LLM-based evaluation against expert baselines to score student work.
Follows the scoring rubrics defined in ASSESSMENT_SPECS.md.

Level 2: Application with feedback (≥70/100, 7-day cooldown on retry)
Level 3: Authentic performance (≥70/100, no criterion below 50%, 30-day cooldown)
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Try to import anthropic, fall back to subprocess if not available
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

SKILLFORGE_HOME = Path.home() / ".skillforge"
PROJECT_ROOT = Path(__file__).parent.parent
BASELINE_PATH = PROJECT_ROOT / "seed-data" / "beane-surgery-anonymized" / "expert_baseline.md"

DOMAIN_NAMES = {
    "domain-1": "Pattern Recognition",
    "domain-2": "Theoretical Positioning",
    "domain-3": "Qualitative Mechanism",
    "domain-4": "Theoretical Framing",
    "domain-5": "Epistemological Genre",
    "domain-6": "Adversarial Evidence",
    "domain-7": "Claim Verification",
}

# Structured evaluation prompts with few-shot examples
EVALUATION_SYSTEM_PROMPT = """You are an expert evaluator for SkillForge, a competency-based training system for mixed-methods management research. You evaluate student submissions against expert baselines.

Your evaluation must be:
1. Fair but rigorous - students should earn their scores
2. Specific - cite evidence from student work
3. Constructive - explain what's missing, not just that it's missing

You MUST respond with valid JSON matching the schema provided. No other text."""

DOMAIN_RUBRICS = {
    "domain-1": {
        "name": "Pattern Recognition",
        "criteria": [
            {"name": "found_patterns", "max_points": 30, "description": "Identified patterns the expert found"},
            {"name": "avoided_false_positives", "max_points": 20, "description": "Avoided pursuing noise as signal"},
            {"name": "reasoning_quality", "max_points": 30, "description": "Robustness thinking is sound"},
            {"name": "completeness", "max_points": 20, "description": "Documented killed findings, heterogeneity, etc."},
        ],
        "examples": {
            "good": """Student identified the main pattern (trainees getting less hands-on time with robots) and explored heterogeneity across hospitals. They documented two patterns they killed because effect sizes were too small. Strong robustness instinct shown by checking controls before framing.""",
            "weak": """Student reported three "significant" correlations but didn't check robustness or explore heterogeneity. No killed findings documented. Treated p<0.05 as sufficient for theoretical interest.""",
        }
    },
    "domain-2": {
        "name": "Theoretical Positioning",
        "criteria": [
            {"name": "conversation_identified", "max_points": 25, "description": "Identified specific scholarly debate"},
            {"name": "contribution_specified", "max_points": 25, "description": "Articulated what would change"},
            {"name": "positioning_quality", "max_points": 30, "description": "Specific, bounded, theoretically grounded"},
            {"name": "alternatives_considered", "max_points": 20, "description": "Considered multiple positioning options"},
        ],
        "examples": {
            "good": """Student positioned against communities of practice theory, specifically arguing that when legitimate peripheral participation fails, alternative learning paths emerge. Clear contribution: extends CoP by showing boundary conditions. Generated three alternative framings and explained why CoP positioning was strongest.""",
            "weak": """Student said they 'contribute to the learning literature' without specifying which debate or what would change. No alternative framings considered. Positioning too broad to be a contribution.""",
        }
    },
    "domain-3": {
        "name": "Qualitative Mechanism",
        "criteria": [
            {"name": "mechanism_overlap", "max_points": 30, "description": "Found mechanisms expert found"},
            {"name": "evidence_overlap", "max_points": 25, "description": "Identified key evidence expert used"},
            {"name": "disconfirming_evidence", "max_points": 30, "description": "Found and engaged with disconfirming cases"},
            {"name": "coding_quality", "max_points": 15, "description": "Codes are action/process-oriented"},
        ],
        "special_rules": ["Must find ≥50% of disconfirming evidence to pass (disconfirm_check)"],
        "examples": {
            "good": """Student identified shadow learning and participation barriers mechanisms. Codes like 'undersupervised struggle' and 'helicopter teaching' capture action. Found 2 of 3 disconfirming cases and used them to specify boundary conditions.""",
            "weak": """Student used topic codes ('Technology', 'Learning') instead of process codes. Found supporting evidence but zero disconfirming cases mentioned. Cherry-picked vivid quotes without distribution.""",
        }
    },
    "domain-4": {
        "name": "Theoretical Framing",
        "criteria": [
            {"name": "novel", "max_points": 25, "description": "Framing is genuinely new"},
            {"name": "true", "max_points": 25, "description": "Evidence supports the framing"},
            {"name": "important", "max_points": 25, "description": "Would matter to target conversation"},
            {"name": "reachable", "max_points": 25, "description": "Audience can understand and engage"},
        ],
        "examples": {
            "good": """Frame: 'Technologies that concentrate control eliminate participation gradients enabling skill transfer.' Novel (extends CoP), True (evidence shows mechanism), Important (changes how we think about tech and learning), Reachable (clear mechanism, bounded scope). Generated 4 candidate frames.""",
            "weak": """Frame: 'Robots affect surgical training.' Too vague - doesn't specify mechanism, conditions, or what changes. Not bounded enough to be testable or generalizable.""",
        }
    },
    "domain-5": {
        "name": "Epistemological Genre",
        "criteria": [
            {"name": "genre_identification", "max_points": 25, "description": "Correctly identified discovery vs testing"},
            {"name": "method_claim_alignment", "max_points": 30, "description": "Claims match what methods support"},
            {"name": "appropriate_hedging", "max_points": 25, "description": "Causal/scope claims appropriately bounded"},
            {"name": "generalization_type", "max_points": 20, "description": "Distinguishes theoretical vs statistical generalization"},
        ],
        "examples": {
            "good": """Correctly identified work as theory-building (discovery). Claims use 'appears to enable' not 'causes'. Explicit about theoretical generalization: mechanism may apply where conditions hold, not claiming population prevalence.""",
            "weak": """Claims to 'test hypothesis' but used discovery methods with no comparison group. Says evidence 'proves' causation from qualitative interviews. Genre confusion throughout.""",
        }
    },
    "domain-6": {
        "name": "Adversarial Evidence",
        "criteria": [
            {"name": "disconfirmation_search", "max_points": 30, "description": "Actively searched for counter-evidence"},
            {"name": "distribution_reported", "max_points": 25, "description": "Reported full distribution, not just supporting cases"},
            {"name": "boundary_conditions", "max_points": 25, "description": "Used disconfirming cases to identify scope"},
            {"name": "integration", "max_points": 20, "description": "Reconciled disconfirming evidence with theory"},
        ],
        "examples": {
            "good": """Reported: 8 strong, 4 weak, 3 absent. Investigated the 3 absent cases - all from one hospital type, leading to boundary condition. Created adversarial codes and re-read all data looking for challenges.""",
            "weak": """Reported 10 supporting quotes with no distribution. 'No disconfirming evidence found' - red flag suggesting confirmation bias. No adversarial coding strategy described.""",
        }
    },
    "domain-7": {
        "name": "Claim Verification",
        "criteria": [
            {"name": "overclaims_identified", "max_points": 40, "description": "Caught causal, scope, measurement overclaims"},
            {"name": "false_positives_avoided", "max_points": 20, "description": "Didn't flag appropriate claims"},
            {"name": "revision_quality", "max_points": 40, "description": "Suggested revisions appropriately calibrated"},
        ],
        "examples": {
            "good": """Identified: causal overclaim ('causes' from correlation), scope overclaim ('nationwide' from 5 hospitals), measurement overclaim (observed behavior claimed as preferences). Revisions appropriately hedged: 'is associated with', 'at studied sites', 'workers engaged in'.""",
            "weak": """Missed obvious causal overclaim. Flagged appropriate hedged claims as overclaims. Suggested revisions still contain overclaims (changed 'proves' to 'strongly proves').""",
        }
    },
}


def build_evaluation_prompt(domain: str, submission: str, baseline: str, level: int) -> str:
    """Build the evaluation prompt with rubric and examples."""

    rubric = DOMAIN_RUBRICS.get(domain, DOMAIN_RUBRICS["domain-1"])

    criteria_text = "\n".join([
        f"  - {c['name']} ({c['max_points']} pts): {c['description']}"
        for c in rubric["criteria"]
    ])

    special_rules = ""
    if "special_rules" in rubric:
        special_rules = "\n\nSPECIAL RULES:\n" + "\n".join(f"- {r}" for r in rubric["special_rules"])

    examples = rubric.get("examples", {})
    example_text = ""
    if examples:
        example_text = f"""

CALIBRATION EXAMPLES:

Strong work looks like:
{examples.get('good', 'N/A')}

Weak work looks like:
{examples.get('weak', 'N/A')}"""

    level_instruction = ""
    if level == 2:
        level_instruction = "This is Level 2 (learning). Provide detailed feedback to help the student improve."
    else:
        level_instruction = "This is Level 3 (final). Be rigorous. Student must demonstrate competence."

    prompt = f"""Evaluate this {rubric['name']} submission.

{level_instruction}

RUBRIC CRITERIA:
{criteria_text}{special_rules}{example_text}

EXPERT BASELINE:
{baseline}

STUDENT SUBMISSION:
{submission}

Respond with JSON matching this exact schema:
{{
  "criteria": {{
    "<criterion_name>": {{
      "score": <0 to max_points>,
      "max": <max_points>,
      "evidence": "<quote or specific reference from student work>",
      "feedback": "<what they did well or missed>"
    }}
  }},
  "total_score": <sum of all criteria scores>,
  "passed": <true if total >= 70 and no criterion below 50% of its max>,
  "summary": "<2-3 sentence overall assessment>",
  "disconfirm_check": <true/false, only for domain-3>
}}

IMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation outside the JSON."""

    return prompt


def load_expert_baseline() -> str:
    """Load the expert baseline document."""
    if BASELINE_PATH.exists():
        return BASELINE_PATH.read_text()
    return "(No expert baseline available)"


def evaluate_with_claude(domain: str, submission_text: str, level: int) -> dict:
    """Use Claude to evaluate student submission against expert baseline."""

    baseline = load_expert_baseline()
    prompt = build_evaluation_prompt(domain, submission_text, baseline, level)

    try:
        if HAS_ANTHROPIC:
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=EVALUATION_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            evaluation_text = response.content[0].text
        else:
            # Fall back to subprocess call
            full_prompt = EVALUATION_SYSTEM_PROMPT + "\n\n" + prompt
            result = subprocess.run(
                ["claude", "-p", full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            evaluation_text = result.stdout

        # Parse JSON response
        # Handle potential markdown code blocks
        if "```json" in evaluation_text:
            evaluation_text = evaluation_text.split("```json")[1].split("```")[0]
        elif "```" in evaluation_text:
            evaluation_text = evaluation_text.split("```")[1].split("```")[0]

        evaluation_text = evaluation_text.strip()

        try:
            parsed = json.loads(evaluation_text)

            # Validate and normalize
            result = {
                "raw_evaluation": evaluation_text,
                "total_score": parsed.get("total_score", 0),
                "passed": parsed.get("passed", False),
                "criteria": parsed.get("criteria", {}),
                "summary": parsed.get("summary", ""),
            }

            # Handle domain-3 special rule
            if domain == "domain-3":
                result["disconfirm_passed"] = parsed.get("disconfirm_check", True)

            # Validate pass criteria
            if result["total_score"] < 70:
                result["passed"] = False

            # Check no criterion below 50%
            for criterion_name, criterion_data in result["criteria"].items():
                if isinstance(criterion_data, dict):
                    score = criterion_data.get("score", 0)
                    max_score = criterion_data.get("max", 100)
                    if max_score > 0 and (score / max_score) < 0.5:
                        result["passed"] = False
                        result["failed_criterion"] = criterion_name
                        break

            return result

        except json.JSONDecodeError as e:
            # Fallback to regex parsing if JSON fails
            return parse_evaluation_fallback(evaluation_text, domain)

    except Exception as e:
        return {
            "error": str(e),
            "raw_evaluation": "",
            "total_score": 0,
            "passed": False,
        }


def parse_evaluation_fallback(text: str, domain: str) -> dict:
    """Fallback parser if JSON parsing fails."""
    result = {
        "raw_evaluation": text,
        "total_score": 0,
        "passed": False,
        "criteria": {},
        "parse_method": "fallback_regex"
    }

    # Try to extract score
    for line in text.split("\n"):
        line_lower = line.lower()
        if "total_score" in line_lower or "total:" in line_lower:
            try:
                # Look for numbers
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    result["total_score"] = int(numbers[0])
            except:
                pass
        if "passed" in line_lower:
            result["passed"] = "true" in line_lower or "yes" in line_lower
        if "disconfirm" in line_lower:
            result["disconfirm_passed"] = "true" in line_lower or "pass" in line_lower

    return result


def evaluate_submission(domain: str, level: int, submission_path: Path) -> dict:
    """Main evaluation function."""

    if not submission_path.exists():
        return {"error": f"File not found: {submission_path}"}

    submission_text = submission_path.read_text()

    print(f"\n🔍 Evaluating {domain} Level {level} submission...")
    print(f"   File: {submission_path}")
    print(f"   Size: {len(submission_text)} characters")

    # Run evaluation
    result = evaluate_with_claude(domain, submission_text, level)

    # Apply level-specific rules
    if level == 3 and result.get("failed_criterion"):
        result["reason"] = f"Criterion '{result['failed_criterion']}' below 50%"

    # Domain-3 special rule: must pass disconfirm check
    if domain == "domain-3" and not result.get("disconfirm_passed", True):
        result["passed"] = False
        result["reason"] = "Failed disconfirming evidence requirement (must find ≥50%)"

    return result


def generate_feedback(evaluation: dict, domain: str, level: int) -> str:
    """Generate formatted feedback from evaluation."""

    feedback = []
    feedback.append(f"\n{'='*60}")
    feedback.append(f"EVALUATION RESULTS: {DOMAIN_NAMES.get(domain, domain).upper()} LEVEL {level}")
    feedback.append(f"{'='*60}\n")

    feedback.append(f"Score: {evaluation.get('total_score', 'N/A')}/100")
    feedback.append(f"Status: {'✅ PASSED' if evaluation.get('passed') else '❌ NOT YET'}\n")

    # Show summary
    if evaluation.get("summary"):
        feedback.append(f"Summary: {evaluation['summary']}\n")

    # Show reason for failure if any
    if evaluation.get("reason"):
        feedback.append(f"⚠️  {evaluation['reason']}\n")

    if level == 2:
        feedback.append("--- Detailed Feedback ---\n")

        # Show criteria breakdown
        criteria = evaluation.get("criteria", {})
        if criteria:
            for name, data in criteria.items():
                if isinstance(data, dict):
                    score = data.get("score", "?")
                    max_score = data.get("max", "?")
                    feedback.append(f"\n{name}: {score}/{max_score}")
                    if data.get("evidence"):
                        feedback.append(f"  Evidence: {data['evidence'][:200]}...")
                    if data.get("feedback"):
                        feedback.append(f"  Feedback: {data['feedback']}")
        else:
            # Fallback to raw evaluation
            feedback.append(evaluation.get("raw_evaluation", ""))

        feedback.append("\n--- Next Steps ---")
        if evaluation.get("passed"):
            feedback.append("You've passed Level 2! You can now attempt Level 3.")
            feedback.append(f"Run: skillforge submit {domain} --level 3 --file <your-work.md>")
        else:
            feedback.append("Review the feedback above and try again in 7 days.")
            feedback.append("Focus on the criteria where you scored lowest.")
    else:  # Level 3
        if evaluation.get("passed"):
            feedback.append(f"\n🎓 Congratulations! You've achieved Level 3 competency in {DOMAIN_NAMES.get(domain, domain)}!")
        else:
            feedback.append("\nNot yet at Level 3. You can retry in 30 days.")
            feedback.append("Consider reviewing Level 2 materials before your next attempt.")

    return "\n".join(feedback)


def save_evaluation_record(
    domain: str,
    level: int,
    submission_path: Path,
    evaluation: dict,
    student_record: dict
) -> None:
    """Save evaluation to student record."""

    eval_record = {
        "domain": domain,
        "level": level,
        "date": datetime.now().isoformat(),
        "submission_file": str(submission_path),
        "score": evaluation.get("total_score", 0),
        "passed": evaluation.get("passed", False),
    }

    # Add to attempts
    if domain not in student_record.get("domains", {}):
        student_record["domains"][domain] = {"level": 0, "attempts": []}

    student_record["domains"][domain]["attempts"].append(eval_record)

    # Update level if passed
    if evaluation.get("passed"):
        current = student_record["domains"][domain].get("level", 0)
        student_record["domains"][domain]["level"] = max(current, level)

    # Save
    record_path = SKILLFORGE_HOME / "record.json"
    record_path.write_text(json.dumps(student_record, indent=2))

    # Also save detailed evaluation
    evals_dir = SKILLFORGE_HOME / "evaluations"
    evals_dir.mkdir(parents=True, exist_ok=True)

    eval_id = f"{domain}-L{level}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    eval_path = evals_dir / f"{eval_id}.json"

    full_eval = {
        **eval_record,
        "evaluation_id": eval_id,
        "criteria": evaluation.get("criteria", {}),
        "summary": evaluation.get("summary", ""),
        "raw_evaluation": evaluation.get("raw_evaluation", ""),
    }
    eval_path.write_text(json.dumps(full_eval, indent=2))


def check_cooldown(domain: str, level: int, student_record: dict) -> Optional[str]:
    """Check if student is in cooldown period."""

    attempts = student_record.get("domains", {}).get(domain, {}).get("attempts", [])

    # Filter to same level, failed attempts
    relevant = [a for a in attempts if a.get("level") == level and not a.get("passed")]

    if not relevant:
        return None

    last_attempt = relevant[-1]
    last_date = datetime.fromisoformat(last_attempt["date"])

    cooldown_days = 7 if level == 2 else 30
    days_since = (datetime.now() - last_date).days

    if days_since < cooldown_days:
        remaining = cooldown_days - days_since
        return f"Cooldown active. You can retry in {remaining} days."

    return None


# CLI interface
def main():
    """CLI for evaluation engine."""
    import argparse

    parser = argparse.ArgumentParser(description="SkillForge Evaluation Engine")
    parser.add_argument("domain", help="Domain to evaluate (e.g., domain-3)")
    parser.add_argument("--level", "-l", type=int, required=True, help="Level (2 or 3)")
    parser.add_argument("--file", "-f", required=True, help="Submission file")
    parser.add_argument("--skip-cooldown", action="store_true", help="Skip cooldown check (testing)")

    args = parser.parse_args()

    # Load student record
    record_path = SKILLFORGE_HOME / "record.json"
    if not record_path.exists():
        print("Not initialized. Run 'skillforge init' first.")
        return 1

    student_record = json.loads(record_path.read_text())

    # Check cooldown
    if not args.skip_cooldown:
        cooldown_msg = check_cooldown(args.domain, args.level, student_record)
        if cooldown_msg:
            print(f"⏳ {cooldown_msg}")
            return 1

    # Run evaluation
    submission_path = Path(args.file)
    evaluation = evaluate_submission(args.domain, args.level, submission_path)

    if "error" in evaluation:
        print(f"❌ Error: {evaluation['error']}")
        return 1

    # Generate and display feedback
    feedback = generate_feedback(evaluation, args.domain, args.level)
    print(feedback)

    # Save record
    save_evaluation_record(
        args.domain,
        args.level,
        submission_path,
        evaluation,
        student_record
    )

    print(f"\n📁 Evaluation saved to ~/.skillforge/evaluations/")

    return 0 if evaluation.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
