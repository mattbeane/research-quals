# Assessment Specifications

## The Problem With My Original Design

I wrote 400-line competency documents but never specified:
- How to actually score assessments
- What datasets to use
- What "overlap with expert" means operationally

This document fixes that.

---

## Scoring Rubrics

### Level 1: Knowledge Recognition (All Domains)

**Format**: 10-15 multiple choice + 2-3 short answer
**Time**: 30-45 minutes
**Passing**: ≥80% (no partial credit on MC)
**Retake**: Immediately, unlimited attempts

**Scoring is binary**: Right or wrong answers with answer key.

---

### Level 2: Application with Feedback (All Domains)

**Format**: Apply concepts to provided materials
**Time**: 2-4 hours
**Passing**: ≥70/100 on rubric
**Retake**: After reviewing feedback, 7-day cooldown

**Scoring rubric template**:

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| Found target patterns/evidence | 30 | Count: (found ∩ expected) / expected |
| Avoided false positives | 20 | Count: (found - expected) / found → penalize |
| Reasoning quality | 30 | Holistic: 0-10 scale × 3 |
| Completeness | 20 | Did they do all parts? Binary per part |

---

### Level 3: Authentic Performance (All Domains)

**Format**: Independent work on novel materials
**Time**: 4-8 hours (varies by domain)
**Passing**: ≥70/100 AND no criterion below 50%
**Retake**: 30-day cooldown (one attempt per month)

**Scoring**: Same rubric as Level 2, but:
- No feedback during assessment
- Stricter floor requirements
- Single attempt enforced

---

## Domain-Specific Scoring

### Domain 1: Pattern Recognition

**Expert baseline**: Matt identifies top 5 patterns in dataset, rates each 1-5 on interest.

**Scoring**:
- Student identifies same patterns: +6 points each (max 30)
- Student identifies pattern Matt rated 1-2: +2 points each
- Student pursues pattern Matt would kill: -5 points each
- Robustness instinct demonstrated: +20 (holistic)
- Heterogeneity explored: +10
- Killed findings documented: +10

### Domain 3: Qualitative Mechanism Extraction

**CRITICAL: This is the hardest to score objectively**

**Expert baseline**: Matt codes 10 interviews, identifies:
- Top 3 mechanisms with quote IDs
- Disconfirming evidence (quote IDs)
- Unexpected themes

**Scoring**:

```
Mechanism overlap = |student_mechanisms ∩ expert_mechanisms| / |expert_mechanisms|
Quote overlap = |student_quotes ∩ expert_quotes| / |expert_quotes|
Disconfirm found = |student_disconfirm ∩ expert_disconfirm| / |expert_disconfirm|

Score = (mechanism_overlap × 30) + (quote_overlap × 25) + (disconfirm_found × 30) + (holistic × 15)
```

**Minimum bar**: Must find ≥50% of disconfirming evidence. Zero tolerance for cherry-picking.

### Domain 4: Theoretical Framing

**Scoring uses Zuckerman rubric-eval**:

```bash
rubric-eval eval student_framing.md rubrics/zuckerman.json \
  --runs 5 --model haiku
```

Each of 10 criteria scored 1-5. Pass requires:
- Total ≥35/50
- No criterion below 2/5
- Generated ≥3 distinct framings

### Domain 7: Claim Verification

**Expert baseline**: Matt identifies all overclaims in test paper.

**Scoring**:
```
Overclaims found = |student ∩ expert| / |expert|
False positives = |student - expert| / |student|
Calibration quality = holistic assessment of revisions

Score = (found × 40) - (false_pos × 20) + (calibration × 40)
```

---

## Assessment Materials Needed

### Priority 1: Create These First

| Domain | Materials | Source | Prep Time |
|--------|-----------|--------|-----------|
| D1 | Quantitative dataset + expert pattern list | Company X (anonymized) | 4-6 hours |
| D3 | 10 interview transcripts + expert coding | Company Y (anonymized) | 8-12 hours |
| D7 | Paper draft with seeded overclaims | Create synthetic | 2-3 hours |

### Priority 2: Create After Pilot

| Domain | Materials | Source | Prep Time |
|--------|-----------|--------|-----------|
| D2 | Finding + expert theoretical positioning | From D1 output | 2-3 hours |
| D4 | Evidence package + expert framings | From D3 output | 4-6 hours |
| D5 | Draft with genre violations + expert revision | Create synthetic | 3-4 hours |
| D6 | Paper + data + expert audit | From prior | 4-6 hours |

---

## Advisor Certification Protocol

When an advisor certifies competence without full assessment:

**Required**:
1. Advisor reviews student's prior work demonstrating competence
2. Advisor signs certification form with:
   - Domain and level being certified
   - Evidence reviewed (paper title, course, etc.)
   - Attestation: "I have reviewed [evidence] and certify that [student] demonstrates competence in [domain] at Level [N]"
3. Certification logged to student record with advisor ID and date

