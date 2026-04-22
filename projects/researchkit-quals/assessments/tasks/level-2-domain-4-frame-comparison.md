# Domain 4: Theoretical Framing
## Level 2 Task - Frame Comparison and Selection

**Time**: 3-4 hours
**Passing**: ≥70/100, with detailed feedback
**Retake**: After 7 days

---

## Your Task

You will compare multiple theoretical framings for the same finding and select the strongest one. This task tests your ability to:
1. Generate genuinely different frames (not just rewordings)
2. Evaluate frames against multiple criteria
3. Identify trade-offs between frames
4. Justify your selection with clear reasoning

---

## Materials Provided

You have been given a finding package:

```
seed-data/framing-exercise/
├── FINDING_SUMMARY.md          # The empirical finding to frame
├── QUANT_EVIDENCE.md           # Quantitative support
├── QUAL_EVIDENCE.md            # Qualitative support
├── CANDIDATE_FRAMES.md         # 4 candidate frames to evaluate
└── EXPERT_EVALUATION.md        # [HIDDEN - revealed after submission]
```

The finding involves how workers respond when new technology threatens to automate parts of their work.

---

## Instructions

### Part 1: Understand the Finding (10%)

Read the finding package. Write a 2-3 sentence summary of:
- What the finding IS (descriptively)
- What's surprising or interesting about it
- What you don't yet know (what questions remain)

### Part 2: Evaluate the Candidate Frames (40%)

Four candidate frames are provided. For EACH frame, evaluate against these dimensions:

**Dimension A: Evidence Fit (1-5)**
- Does the evidence actually support this frame?
- Are there significant gaps?

**Dimension B: Theoretical Novelty (1-5)**
- Would this be new to the target literature?
- Has someone already said this?

**Dimension C: Audience Alignment (1-5)**
- Who is the audience (row vs column)?
- Would they find this surprising and important?

**Dimension D: Coherence (1-5)**
- Does the frame hold together logically?
- Are boundary conditions specified?

**Dimension E: Robustness (1-5)**
- Can alternative explanations be ruled out?
- How would this survive hostile review?

**Dimension F: Practical Feasibility (1-5)**
- Can you actually write this paper with available evidence?
- Is the required literature accessible?

### Part 3: Comparative Analysis (25%)

**A. Create a comparison matrix:**

| Dimension | Frame 1 | Frame 2 | Frame 3 | Frame 4 |
|-----------|---------|---------|---------|---------|
| Evidence Fit | | | | |
| Theoretical Novelty | | | | |
| Audience Alignment | | | | |
| Coherence | | | | |
| Robustness | | | | |
| Practical Feasibility | | | | |
| **TOTAL** | | | | |

**B. Identify key trade-offs:**

For any pair of frames where one beats the other on some dimensions but loses on others, describe the trade-off:

Example: "Frame 1 has higher novelty than Frame 2 (it challenges established theory), but Frame 2 has better evidence fit (all subgroups support it). Choosing Frame 1 means accepting thinner evidence for a bigger claim."

Identify at least 3 meaningful trade-offs.

### Part 4: Selection and Justification (25%)

**A. Select your recommended frame.**

**B. Justify your selection (300-400 words):**
- Why this frame over the alternatives?
- What trade-offs are you accepting?
- What would need to be true for a different frame to be better?
- What is the single biggest weakness of your selected frame, and how would you address it?

**C. If you had to pick a SECOND frame (backup), which would it be and why?**

---

## Submission Format

```markdown
# Domain 4 Level 2 Submission: Frame Comparison

## Part 1: Finding Summary

[Your 2-3 sentence summary]

## Part 2: Frame Evaluations

### Frame 1: [Name]
- Evidence Fit: [1-5] - [Brief justification]
- Theoretical Novelty: [1-5] - [Brief justification]
- Audience Alignment: [1-5] - [Brief justification]
- Coherence: [1-5] - [Brief justification]
- Robustness: [1-5] - [Brief justification]
- Practical Feasibility: [1-5] - [Brief justification]

### Frame 2: [Name]
[Same structure]

### Frame 3: [Name]
[Same structure]

### Frame 4: [Name]
[Same structure]

## Part 3: Comparative Analysis

### Comparison Matrix
[Table]

### Key Trade-offs
1. [Trade-off 1]
2. [Trade-off 2]
3. [Trade-off 3]

## Part 4: Selection

### Recommended Frame
[Your choice]

### Justification
[300-400 words]

### Backup Frame
[Your second choice and brief rationale]
```

---

## Evaluation Rubric

| Criterion | Points | What We're Looking For |
|-----------|--------|------------------------|
| Frame evaluations | 30 | Accurate scoring with clear justifications |
| Trade-off identification | 25 | Identified non-obvious tensions between frames |
| Selection justification | 35 | Reasoning is sound, acknowledges weaknesses |
| Overall judgment | 10 | Would the expert make the same choice? |

---

## What Good Frame Comparison Looks Like

**Bad comparison**:
- "Frame 1 is best because it sounds most academic"
- Scoring all dimensions the same across frames
- No recognition of trade-offs
- Justification doesn't reference specific evidence

**Good comparison**:
- "Frame 1 scores highest on novelty (5) because no one has applied [theory] to [context], but it scores lower on evidence fit (3) because the heterogeneity pattern doesn't cleanly match the theory's predictions"
- Trade-offs articulated: "If I want maximum novelty, I accept thinner evidence; if I want bulletproof evidence, I accept a more incremental contribution"
- Justification acknowledges: "The weakness of Frame 1 is [X]. A hostile reviewer would say [Y]. My response would be [Z]."

---

## Common Mistakes

1. **Scoring all frames the same**: If all frames score 4-4-4-4-4-4, you're not discriminating. Real frames have different strengths.

2. **No trade-off recognition**: Saying Frame 1 is "just better in every way" misses the point. Almost always, stronger novelty comes with weaker evidence fit or narrower audience.

3. **Justification is just restating scores**: "I picked Frame 1 because it scored highest" isn't justification. Explain WHY those scores matter given your goals.

4. **Ignoring feasibility**: The most exciting frame isn't the best choice if you can't actually write that paper.

5. **Backup is "anything but my choice"**: Your backup should be a genuine alternative that would be chosen under different circumstances.

---

## Tips

1. **Score first, then compare**. Don't let your preference contaminate evaluation. Score each frame independently, then look at the matrix.

2. **Trade-offs are features, not bugs**. Real scholarly choice involves accepting worse on some dimensions to get better on others.

3. **Think about the reviewer**. Your selection will be evaluated by an expert. They'll see if your reasoning is sound even if they'd choose differently.

4. **The backup matters**. Showing you understand why someone might choose differently demonstrates judgment.

---

## Submit

```bash
skillforge submit domain-4 --level 2 --file your-submission.md
```
