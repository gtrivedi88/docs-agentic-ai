# Lyra Documentation Agent - Demo

**Autonomous Documentation Generation - Demonstration Version**

---

## Quick Start (3 Steps)

```bash
# 1. Setup (30 seconds)
./setup_demo.sh

# 2. Run demo (3 seconds)
python src/main.py create-release-notes v2.1

# 3. View output
cat demo/outputs/openshift_v2.1_release_notes.md
```

**That's it!** You just saw Lyra generate release notes from multiple sources.

---

## What is This?

This is a **demonstration version** of Lyra - an autonomous documentation agent that:
- Searches multiple sources (Jira, GitHub, Confluence, Slack, etc.)
- Extracts key decisions from noise (50 comments → 1 decision)
- Synthesizes professional documentation
- Includes citations for transparency

**This demo uses hardcoded data** to show what the full system will do.

---

## Demo Commands

### Basic Demo
```bash
python src/main.py create-release-notes v2.1
```

### Show What's Hardcoded
```bash
python src/main.py create-release-notes v2.1 --show-hardcoded
```

### Get Information
```bash
python src/main.py info
```

---

## Documentation

- **`README_DEMO.md`** - Complete demo guide, FAQ, customization
- **`demo/PRESENTATION_SCRIPT.md`** - How to present to your team (10 min script)
- **`DEMO_CHECKLIST.md`** - Pre-presentation checklist

### Full Implementation Docs (in parent directory)
- **`phase1_implementation_plan.md`** (5,650 lines) - Complete code reference
- **`phase1_incremental_sprints.md`** (1,312 lines) - Sprint-based execution
- **`working_with_ai_implementation_guide.md`** (2,055 lines) - AI collaboration prompts

---

## Demo vs Full Version

| Feature | Demo | Full Version |
|---------|------|--------------|
| Data | Hardcoded JSON | Real APIs |
| Agent | Simulated | Real LLM (Mistral AI) |
| Output | Pre-written | Actually generated |
| Sources | 3 (samples) | 6 (live) |
| Build Time | 1-2 days | 7-9 days |
| Purpose | Validate concept | Production use |

---

## Next Steps

### After Demoing to Team:

**If Approved** → Start Sprint 1:
1. Use prompts from `working_with_ai_implementation_guide.md`
2. Implement Sprint 1 (2 days): Jira + GitHub working
3. Demo real release notes generation
4. Continue Sprints 2-6

**If Feedback** → Adjust plan and re-demo

---

## Demo Structure

```
demo-lyra/
├── demo/
│   ├── fixtures/              # Hardcoded sample data
│   ├── outputs/               # Generated files appear here
│   ├── demo_agent.py          # Simulated agent
│   └── PRESENTATION_SCRIPT.md # How to present
│
├── src/
│   ├── main.py               # CLI entry point
│   └── utils/
│       └── terminal_ui.py    # Beautiful terminal output
│
├── README.md                  # This file
├── README_DEMO.md             # Detailed demo guide
├── DEMO_CHECKLIST.md          # Pre-presentation checklist
├── requirements_demo.txt      # Just: rich, typer
└── setup_demo.sh              # One-command setup
```

---

## Key Points for Your Team

1. **This solves a real problem**: Hours of manual work automated
2. **It's feasible**: Complete architecture designed
3. **It's planned**: 6 sprints, 7-9 days, clear milestones  
4. **It's smart**: Shows intelligence (distillation, quality review)
5. **It's transparent**: Citations, confidence scores
6. **It's ready**: Can start Sprint 1 immediately

---

## Presenting to Your Team?

1. Read: `demo/PRESENTATION_SCRIPT.md` (10-minute script)
2. Check: `DEMO_CHECKLIST.md` (preparation checklist)
3. Review: `README_DEMO.md` (detailed FAQ)

**You have everything you need for a successful demo!**

---

## Customizing the Demo

Want to customize for your project?

**Change the data**: Edit `demo/fixtures/*.json` with your examples  
**Change the output**: Edit `demo/fixtures/expected_output.md`  
**Change the timing**: Edit `time.sleep()` values in `demo/demo_agent.py`  
**Change the project**: Use `--project=yourproject` flag

---

## Questions?

**About the demo**: See `README_DEMO.md`  
**About presenting**: See `demo/PRESENTATION_SCRIPT.md`  
**About implementation**: See parent directory docs  

---

**Ready to demo? Run**: `python src/main.py create-release-notes v2.1`