**Audit trail**:
```json
{
  "type": "advisor_certification",
  "domain": "domain-3",
  "level": 3,
  "advisor": "Prof. Beane",
  "advisor_id": "mbeane",
  "date": "2025-02-02",
  "evidence": "Prior qual methods course at Stanford (TM 502), A grade",
  "attestation_signed": true
}
```

**Limits**:
- Advisor can certify max 3 domains per student (prevents blanket exemption)
- Domains 6-7 cannot be certified (must demonstrate adversarial + verification skills)

---

## Integration With TheoryForge

### Check Function (to add to TheoryForge)

```python
# theory-forge/lib/competency_gate.py

import json
from pathlib import Path

UNLOCK_MAP = {
    "hunt-patterns": {"domain-1": 3},
    "find-theory": {"domain-1": 3, "domain-2": 3},
    "mine-qual": {"domain-2": 3, "domain-3": 3},
    "smith-frames": {"domain-3": 3, "domain-4": 3},
    "eval-zuckerman": {"domain-3": 3, "domain-4": 3},
    "eval-genre": {"domain-4": 3, "domain-5": 3},
    "draft-paper": {"domain-4": 3, "domain-5": 3},
    "audit-claims": {"domain-5": 3, "domain-6": 3},
    "verify-claims": {"domain-5": 3, "domain-6": 3},
    "package-verification": {"domain-6": 3, "domain-7": 3},
}

def check_competency(command: str, student_id: str = None) -> tuple[bool, str]:
    """
    Check if student can run this command.
    Returns (allowed, message).
    """
    if command not in UNLOCK_MAP:
        return True, ""  # Ungated command

    # Find student record
    if not student_id:
        id_file = Path.home() / ".researchkit-quals" / "student-id"
        if not id_file.exists():
            return True, ""  # No quals system configured
        student_id = id_file.read_text().strip()

    record_path = Path.home() / ".researchkit-quals" / student_id / "unlock-status.json"
    if not record_path.exists():
        return True, ""  # No record = no restrictions (faculty/expert mode)

    record = json.loads(record_path.read_text())
    requirements = UNLOCK_MAP[command]

    missing = []
    for domain, level in requirements.items():
        student_level = record.get("domains", {}).get(domain, {}).get("level", 0)
        if student_level < level:
            missing.append(f"{domain} Level {level}")

    if missing:
        msg = f"🔒 /{command} requires: {', '.join(missing)}\n"
        msg += f"Run /quals-status to see your progress."
        return False, msg

    return True, ""
```

### Usage in Command Files

Add to top of each gated command:

```markdown
## Competency Gate

Before running this command, the system checks competency status.

If you see a "🔒 Locked" message, you need to complete the required
assessments first. Run `/quals-status` for details.

Faculty and expert users (no student record) are not gated.
```

---

---

## New Assessment Items (TheoryForge-Aligned)

Based on improvements to TheoryForge, the following supplements have been added:

### Domain 1: Pattern Recognition
- **L2 Supplement**: `tasks/level-2-domain-1-contribution-diagnosis.md`
  - Tests ability to diagnose WHAT TYPE of contribution a pattern supports
  - Not all patterns are "theory violation"—teaches elaboration, phenomenon, methodological, practical

### Domain 4: Theoretical Framing
- **L2 Task**: `tasks/level-2-domain-4-frame-comparison.md`
  - Tests ability to COMPARE and SELECT between frames
  - Emphasizes trade-off identification and justified selection
- **L3 Supplement**: `tasks/level-3-reviewer-anticipation.md`
  - Tests ability to ANTICIPATE hostile, supportive, and confused reviewers
  - Requires simulating 3 reviews and developing defense plan

### Domain 5: Evidence Evaluation
- **L2 Task**: `tasks/level-2-domain-5-quant-qual-integration.md`
  - Tests ability to INTEGRATE quant patterns with qual mechanisms
  - Mapping matrix, convergence/divergence analysis, gap identification

### Domain 7: Execution Discipline
- **L1 Supplement**: `level-1-domain-7-execution-resilience.md`
  - Tests ability to RECOVER from setbacks
  - Scenarios: killed findings, framing failures, getting scooped, advisor pushback

---

## Rationale

These additions address gaps revealed by TheoryForge development:

| TheoryForge Feature | SkillForge Gap | New Assessment |
|---------------------|----------------|----------------|
| `/eval-contribution` | Assumed one contribution type | Contribution diagnosis in D1 |
| `/integrate-quant-qual` | No integration testing | Quant-qual integration in D5 |
| `/compare-frames` | No frame selection testing | Frame comparison in D4 |
| `/simulate-review` | No anticipation testing | Reviewer anticipation in D4 L3 |
| `/repair-state` | No resilience testing | Execution resilience in D7 |

---

## What I Still Haven't Done

1. **Actually create the assessment datasets** - This is real work
2. **Build the quals CLI** - Commands to take/submit assessments
3. **Create the Level 1 question banks** - Multiple choice from competency docs
4. **Set up rubric-eval for D4** - Zuckerman criteria as rubric
5. **Create seed data for new L2 tasks** - Especially for integration and frame comparison

The competency definitions are design docs. The system isn't operational until the above exist.
