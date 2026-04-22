# SkillForge - Development Status

## ✅ Prototype Complete

The core system is operational:

```bash
pip install -e .
skillforge init --name "Student" --email student@ucsb.edu
skillforge status
skillforge take domain-1 --level 1
skillforge submit domain-3 --level 2 --file my-work.md
```

### What's Built

**CLI (`cli/`)**
- `skillforge.py` - Main CLI: init, status, take, submit
- `evaluator.py` - LLM-based L2-3 evaluation with structured JSON output
- `competency_gate.py` - TheoryForge integration (import and call `check_competency()`)

**Assessments (`assessments/`)**
- Level 1 quizzes for all 7 domains (10 MC + 2 short answer each)
- LLM scoring for short answers
- Question and option randomization
- Level 2-3 task documents (D1, D3)

**Infrastructure**
- Student records in `~/.skillforge/`
- Cooldown enforcement (7d L2, 30d L3)
- Domain prerequisites and level progression
- Few-shot calibrated evaluation prompts

**Seed Data**
- Expert baseline from Shadow Learning + Resourcing papers
- 3 mechanisms documented with quote IDs and disconfirming evidence

---

## 🔮 Future Development Directions

These features make sense once there are actual users:

### Advisor Certification (`skillforge certify`)
Allow advisors to certify student competence without assessment for students with prior demonstrated skill (e.g., published qual paper, rigorous methods course).

**Design considerations:**
- Max 3 domains certifiable per student
- Domains 6-7 (Adversarial, Verification) cannot be certified—must demonstrate
- Need to decide: CLI approval vs email link vs web interface
- Need to decide: How to verify advisor identity

### Faculty Mode
Faculty shouldn't be gated by competency requirements.

**Design considerations:**
- `skillforge faculty-mode --enable`
- Bypasses all competency gates
- Can view student progress
- Can take assessments in calibration mode (not recorded)
- Need to decide: Honor system vs institutional verification

### Additional Expert Baselines
Currently only Matt's surgery data. More baselines from different contexts would:
- Test generalization of assessment approach
- Provide variety for L2-3 materials
- Allow domain-specific assessments beyond surgery examples

### Question Banking
Currently each domain has one fixed question set. For fairer retakes:
- Create 2-3 question variants per item
- Randomly select from pool each attempt
- Track which variants student has seen

### Student Dashboard for Advisors
Web interface showing:
- All advisees' progress
- Pending certification requests
- Aggregate statistics

---

## 📁 Current File Structure

```
skillforge/
├── README.md                    # Standalone pitch
├── TODO.md                      # This file
├── pyproject.toml               # pip installable
│
├── cli/
│   ├── __init__.py
│   ├── skillforge.py            # Main CLI
│   ├── evaluator.py             # L2-3 LLM evaluation
│   └── competency_gate.py       # TheoryForge integration
│
├── assessments/
│   ├── ASSESSMENT_SPECS.md      # Scoring rubrics
│   ├── level-1-domain-*.md      # L1 quizzes (all 7 domains)
│   └── tasks/
│       ├── level-2-domain-1-task.md
│       ├── level-2-domain-3-task.md
│       └── level-3-instructions.md
│
├── competencies/                # Domain definitions
│   └── domain-*-*.md            # 7 domain specs
│
├── tools/                       # Data processing
│   ├── atlasti_parser.py
│   └── anonymize*.py            # 3-stage anonymization
│
└── seed-data/
    └── beane-surgery-anonymized/
        └── expert_baseline.md   # Matt's tacit knowledge
```

---

## Next Steps When Ready to Deploy

1. **Find pilot students** - 2-3 PhD students willing to test
2. **Run them through D1 and D3** - Validate L1 quizzes discriminate
3. **Gather feedback** - What's confusing? What's missing?
4. **Then** consider certification/faculty features based on actual needs
