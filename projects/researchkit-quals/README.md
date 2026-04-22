# SkillForge

**Train like a mixed-methods management scholar. Learn what you actually need to do the work.**

## The Problem

PhD programs teach theory and methods separately from the messy reality of producing research. Students learn regression in one course, qualitative coding in another, and framing in a third—but nobody teaches them how these fit together when you're staring at a dataset wondering "is this a paper?"

Most doctoral training happens through apprenticeship: watch your advisor, absorb tacit knowledge, hope you pick up the pattern recognition that distinguishes publishable insights from noise. Some students get great mentorship. Many don't.

Meanwhile, AI tools are getting powerful enough to generate polished-looking research outputs. Without the underlying judgment, students can produce work that *looks* rigorous but isn't.

## The Solution

SkillForge is a competency-based training system for mixed-methods management research. It captures the tacit knowledge that expert researchers use—and makes it learnable.

**Seven domains. Three levels. Real data.**

| Domain | The Question It Answers |
|--------|------------------------|
| 1. Pattern Recognition | Is this signal or noise? |
| 2. Theoretical Positioning | What makes this a contribution? |
| 3. Qualitative Mechanism | What's actually happening here? |
| 4. Theoretical Framing | How do I position this for reviewers? |
| 5. Epistemological Genre | Am I discovering or testing? |
| 6. Adversarial Evidence | What challenges my interpretation? |
| 7. Claim Verification | Does my evidence support my claims? |

## How It Works

### Level 1: Recognize
Can you identify good practice when you see it? Multiple choice and short answer on real examples.

*"A researcher finds that 12 of 15 informants support the mechanism, but 3 describe the opposite. What should they do?"*

### Level 2: Apply
Given real data, can you do it yourself—with feedback? Work on actual datasets, get detailed comparison to expert analysis.

*"Here are 10 interview excerpts. Code them for mechanisms. We'll compare your coding to how a published researcher coded the same data."*

### Level 3: Perform
Can you do it independently on novel materials? Single attempt, expert evaluation, no hand-holding.

*"Here's a new dataset. Find the patterns. Identify the mechanisms. We'll assess whether you found what an expert would find—and whether you avoided the traps."*

## What Makes It Different

**Built on real research.** Assessment materials come from published studies—anonymized dissertation data with expert baselines showing what skilled researchers actually found.

**Tacit knowledge made explicit.** Each domain captures what experts do intuitively: the robustness checks they run first, the disconfirming evidence they hunt for, the overclaims they catch.

**Progressive mastery.** You can't skip ahead. Pattern recognition comes before theoretical framing. Finding mechanisms comes before verifying claims. The sequence matters.

**Advisor-compatible.** Faculty can review student work and certify competence. No arbitrary gatekeeping—just demonstrated skill.

## Time to Competence

**Typical PhD student:** 3-6 months to full competency across all domains

- Domains 1-2: 2-4 weeks (foundational)
- Domain 3: 2-4 weeks (requires coding practice)
- Domains 4-5: 4-6 weeks (iteration and feedback)
- Domains 6-7: 2-4 weeks (builds on prior)

**Fast track:** Students with prior qual methods training can test out of early domains immediately.

## Getting Started

```bash
# Check your current status
skillforge status

# Take a Level 1 assessment
skillforge take domain-1 level-1

# Submit Level 3 work for evaluation
skillforge submit domain-3 --file my-coding.md
```

## For Faculty: Contributing Data

The system gets better with more expert baselines. Faculty can contribute anonymized data from their research to create new assessment materials.

### The Anonymization Engine

A three-stage pipeline protects your data:

1. **Detect**: NER + regex patterns find names, places, organizations, dates
2. **Review**: You verify each detection, assign pseudonyms, mark false positives
3. **Apply**: Replacements applied, audit trail generated, sign-off template created

All processing runs locally. Your data never leaves your machine.

```bash
# Parse your Atlas.ti project
python tools/atlasti_parser.py "My Project.atlpac" parsed_data.json

# Run the full anonymization pipeline
python tools/anonymize.py detect parsed_data.json
python tools/anonymize.py review parsed_data.entities.json
python tools/anonymize.py apply parsed_data.entities.reviewed.json parsed_data.json \
    --output-dir contribution/ --verify
```

### Creating Expert Baselines

After anonymization, document your expert knowledge:

- **Mechanisms found**: What did you discover in this data?
- **Key evidence**: Which quotes reveal each mechanism?
- **Disconfirming evidence**: What challenged your interpretation?
- **What makes good coding**: Your tacit standards made explicit

This becomes the ground truth students are assessed against.

## Current Status

**Built:**
- ✅ 7 competency domain definitions with rubrics
- ✅ Level 1 assessments for Domains 1, 3, 7
- ✅ Atlas.ti parser + 3-stage anonymization engine
- ✅ Expert baseline from published robotic surgery research
- ✅ Scoring specifications for all levels

**Coming:**
- ⏳ Level 2-3 assessments
- ⏳ CLI for taking/submitting assessments
- ⏳ Student record tracking
- ⏳ Additional expert baselines from faculty contributions

## Philosophy

**Competency over credentials.** Time in program doesn't equal readiness. Demonstrated skill does.

**Authentic over artificial.** Assessments use real data, not toy examples. If you can do it here, you can do it in your research.

**Transparent over mysterious.** The rubrics are public. The expert baselines show what good looks like. No hidden criteria.

**Formative over punitive.** Level 1-2 exists for learning. Fail, get feedback, try again. Level 3 is where it counts.

---

*SkillForge: Because "I took a methods course" isn't the same as "I can do research."*
