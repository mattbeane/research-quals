#!/usr/bin/env python3
"""
SkillForge CLI - Competency-based training for mixed-methods management research

Commands:
    status      Show your current competency status
    take        Take a Level 1 assessment
    submit      Submit Level 2-3 work for evaluation
    init        Initialize student profile
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuration
SKILLFORGE_HOME = Path.home() / ".skillforge"
ASSESSMENTS_DIR = Path(__file__).parent.parent / "assessments"

DOMAINS = {
    "domain-1": "Pattern Recognition",
    "domain-2": "Theoretical Positioning",
    "domain-3": "Qualitative Mechanism",
    "domain-4": "Theoretical Framing",
    "domain-5": "Epistemological Genre",
    "domain-6": "Adversarial Evidence",
    "domain-7": "Claim Verification",
}

DOMAIN_QUESTIONS = {
    "domain-1": "Is this signal or noise?",
    "domain-2": "What makes this a contribution?",
    "domain-3": "What's actually happening here?",
    "domain-4": "How do I position this for reviewers?",
    "domain-5": "Am I discovering or testing?",
    "domain-6": "What challenges my interpretation?",
    "domain-7": "Does my evidence support my claims?",
}

# Progression rules
LEVEL_PREREQS = {
    # level 2 requires level 1 in same domain
    # level 3 requires level 2 in same domain
}

DOMAIN_PREREQS = {
    # Some domains require others first
    "domain-2": ["domain-1"],
    "domain-4": ["domain-3"],
    "domain-5": ["domain-4"],
    "domain-6": ["domain-5"],
    "domain-7": ["domain-6"],
}


def get_student_record() -> dict:
    """Load or create student record."""
    record_path = SKILLFORGE_HOME / "record.json"
    if record_path.exists():
        return json.loads(record_path.read_text())
    return {
        "student_id": None,
        "created": None,
        "domains": {},
        "attempts": [],
    }


def save_student_record(record: dict):
    """Save student record."""
    SKILLFORGE_HOME.mkdir(parents=True, exist_ok=True)
    record_path = SKILLFORGE_HOME / "record.json"
    record_path.write_text(json.dumps(record, indent=2))


def cmd_init(args):
    """Initialize student profile."""
    record = get_student_record()

    if record["student_id"]:
        print(f"Already initialized as: {record['student_id']}")
        if not args.force:
            print("Use --force to reinitialize (warning: clears progress)")
            return 1
        print("Reinitializing...")
        record = {"domains": {}, "attempts": []}

    # Get student info
    if args.name:
        name = args.name
    else:
        name = input("Your name: ").strip()

    if args.email:
        email = args.email
    else:
        email = input("Your email: ").strip()

    record["student_id"] = email.split("@")[0]
    record["name"] = name
    record["email"] = email
    record["created"] = datetime.now().isoformat()
    record["domains"] = {d: {"level": 0, "attempts": []} for d in DOMAINS}
    record["attempts"] = []

    save_student_record(record)
    print(f"\n✅ Initialized SkillForge profile for {name}")
    print(f"   Student ID: {record['student_id']}")
    print(f"\nRun 'skillforge status' to see your competency map.")
    return 0


def cmd_status(args):
    """Show competency status."""
    record = get_student_record()

    if not record["student_id"]:
        print("Not initialized. Run 'skillforge init' first.")
        return 1

    print(f"\n🎓 SkillForge Status: {record.get('name', record['student_id'])}")
    print("=" * 60)

    # Summary stats
    total_l3 = sum(1 for d in record.get("domains", {}).values() if d.get("level", 0) >= 3)
    print(f"\nLevel 3 Competencies: {total_l3}/7")

    # Domain breakdown
    print("\n" + "-" * 60)
    print(f"{'Domain':<35} {'Level':<10} {'Status':<15}")
    print("-" * 60)

    for domain_id, domain_name in DOMAINS.items():
        domain_data = record.get("domains", {}).get(domain_id, {})
        level = domain_data.get("level", 0)

        # Status indicator
        if level >= 3:
            status = "✅ Complete"
            level_str = "L3"
        elif level >= 2:
            status = "🔶 L3 available"
            level_str = "L2"
        elif level >= 1:
            status = "🔶 L2 available"
            level_str = "L1"
        else:
            # Check prereqs
            prereqs = DOMAIN_PREREQS.get(domain_id, [])
            prereqs_met = all(
                record.get("domains", {}).get(p, {}).get("level", 0) >= 1
                for p in prereqs
            )
            if prereqs_met:
                status = "⚪ L1 available"
            else:
                status = f"🔒 Requires {', '.join(prereqs)}"
            level_str = "--"

        question = DOMAIN_QUESTIONS[domain_id]
        print(f"{domain_id}: {domain_name:<24} {level_str:<10} {status}")

    print("-" * 60)

    # Next steps
    print("\n📋 Next Steps:")
    suggested = False
    for domain_id in DOMAINS:
        domain_data = record.get("domains", {}).get(domain_id, {})
        level = domain_data.get("level", 0)
        prereqs = DOMAIN_PREREQS.get(domain_id, [])
        prereqs_met = all(
            record.get("domains", {}).get(p, {}).get("level", 0) >= 1
            for p in prereqs
        )

        if level < 3 and prereqs_met:
            next_level = level + 1
            if next_level == 1:
                print(f"   skillforge take {domain_id} --level 1")
            elif next_level == 2:
                print(f"   skillforge take {domain_id} --level 2")
            else:
                print(f"   skillforge submit {domain_id} --level 3")
            suggested = True
            if suggested and level == 0:
                break  # Only show first available domain for beginners

    if not suggested:
        print("   🎉 All domains complete! You're ready for independent research.")

    print()
    return 0


def load_assessment(domain: str, level: int) -> Optional[dict]:
    """Load assessment questions from markdown file."""
    # Map level 1 files
    level_1_files = {
        "domain-1": "level-1-domain-1-pattern-recognition.md",
        "domain-2": "level-1-domain-2-theoretical-positioning.md",
        "domain-3": "level-1-domain-3-qualitative-mechanism.md",
        "domain-4": "level-1-domain-4-theoretical-framing.md",
        "domain-5": "level-1-domain-5-epistemological-genre.md",
        "domain-6": "level-1-domain-6-adversarial-evidence.md",
        "domain-7": "level-1-domain-7-claim-verification.md",
    }

    if level == 1 and domain in level_1_files:
        file_path = ASSESSMENTS_DIR / level_1_files[domain]
        if file_path.exists():
            return parse_assessment_md(file_path)

    return None


def parse_assessment_md(file_path: Path) -> dict:
    """Parse assessment markdown into structured questions."""
    content = file_path.read_text()

    questions = []
    current_q = None
    in_options = False
    correct_answer = None
    why_text = None
    model_answer = []
    in_model_answer = False

    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # Start of new question
        if line.startswith("### Question "):
            if current_q:
                # Save previous question
                if current_q.get("type") == "mc":
                    current_q["correct"] = correct_answer
                    current_q["explanation"] = why_text
                elif current_q.get("type") == "short":
                    current_q["model_answer"] = "\n".join(model_answer)
                questions.append(current_q)

            q_num = int(line.replace("### Question ", "").strip())
            # Read next line for question text
            i += 1
            q_text = ""
            while i < len(lines) and not lines[i].startswith("- ") and not lines[i].startswith("**"):
                if lines[i].strip():
                    q_text += lines[i] + " "
                i += 1

            current_q = {
                "number": q_num,
                "question": q_text.strip(),
                "options": [],
                "type": "mc",  # default, will change if short answer
            }
            correct_answer = None
            why_text = None
            model_answer = []
            in_model_answer = False
            in_options = True
            continue

        # Options for MC
        if in_options and line.startswith("- "):
            option = line[2:].strip()
            # Parse "a) text" format
            if len(option) >= 3 and option[1] == ")":
                letter = option[0].lower()
                text = option[3:].strip()
                current_q["options"].append({"letter": letter, "text": text})

        # Correct answer
        if line.startswith("**Correct**:"):
            correct_answer = line.replace("**Correct**:", "").strip().lower()
            in_options = False

        # Explanation
        if line.startswith("**Why**:"):
            why_text = line.replace("**Why**:", "").strip()

        # Short answer detection
        if "**Model answer should include**:" in line or "**Model answer should include any" in line:
            current_q["type"] = "short"
            in_model_answer = True
            in_options = False

        # Collect model answer bullets
        if in_model_answer and line.startswith("- "):
            model_answer.append(line[2:].strip())

        i += 1

    # Don't forget last question
    if current_q:
        if current_q.get("type") == "mc":
            current_q["correct"] = correct_answer
            current_q["explanation"] = why_text
        elif current_q.get("type") == "short":
            current_q["model_answer"] = "\n".join(model_answer)
        questions.append(current_q)

    # Extract metadata
    time_limit = "30-45 minutes"
    passing = "80%"

    for line in lines[:30]:
        if "**Time**:" in line:
            time_limit = line.split("**Time**:")[1].strip()
        if "**Passing**:" in line:
            passing = line.split("**Passing**:")[1].strip()

    return {
        "file": str(file_path),
        "time_limit": time_limit,
        "passing": passing,
        "questions": questions,
    }


def run_level1_assessment(assessment: dict, domain: str) -> tuple[int, int, list]:
    """Run interactive Level 1 assessment. Returns (score, total, responses)."""
    import random

    questions = assessment["questions"]
    mc_questions = [q for q in questions if q["type"] == "mc"]
    short_questions = [q for q in questions if q["type"] == "short"]

    # Randomize question order (keep MC before short answer)
    random.shuffle(mc_questions)
    random.shuffle(short_questions)

    # Randomize option order within each MC question
    for q in mc_questions:
        if q.get("options"):
            # Store correct answer text before shuffling
            correct_letter = q.get("correct", "")
            correct_text = None
            for opt in q["options"]:
                if opt["letter"] == correct_letter:
                    correct_text = opt["text"]
                    break

            # Shuffle options
            random.shuffle(q["options"])

            # Reassign letters a, b, c, d and update correct answer
            for i, opt in enumerate(q["options"]):
                new_letter = chr(ord('a') + i)
                if opt["text"] == correct_text:
                    q["correct"] = new_letter
                opt["letter"] = new_letter

    print(f"\n📝 Level 1 Assessment: {DOMAINS[domain]}")
    print("=" * 60)
    print(f"Time: {assessment['time_limit']}")
    print(f"Passing: {assessment['passing']}")
    print(f"Questions: {len(mc_questions)} multiple choice + {len(short_questions)} short answer")
    print("=" * 60)

    input("\nPress Enter to begin...")

    responses = []
    mc_correct = 0

    # Multiple choice section
    print("\n--- Section A: Multiple Choice ---\n")

    for q in mc_questions:
        print(f"\nQuestion {q['number']}:")
        print(q["question"])
        print()
        for opt in q["options"]:
            print(f"  {opt['letter']}) {opt['text']}")

        while True:
            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            if answer in ["a", "b", "c", "d"]:
                break
            print("Please enter a, b, c, or d")

        is_correct = answer == q["correct"]
        if is_correct:
            mc_correct += 1

        responses.append({
            "question": q["number"],
            "type": "mc",
            "answer": answer,
            "correct": q["correct"],
            "is_correct": is_correct,
        })

    # Short answer section
    print("\n--- Section B: Short Answer ---\n")

    for q in short_questions:
        print(f"\nQuestion {q['number']}:")
        print(q["question"])
        print("\n(Type your answer, then press Enter twice to submit)")

        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)

        answer = "\n".join(lines[:-1] if lines and lines[-1] == "" else lines)

        responses.append({
            "question": q["number"],
            "type": "short",
            "answer": answer,
            "model_answer": q.get("model_answer", ""),
        })

    # Calculate score
    mc_total = len(mc_questions)
    short_total = len(short_questions) * 2  # 2 points each

    print("\n" + "=" * 60)
    print("Assessment Complete!")
    print("=" * 60)

    # Show MC results immediately
    print(f"\nMultiple Choice: {mc_correct}/{mc_total}")

    # Score short answers with LLM
    print(f"\nShort Answer: Scoring {len(short_questions)} questions...")

    short_score = 0
    for resp in responses:
        if resp["type"] == "short":
            print(f"\nScoring Question {resp['question']}...")
            score, feedback = score_short_answer(
                resp["question"],
                resp["answer"],
                resp["model_answer"],
                domain
            )
            short_score += score
            resp["llm_score"] = score
            resp["llm_feedback"] = feedback

            print(f"  Score: {score}/2")
            print(f"  Feedback: {feedback}")

    total_score = mc_correct + short_score
    total_possible = mc_total + short_total
    percentage = (total_score / total_possible) * 100

    return total_score, total_possible, responses, percentage


def score_short_answer(question_num: int, student_answer: str, model_answer: str, domain: str) -> tuple[int, str]:
    """Use LLM to score a short answer question. Returns (score 0-2, feedback)."""

    if not student_answer.strip():
        return 0, "No answer provided."

    prompt = f"""You are scoring a short answer question for a PhD research methods assessment.

