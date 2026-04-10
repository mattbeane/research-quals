# Research-Quals

**Train like a mixed-methods management scholar. Learn what you actually need to do the work.**

> **Part of the Forge ecosystem.** Research-quals builds the judgment. [Theory-forge](https://github.com/mattbeane/theory-forge) assumes it.

---

## If You're Worried About AI Replacing Researchers...

You're not wrong to worry. AI tools can now generate polished-looking papers, identify patterns in data, and draft theoretical framings. In the wrong hands, this creates problems.

But here's the thing: **AI doesn't know what it doesn't know.**

An LLM will:
- Frame discovery research as hypothesis testing (because that's what most papers look like)
- Overclaim contributions that aren't supported by evidence
- Miss disconfirming evidence that challenges the story
- Generate technically correct but theoretically boring findings
- Sound confident about things it's making up

**Researchers who can catch these mistakes are more valuable, not less.**

Research-quals prepares you to direct AI rather than be replaced by it. The Level 4 capstone proves you can catch what AI gets wrong—the exact skill that makes you irreplaceable in an AI-augmented research world.

This isn't about competing with AI. It's about becoming the human who knows when AI is wrong.

---

## The Problem

PhD programs teach theory and methods separately from the messy reality of producing research. Students learn regression in one course, qualitative coding in another, and framing in a third—but nobody teaches them how these fit together when you're staring at a dataset wondering "is this a paper?"

Most doctoral training happens through apprenticeship: watch your advisor, absorb tacit knowledge, hope you pick up the pattern recognition that distinguishes publishable insights from noise. Some students get great mentorship. Many don't.

Meanwhile, AI tools are getting powerful enough to generate polished-looking research outputs. Without the underlying judgment, students can produce work that *looks* rigorous but isn't.

## The Solution

Research-quals is a competency-based training system for mixed-methods management research. It captures the tacit knowledge that expert researchers use—and makes it learnable.

**Seven domains. Three levels. Real data.**

| Domain | The Question It Answers |
|--------|------------------------|
| 1. Pattern Recognition & Data Sense | Is this signal or noise? |
| 2. Theoretical Positioning | What makes this a contribution? |
| 3. Research Design Intuition | Can this design answer this question? |
| 4. Qualitative Rigor | Is this interpretation defensible? |
| 5. Literature Synthesis | How does this fit the conversation? |
| 6. Adversarial Evidence | What challenges my interpretation? |
| 7. Claim Verification | Does my evidence support my claims? |

## How It Works

### Foundation
Can you identify good practice when you see it? Conceptual exercises on real examples. Unlimited retakes—this is for learning.

*"Here are 6 research questions. Match each to the appropriate method and explain why."*

### Practice
Given real data, can you do it yourself—with feedback? Work on actual problems, get detailed comparison to expert analysis.

*"Code these interview excerpts. Build themes from your codes. We'll compare your analysis to expert standards."*

### Mastery
Can you do it independently and defend your choices? Single attempt, expert evaluation, adversarial defense.

*"Design a complete research study. Defend it against hostile reviewer critiques. This is where you prove it."*

### Capstone (Two Options)

**Option A — AI Output Supervision**: Can you catch what AI gets wrong? Review an AI-generated paper and identify issues across all seven domains.

*"An AI ran this dataset through a research pipeline and produced a draft paper. Find everything wrong with it. Prioritize what would sink it at review."*

**Option B — Build Your Own Machine**: Given an unfamiliar dataset and full access to every existing tool (including theory-forge), build your own analytical pipeline and defend every design choice. The dataset is deliberately chosen so copying doesn't help — the defense exposes whether the choices are genuinely yours.

*"Show me your machine. We'll debrief about what you thought you knew about the scholarly process that led you to build it that way."* — Paul Leonardi

Students can complete one or both capstones. Both require mastery badges in all seven domains.

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
research-quals status

# Take a Level 1 assessment
research-quals take domain-1 level-1

# Submit Level 3 work for evaluation
research-quals submit domain-3 --file my-coding.md
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
- ✅ Complete curriculum: 42 exercises + 21 assessments across all 7 domains
- ✅ Three levels per domain: Foundation, Practice, Mastery
- ✅ Two capstone options: AI Output Supervision + Build Your Own Machine
- ✅ 26 badge designs with git-based verification system
- ✅ Portfolio template for student progress tracking
- ✅ Atlas.ti parser + 3-stage anonymization engine
- ✅ Expert baseline from published robotic surgery research

**Coming:**
- ⏳ CLI for taking/submitting assessments
- ⏳ Automated badge issuance
- ⏳ Additional expert baselines from faculty contributions

## Skill-Forge + Theory-Forge: The Ecosystem

**Research-quals** teaches the judgment skills. **Theory-forge** is the AI-assisted pipeline for producing papers.

```
Skill-Forge → Learn the craft → Theory-Forge → Accelerate the work
   (judgment)                    (productivity)
```

### Why Both?

AI tools like theory-forge can dramatically accelerate research—but they require supervision. An LLM can generate plausible-looking framings, identify patterns, and draft prose. But it will also:

- Frame discovery research as hypothesis testing (genre violation)
- Overclaim contributions that aren't supported by evidence
- Miss disconfirming evidence that challenges the story
- Generate technically correct but theoretically boring findings

**Research-quals ensures you can catch what AI gets wrong.**

### The Unlock

Theory-forge checks whether you've completed research-quals before letting you proceed. This isn't gatekeeping—it's protection. Using powerful tools without the judgment to evaluate their output creates problems that show up at peer review, or worse, after publication.

| Skill-Forge Badge | What It Unlocks in Theory-Forge |
|-------------------|--------------------------------|
| D1 Practice | `/hunt-patterns` (guided mode) |
| D4 Practice | `/mine-qual` (mechanism extraction) |
| D5 Foundation | `/eval-genre` (can check your own papers) |
| All 7 Mastery badges | Full theory-forge access |
| AI Supervisor (Capstone) | Certified to supervise AI research tools |

### The Capstone Proves It

The AI Supervisor capstone is the qualifying exam: review an AI-generated paper and catch all the issues. If you can do that, you can use theory-forge responsibly. If you can't, you need more practice—better to discover that here than at peer review.

**→ [Theory-forge documentation](https://github.com/mattbeane/theory-forge)**

---

## The broader question: what happens to apprenticeship?

Research-quals answers a specific question: *what skills do you need to do research?* But there's a bigger question it doesn't address: *what happens to the apprenticeship infrastructure when agentic AI tools enter the loop?*

When tools like theory-forge magnify novice errors and let seniors deliver outputs without juniors, legitimate peripheral participation breaks down. Students lose access to risky work. Faculty struggle to learn the new tools without looking incompetent. Shadow learning and inverted apprenticeship dynamics kick in.

That broader question — how to restore the conditions for skill development in AI-disrupted environments — is addressed by a companion project: **[reforging-apprenticeship](https://github.com/mattbeane/reforging-apprenticeship)**. It provides protocol infrastructure (sandbox sessions, a trace library, co-pilot sessions, Faculty Drill, cohort telemetry) for environments where the learning is bidirectional and the traditional apprenticeship model is under strain.

Research-quals teaches the skills. Reforging-apprenticeship provides the conditions under which those skills can actually develop.

---

## Philosophy

**Competency over credentials.** Time in program doesn't equal readiness. Demonstrated skill does.

**Authentic over artificial.** Assessments use real data, not toy examples. If you can do it here, you can do it in your research.

**Transparent over mysterious.** The rubrics are public. The expert baselines show what good looks like. No hidden criteria.

**Formative over punitive.** Level 1-2 exists for learning. Fail, get feedback, try again. Level 3 is where it counts.

---

*Research-quals: Because "I took a methods course" isn't the same as "I can do research."*
