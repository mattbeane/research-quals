# Domain 3: Qualitative Mechanism Extraction
## Level 2 Task - Application with Feedback

**Time**: 2-4 hours
**Passing**: ≥70/100, with detailed feedback
**Retake**: After 7 days

---

## Your Task

You will analyze a set of interview excerpts to identify qualitative mechanisms. This task tests your ability to:
1. Find mechanisms operating in qualitative data
2. Create action/process-oriented codes
3. Identify and engage with disconfirming evidence
4. Report the full distribution of evidence

---

## Materials Provided

You have been given **10 interview excerpts** from an ethnographic study of surgical training. The excerpts are located in:

```
seed-data/beane-surgery-anonymized/interview_excerpts_l2.md
```

These excerpts are drawn from the anonymized dissertation data. They include:
- Interviews with surgical trainees (residents)
- Interviews with attending physicians (supervisors)
- Observations from the operating room

---

## Instructions

### Part 1: Initial Coding (40%)

Read all 10 excerpts and develop codes to capture what you observe.

**Requirements:**
- Create at least 8 codes
- Codes should be **action/process-oriented** (verbs, not nouns)
- For each code, list which excerpt(s) it applies to
- Provide one illustrative quote per code

**Bad codes** (topics, not processes):
- "Technology"
- "Learning"
- "Training"

**Good codes** (capture action):
- "Helicopter teaching" (constant verbal correction)
- "Undersupervised struggle" (working at edge of capacity alone)
- "Abstract rehearsal" (practicing on simulators/videos instead of patients)

### Part 2: Mechanism Identification (30%)

From your codes, identify **2-3 mechanisms** that explain how something works in this context.

**For each mechanism:**
1. Name it (descriptive, evocative)
2. Define it (1-2 sentences on what it is)
3. Explain how it works (the process)
4. List supporting evidence (excerpt numbers + specific quotes)
5. Explain its theoretical significance (why it matters)

### Part 3: Disconfirming Evidence (30%)

**CRITICAL**: This section is required to pass.

After identifying your mechanisms, actively search for evidence that challenges them.

**Requirements:**
1. Describe your process for searching for disconfirming evidence
2. Report the **full distribution**: How many excerpts support each mechanism? How many don't?
3. Identify at least **one disconfirming case** (an excerpt that challenges your interpretation)
4. Explain how you reconcile this with your mechanism (boundary condition? alternative explanation?)

**If you find zero disconfirming evidence**, explain why this might be problematic.

---

## Submission Format

Submit a markdown file with these sections:

```markdown
# Domain 3 Level 2 Submission

## Part 1: Codes

### Code 1: [Name]
- Definition: ...
- Excerpts: [list]
- Illustrative quote: "..."

### Code 2: [Name]
...

## Part 2: Mechanisms

### Mechanism 1: [Name]
- Definition: ...
- How it works: ...
- Supporting evidence: ...
- Theoretical significance: ...

### Mechanism 2: [Name]
...

## Part 3: Disconfirming Evidence

### Search Process
...

### Evidence Distribution
| Mechanism | Strong Support | Weak Support | No Evidence | Disconfirming |
|-----------|---------------|--------------|-------------|---------------|
| Mech 1    | X excerpts    | X excerpts   | X excerpts  | X excerpts    |
| Mech 2    | ...           | ...          | ...         | ...           |

### Disconfirming Case Analysis
Excerpt [#] challenges my interpretation because...
I reconcile this by...
```

---

## Evaluation Rubric

| Criterion | Points | What We're Looking For |
|-----------|--------|------------------------|
| Mechanism overlap | 30 | Did you find mechanisms the expert found? |
| Evidence overlap | 25 | Did you identify key evidence the expert used? |
| Disconfirming evidence | 30 | Did you find AND engage with complications? |
| Coding quality | 15 | Are codes action-oriented, not topics? |

**Minimum bar**: Must report disconfirming evidence to pass. Zero disconfirmation = automatic fail.

---

## Tips

1. **Read all excerpts first** before coding. Patterns emerge across the full set.
2. **Use informants' language** where possible (in-vivo codes).
3. **Don't force fit**. If an excerpt doesn't support your mechanism, that's data.
4. **The distribution matters**. "8 of 10 support" is different from "10 of 10 support."
5. **Disconfirmation is your friend**. It sharpens theory and shows intellectual honesty.

---

## Submit

```bash
skillforge submit domain-3 --level 2 --file your-submission.md
```

Your work will be evaluated against the expert baseline. You'll receive detailed feedback within minutes.
