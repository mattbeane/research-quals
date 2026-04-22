# Domain 1: Pattern Recognition
## Level 2 Task - Application with Feedback

**Time**: 2-4 hours
**Passing**: ≥70/100, with detailed feedback
**Retake**: After 7 days

---

## Your Task

You will explore a quantitative dataset to identify patterns worth pursuing. This task tests your ability to:
1. Distinguish signal from noise
2. Apply robustness thinking before framing
3. Identify theoretically interesting patterns (not just significant ones)
4. Document and kill weak findings

---

## Materials Provided

You have been given a dataset with variables related to training outcomes. The data is located in:

```
seed-data/training-outcomes/training_data_l2.csv
seed-data/training-outcomes/data_dictionary.md
```

**Context**: This data comes from a multi-site study of professional training. You'll find:
- Trainee characteristics (experience, background)
- Training conditions (program type, mentor involvement)
- Outcome measures (skill assessments, completion rates)
- Site-level variables (organization size, resources)

---

## Instructions

### Part 1: Initial Exploration (20%)

Explore the data to understand what's there.

**Requirements:**
- Report key descriptive statistics
- Note any surprising distributions or patterns
- Identify which variables have meaningful variation

### Part 2: Pattern Identification (40%)

Identify your **top 3 patterns** worth investigating further.

**For each pattern:**
1. **Describe it**: What relationship or finding did you observe?
2. **Theoretical interest**: Why is this interesting beyond statistical significance? What would it mean if true?
3. **Robustness concerns**: What obvious confounds should be checked? What might kill this finding?
4. **Heterogeneity**: Does this pattern hold for everyone, or does it vary by subgroup?

**Avoid**:
- Reporting every significant correlation
- Treating p<0.05 as sufficient for interest
- Ignoring effect sizes

### Part 3: Killed Findings (20%)

Document **at least 2 patterns** you explored but decided NOT to pursue.

**For each:**
1. What pattern did you initially observe?
2. Why did you kill it? (too small, doesn't survive controls, well-established, etc.)
3. What robustness check revealed the problem?

### Part 4: Prioritization (20%)

Rank your top 3 patterns by theoretical promise. Explain your ranking.

**Consider:**
- Effect size and practical significance
- Likelihood of surviving additional scrutiny
- Theoretical novelty (what would it change if true?)
- Data available to investigate further

---

## Submission Format

Submit a markdown file with these sections:

```markdown
# Domain 1 Level 2 Submission

## Part 1: Initial Exploration

### Key Descriptives
...

### Surprising Patterns
...

## Part 2: Top 3 Patterns

### Pattern 1: [Name]
- Description: ...
- Theoretical interest: ...
- Robustness concerns: ...
- Heterogeneity: ...

### Pattern 2: [Name]
...

### Pattern 3: [Name]
...

## Part 3: Killed Findings

### Killed 1: [Name]
- Initial observation: ...
- Why killed: ...
- What revealed the problem: ...

### Killed 2: [Name]
...

## Part 4: Prioritization

1. [Pattern X] because...
2. [Pattern Y] because...
3. [Pattern Z] because...
```

---

## Evaluation Rubric

| Criterion | Points | What We're Looking For |
|-----------|--------|------------------------|
| Found patterns | 30 | Did you identify patterns the expert found? |
| Avoided false positives | 20 | Did you avoid pursuing noise? |
| Reasoning quality | 30 | Is robustness thinking sound? |
| Completeness | 20 | Killed findings documented? Heterogeneity explored? |

---

## Tips

1. **Robustness first, framing later**. Check if the pattern survives before getting excited.
2. **Heterogeneity is often the story**. If an effect varies by subgroup, investigate why.
3. **Effect size matters**. A tiny effect that's significant isn't interesting.
4. **Anomalies are friends**. Patterns that violate expectations are often paper-worthy.
5. **Kill findings proudly**. Documenting what doesn't work is part of the process.

---

## Submit

```bash
skillforge submit domain-1 --level 2 --file your-submission.md
```
