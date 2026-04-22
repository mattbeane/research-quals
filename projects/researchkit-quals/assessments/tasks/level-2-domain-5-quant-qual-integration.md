# Domain 5: Evidence Evaluation
## Level 2 Task - Quantitative-Qualitative Integration

**Time**: 3-4 hours
**Passing**: ≥70/100, with detailed feedback
**Retake**: After 7 days

---

## Your Task

You will evaluate evidence from a mixed-methods study, specifically testing your ability to:
1. Identify where quantitative patterns and qualitative mechanisms CONVERGE
2. Identify where they DIVERGE or contradict
3. Diagnose gaps in coverage
4. Generate integrated claims that draw on both streams

This task tests the critical skill of integration—not just having both quant and qual, but making them talk to each other.

---

## Materials Provided

You have been given:

1. **Quantitative pattern report**: `seed-data/integration-test/PATTERN_REPORT.md`
   - 4 robust patterns identified
   - Effect sizes and heterogeneity documented
   - Subgroups that show vs. don't show the effects

2. **Qualitative mechanism report**: `seed-data/integration-test/MECHANISM_REPORT.md`
   - 3 mechanisms identified from interviews
   - Supporting and challenging quotes
   - Informant roles and sites represented

3. **Raw data summary**: `seed-data/integration-test/DATA_SUMMARY.md`
   - Who was interviewed (roles, sites)
   - What's in the quantitative data
   - Any known gaps

---

## Instructions

### Part 1: Build the Mapping Matrix (25%)

Create a matrix showing how patterns map to mechanisms:

```
                    | Mechanism A | Mechanism B | Mechanism C | No Mechanism
--------------------|-------------|-------------|-------------|-------------
Pattern 1           |             |             |             |
Pattern 2           |             |             |             |
Pattern 3           |             |             |             |
Pattern 4           |             |             |             |
No Pattern          |             |             |             |
```

For each cell, indicate:
- **✓ Strong link**: Mechanism clearly explains pattern
- **~ Partial link**: Possible connection, needs more evidence
- **✗ No link**: Not related
- Leave empty if unclear

### Part 2: Convergence Analysis (25%)

For any Pattern-Mechanism pairs you marked ✓ or ~:

**A. Describe the connection:**
- What evidence links this pattern to this mechanism?
- Does the mechanism operate for the same subgroups showing the pattern?

**B. Draft an integrated claim:**
> "[Pattern X] appears in the quantitative data (effect = Y). Qualitative evidence suggests [Mechanism A] drives this effect because [specific evidence]. This is consistent with [theoretical explanation]."

### Part 3: Divergence Analysis (25%)

Identify and analyze:

**A. Unexplained patterns** (quant pattern with no qual mechanism):
- Which patterns lack mechanism evidence?
- Why might this be? (Sampling gap? Different construct? Spurious pattern?)
- What would you need to explain this pattern?

**B. Unsupported mechanisms** (qual mechanism with no quant pattern):
- Which mechanisms don't show quantitative support?
- Why might this be? (Too context-specific? No matching variable? Real but rare?)
- Can you construct a quant test?

**C. Contradictions** (quant and qual point opposite directions):
- Are there any? Describe them.
- How would you resolve? (Boundary condition? Measurement error? Different constructs?)

### Part 4: Gap Analysis (25%)

**A. Qualitative coverage of quantitative subgroups:**

| Quant Subgroup | Effect in Quant | Qual Interviews | Coverage |
|----------------|-----------------|-----------------|----------|
| [Subgroup A]   | [Effect]        | [N]             | Good/Thin/None |
| ...            | ...             | ...             | ...      |

**B. Quantitative coverage of qualitative mechanisms:**

| Qual Mechanism | Supporting Quotes | Quant Variable Available? | Coverage |
|----------------|-------------------|--------------------------|----------|
| [Mechanism A]  | [N]               | Yes/Proxy/No             | Good/Thin/None |
| ...            | ...               | ...                      | ...      |

**C. Critical gaps**:
- What gap most undermines your ability to make integrated claims?
- What would you do about it?

---

## Submission Format

```markdown
# Domain 5 Level 2 Submission: Integration

## Part 1: Mapping Matrix

[Your matrix]

## Part 2: Convergence Analysis

### Convergence 1: Pattern [X] ↔ Mechanism [Y]
- Connection: ...
- Integrated claim: ...

[Repeat for each strong convergence]

## Part 3: Divergence Analysis

### Unexplained Patterns
...

### Unsupported Mechanisms
...

### Contradictions
...

## Part 4: Gap Analysis

### Qual Coverage of Quant Subgroups
[Table]

### Quant Coverage of Qual Mechanisms
[Table]

### Critical Gap
...
```

---

## Evaluation Rubric

| Criterion | Points | What We're Looking For |
|-----------|--------|------------------------|
| Matrix accuracy | 25 | Correctly identified links between patterns and mechanisms |
| Convergence claims | 25 | Integrated claims that appropriately draw on both streams |
| Divergence diagnosis | 25 | Identified and explained gaps, contradictions |
| Gap analysis | 25 | Realistic assessment of coverage, sensible remediation |

---

## Common Mistakes to Avoid

1. **"Ships passing in the night"**: Treating quant and qual as separate sections that don't speak to each other. Integration requires explicit connections.

2. **"Qual as illustration"**: Using qual only to put a human face on numbers. Qual should reveal MECHANISMS—the "why" behind the patterns.

3. **"All convergence, no divergence"**: Real data always has gaps and tensions. If you found zero divergences, you're not looking hard enough.

4. **"Ignoring coverage gaps"**: Claiming strong integration when your qual doesn't cover the subgroups showing the quant effect.

5. **"Forcing fit"**: Making mechanisms sound like they explain patterns when the connection is weak or speculative.

---

## Tips

1. **Start with the matrix**. This forces systematic comparison before you write claims.

2. **Be honest about partial links**. A ~ is not failure—it's accurate assessment.

3. **Divergences are interesting**. The patterns without mechanisms, or mechanisms without patterns, often become the most important part of the paper (as limitations or future directions).

4. **Coverage matters**. If quant shows the effect is strongest for Group A, but your qual interviews are mostly Group B, that's a gap you must acknowledge.

5. **Integrated claims are hard**. If you find yourself just summarizing quant, then summarizing qual, you're not integrating. Real integration shows how they inform each other.

---

## Submit

```bash
skillforge submit domain-5 --level 2 --file your-submission.md
```