Domain: {DOMAINS.get(domain, domain)}

Question {question_num}

Student's answer:
{student_answer}

Model answer should include:
{model_answer}

Score this answer 0, 1, or 2 points:
- 0 points: Missing key concepts, fundamentally wrong, or no meaningful attempt
- 1 point: Partial understanding, got some key points but missed important ones
- 2 points: Demonstrates clear understanding, hits most key points from model answer

Respond in exactly this format:
SCORE: [0, 1, or 2]
FEEDBACK: [One sentence explaining the score]
"""

    try:
        # Try anthropic SDK first
        try:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            result_text = response.content[0].text
        except ImportError:
            # Fall back to subprocess
            import subprocess
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            result_text = result.stdout

        # Parse response
        score = 1  # Default to partial credit
        feedback = "Unable to parse feedback."

        for line in result_text.split("\n"):
            if line.startswith("SCORE:"):
                try:
                    score = int(line.split(":")[1].strip())
                    score = max(0, min(2, score))  # Clamp to 0-2
                except:
                    pass
            if line.startswith("FEEDBACK:"):
                feedback = line.split(":", 1)[1].strip()

        return score, feedback

    except Exception as e:
        # If LLM fails, fall back to self-assessment
        print(f"  (LLM scoring unavailable: {e})")
        print(f"  Your answer: {student_answer[:150]}...")
        print(f"  Model answer includes: {model_answer[:150]}...")
        while True:
            self_score = input("  Self-assess (0/1/2): ").strip()
            if self_score in ["0", "1", "2"]:
                return int(self_score), "Self-assessed"
        return 1, "Scoring unavailable, default partial credit"


def cmd_take(args):
    """Take an assessment."""
    record = get_student_record()

    if not record["student_id"]:
        print("Not initialized. Run 'skillforge init' first.")
        return 1

    domain = args.domain
    level = args.level

    # Validate domain
    if domain not in DOMAINS:
        print(f"Unknown domain: {domain}")
        print(f"Valid domains: {', '.join(DOMAINS.keys())}")
        return 1

    # Check prerequisites
    prereqs = DOMAIN_PREREQS.get(domain, [])
    for prereq in prereqs:
        prereq_level = record.get("domains", {}).get(prereq, {}).get("level", 0)
        if prereq_level < 1:
            print(f"🔒 {domain} requires {prereq} Level 1 first.")
            print(f"   Run: skillforge take {prereq} --level 1")
            return 1

    current_level = record.get("domains", {}).get(domain, {}).get("level", 0)
    if level > current_level + 1:
        print(f"🔒 You must pass Level {current_level + 1} before Level {level}")
        return 1

    # Load assessment
    assessment = load_assessment(domain, level)
    if not assessment:
        print(f"❌ No assessment available for {domain} Level {level}")
        print("   Available Level 1 assessments: all domains (domain-1 through domain-7)")
        print("   Level 2-3: Use 'skillforge submit' with your work file")
        return 1

    # Run the assessment
    if level == 1:
        score, total, responses, percentage = run_level1_assessment(assessment, domain)

        passed = percentage >= 80

        print("\n" + "=" * 60)
        print(f"Final Score: {score}/{total} ({percentage:.0f}%)")
        print(f"Required: 80%")

        if passed:
            print("\n✅ PASSED!")
            # Update record
            if domain not in record["domains"]:
                record["domains"][domain] = {"level": 0, "attempts": []}
            record["domains"][domain]["level"] = max(record["domains"][domain]["level"], 1)
            record["domains"][domain]["attempts"].append({
                "level": 1,
                "date": datetime.now().isoformat(),
                "score": score,
                "total": total,
                "percentage": percentage,
                "passed": True,
            })
            save_student_record(record)
            print(f"\n{DOMAINS[domain]} Level 1 complete!")
            print(f"Run 'skillforge status' to see your updated progress.")
        else:
            print("\n❌ Not yet. Review the material and try again.")
            record["attempts"].append({
                "domain": domain,
                "level": 1,
                "date": datetime.now().isoformat(),
                "score": score,
                "total": total,
                "percentage": percentage,
                "passed": False,
            })
            save_student_record(record)
    else:
        print(f"Level {level} assessments require file submission.")
        print(f"Run: skillforge submit {domain} --level {level} --file your_work.md")

    return 0


def cmd_submit(args):
    """Submit work for Level 2-3 evaluation."""
    record = get_student_record()

    if not record["student_id"]:
        print("Not initialized. Run 'skillforge init' first.")
        return 1

    domain = args.domain
    level = args.level
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 1

    # Validate domain
    if domain not in DOMAINS:
        print(f"Unknown domain: {domain}")
        print(f"Valid domains: {', '.join(DOMAINS.keys())}")
        return 1

    # Check prerequisites - must have passed previous level
    current_level = record.get("domains", {}).get(domain, {}).get("level", 0)
    if level > current_level + 1:
        print(f"🔒 You must pass Level {current_level + 1} before Level {level}")
        return 1

    # Level 2+ requires Level 1 first
    if level >= 2 and current_level < 1:
        print(f"🔒 You must pass Level 1 before Level {level}")
        print(f"   Run: skillforge take {domain} --level 1")
        return 1

    # Import evaluator
    try:
        from . import evaluator
    except ImportError:
        # Running as script
        import evaluator

    # Check cooldown
    cooldown_msg = evaluator.check_cooldown(domain, level, record)
    if cooldown_msg:
        print(f"⏳ {cooldown_msg}")
        return 1

    # Run evaluation
    print(f"\n🔍 Evaluating {DOMAINS[domain]} Level {level}...")
    print(f"   File: {file_path}")

    evaluation = evaluator.evaluate_submission(domain, level, file_path)

    if "error" in evaluation:
        print(f"❌ Error: {evaluation['error']}")
        return 1

    # Generate and display feedback
    feedback = evaluator.generate_feedback(evaluation, domain, level)
    print(feedback)

    # Save record
    evaluator.save_evaluation_record(domain, level, file_path, evaluation, record)

    print(f"\n📁 Evaluation saved to ~/.skillforge/evaluations/")

    # Update status message
    if evaluation.get("passed"):
        record = get_student_record()  # Reload after save
        if level == 2:
            print(f"\nNext: skillforge submit {domain} --level 3 --file <your-work.md>")
        else:
            print(f"\n🎓 {DOMAINS[domain]} complete!")

    return 0 if evaluation.get("passed") else 1


def main():
    parser = argparse.ArgumentParser(
        description="SkillForge - Competency-based training for mixed-methods research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    skillforge init                     Initialize your profile
    skillforge status                   See your competency map
    skillforge take domain-1 --level 1  Take Pattern Recognition L1
    skillforge submit domain-3 --level 2 --file my-coding.md
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize student profile")
    init_parser.add_argument("--name", help="Your name")
    init_parser.add_argument("--email", help="Your email")
    init_parser.add_argument("--force", action="store_true", help="Reinitialize (clears progress)")

    # status
    status_parser = subparsers.add_parser("status", help="Show competency status")

    # take
    take_parser = subparsers.add_parser("take", help="Take an assessment")
    take_parser.add_argument("domain", help="Domain to assess (e.g., domain-1)")
    take_parser.add_argument("--level", "-l", type=int, default=1, help="Level (1, 2, or 3)")

    # submit
    submit_parser = subparsers.add_parser("submit", help="Submit work for evaluation")
    submit_parser.add_argument("domain", help="Domain (e.g., domain-3)")
    submit_parser.add_argument("--level", "-l", type=int, required=True, help="Level (2 or 3)")
    submit_parser.add_argument("--file", "-f", required=True, help="File to submit")

    args = parser.parse_args()

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "take":
        return cmd_take(args)
    elif args.command == "submit":
        return cmd_submit(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
