# Level 3 Assessments - General Instructions

## What Level 3 Tests

Level 3 is authentic performance: Can you do this independently on novel materials?

- **No feedback during assessment**
- **Single attempt** per 30-day period
- **Evaluated against expert baseline**
- Must score ≥70/100 with no criterion below 50%

---

## How Level 3 Works

### 1. Request Materials

When you're ready for Level 3, request your materials:

```bash
skillforge take domain-X --level 3 --request-materials
```

You'll receive:
- Novel dataset/excerpts (different from Level 2)
- Task instructions
- Submission format

### 2. Complete Independently

You have **1 week** from receiving materials to submit.

**Rules:**
- Work independently
- Do not share materials with others
- Do not use AI assistants to generate your analysis (using them to check grammar is fine)

### 3. Submit

```bash
skillforge submit domain-X --level 3 --file your-submission.md
```

### 4. Receive Results

Your submission is evaluated against the expert baseline.

**If you pass**: Competency recorded. Command unlocks in TheoryForge.

**If you don't pass**: 30-day cooldown before retry. Review your Level 2 feedback.

---

## Level 3 Materials by Domain

### Domain 1: Pattern Recognition
- **Novel dataset**: Different context from Level 2
- **Task**: Identify patterns, document robustness thinking, kill weak findings
- **Time**: 4-6 hours recommended

### Domain 2: Theoretical Positioning
- **Materials**: Finding summary + relevant literature
- **Task**: Position finding in scholarly conversation, generate alternatives, specify contribution
- **Time**: 3-4 hours recommended

### Domain 3: Qualitative Mechanism
- **Novel excerpts**: 15 excerpts from different study
- **Task**: Code, identify mechanisms, report distribution, engage disconfirmation
- **Time**: 4-6 hours recommended

### Domain 4: Theoretical Framing
- **Materials**: Mechanism description + evidence package
- **Task**: Generate 3+ frames, evaluate against Zuckerman criteria, select best
- **Time**: 3-4 hours recommended

### Domain 5: Epistemological Genre
- **Materials**: Draft paper with genre violations
- **Task**: Identify violations, revise claims to match methods
- **Time**: 2-3 hours recommended

### Domain 6: Adversarial Evidence
- **Materials**: Paper draft + underlying data
- **Task**: Audit for missing disconfirmation, identify boundary conditions
- **Time**: 3-4 hours recommended

### Domain 7: Claim Verification
- **Materials**: Paper draft with seeded overclaims
- **Task**: Identify overclaims, suggest calibrated revisions
- **Time**: 2-3 hours recommended

---

## Scoring

Level 3 uses the same rubric as Level 2, but:

1. **Higher stakes**: Must pass all criteria at ≥50%
2. **No feedback**: You won't see detailed breakdown until after scoring
3. **Expert comparison**: Directly compared to what expert found

---

## Advisor Certification

If you have prior demonstrated competence (e.g., published qual paper, completed methods training), your advisor may certify Level 3 without assessment.

**Limits:**
- Max 3 domains can be certified
- Domains 6-7 cannot be certified (must demonstrate)

To request certification:
```bash
skillforge request-certification domain-X --advisor advisor@university.edu
```

---

## FAQ

**Q: Can I retake if I fail?**
A: Yes, after 30 days.

**Q: Can I see what I got wrong?**
A: You'll see your total score and which criterion (if any) fell below 50%.

**Q: What if I run out of time?**
A: Submit what you have. Partial submissions are scored.

**Q: Can I use reference materials?**
A: Yes—your notes, readings, Level 2 feedback. No AI-generated analysis.
