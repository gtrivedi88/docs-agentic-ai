# Lyra Demo Presentation Script
## 10-Minute Team Presentation Guide

**Goal**: Show Lyra's value, get team buy-in for full implementation  
**Time**: 10 minutes  
**Audience**: Engineering team, product managers, tech leads

---

## Pre-Presentation Setup (5 minutes before)

### Terminal Setup
```bash
cd demo-lyra
pip install -r requirements_demo.txt
python src/main.py info  # Test it works
clear  # Clean terminal
```

### Have Open
1. Terminal (for live demo)
2. `demo/outputs/` folder (to show generated file)
3. This script (for reference)

---

## Presentation Flow

### PART 1: The Problem (2 minutes)

**Say**:
"Let me show you the current state of our release notes process."

**Show** (optional - have a screenshot):
- Open Jira with 20 tickets
- Open GitHub with 15 PRs
- Open Confluence with style guide
- Open Google Docs with requirements

**Say**:
"To create release notes, a technical writer must:
1. Search Jira for all tickets in a release (10-20 tickets)
2. Read through hundreds of comments to find key decisions
3. Find related PRs in GitHub (across multiple repos)
4. Read PR descriptions and code diffs
5. Check Confluence for style guidelines
6. Synthesize all this into coherent documentation
7. Manually verify accuracy

**Time**: 4-8 hours per release  
**Error-prone**: Easy to miss tickets, misinterpret comments, or miss linked PRs  
**Inconsistent**: Style varies by writer  
**Not scalable**: We have multiple projects, multiple releases per month"

**Transition**:
"What if we could automate this?"

---

### PART 2: The Solution (1 minute)

**Say**:
"We've designed Lyra - an autonomous documentation agent. Let me show you what it does."

**Show**: Architecture diagram (optional - draw on whiteboard or show doc):
```
Command → Agent → Explores Multiple Sources → Synthesizes → Release Notes
          ↓
    Jira, GitHub, Confluence, Slack, etc.
```

**Say**:
"One command. Agent does all the searching, reading, and synthesis. Let me show you."

---

### PART 3: Live Demo (5 minutes)

**Terminal Command**:
```bash
python src/main.py create-release-notes v2.1 --show-hardcoded
```

**As it runs, narrate**:

*[When it shows "What's Hardcoded"]:*
"This demo uses sample data. I'll show you in a moment what will be real."

*[Click continue]*

*[As agent explores Jira]:*
"Watch - it's searching Jira for tickets... Found 5 tickets. Now it's following linked tickets... reading 47 comments."

*[As smart tool runs]:*
"This is key - the smart tool distills those 47 comments into 4 clear decisions. No noise."

*[As it searches GitHub]:*
"Now GitHub - finding related PRs... 7 PRs linked to those tickets."

*[As second smart tool runs]:*
"Another smart tool - analyzing what changed for users, filtering out internal refactoring."

*[As it searches Confluence]:*
"Checking our style guide for consistency."

*[As it synthesizes]:*
"Now it's writing - pulling together all this information into structured documentation."

*[As it critiques]:*
"Quality review - checking accuracy, completeness, style. Quality score: 87%."

*[When done]:*
"Done. 3 seconds. Let's look at what it generated."

**Open the generated file**:
```bash
cat demo/outputs/openshift_v2.1_release_notes.md
# Or open in your editor
```

**Point out**:
- "Look - professional structure"
- "See the citations? Every claim links back to Jira or GitHub"
- "Notice the breaking changes section - it caught that automatically"
- "Performance improvements - it understood the impact from code changes"
- "Migration guide link - it found related documentation tickets"

**Say**:
"This level of quality, in 3 seconds. Compare that to 4-8 hours manually."

---

### PART 4: What's Real vs Demo (2 minutes)

**Terminal Command**:
```bash
python src/main.py info
```

**As it displays, explain**:

*[Point to "What's Hardcoded"]:*
"This demo: 5 sample tickets, 7 sample PRs - hardcoded for demo.  
Full version: Real API connections to your actual Jira, GitHub, etc."

*[Point to "What Will Be Real"]:*
"Full version includes:
- Live API connections to 6 data sources
- Real LLM (Mistral AI) for reasoning
- Truly autonomous - it decides what to search, what's relevant
- Multiple doc types - release notes, help docs, API references
- Full lifecycle - create, update, delete, audit docs"

**Say**:
"This demo took 1 day to build. The full version we've completely architected - 7-9 days to implement."

---

### PART 5: The Plan (2 minutes)

**Say**:
"We have a complete implementation plan."

**Show** (briefly, don't read - just show existence):
- Open `phase1_implementation_plan.md` - "5,650 lines of complete code and architecture"
- Open `phase1_incremental_sprints.md` - "6 sprint breakdown, 7-9 days"
- Open `working_with_ai_implementation_guide.md` - "Copy-paste prompts for AI-assisted development"

**Say**:
"Everything is designed. 51 files, all planned out. We'll build it incrementally:

**Sprint 1** (2 days): Jira + GitHub working - can generate real release notes  
**Sprint 2** (1 day): Add Confluence for style  
**Sprint 3** (1 day): Add audit capability  
**Sprint 4** (1 day): Add help docs  
**Sprint 5** (1-2 days): Add remaining sources (GitLab, Slack, Google Docs)  
**Sprint 6** (1 day): Complete CRUD (update, delete)

After Sprint 1 (2 days), we have a working system. Each sprint adds capabilities."

---

### PART 6: The Ask & Q&A (2 minutes)

**Say**:
"Questions I expect:

**'How accurate will it be?'**  
Built-in quality review, citations for verification, human review before publishing.

**'What if it makes mistakes?'**  
Every claim has a citation back to source. You can verify. Plus audit feature finds outdated docs.

**'Can we customize it?'**  
Yes - configurable prompts, templates, quality thresholds, per-project settings.

**'What's the cost?'**  
Mistral API: ~$0.10-0.50 per document. Compare to hours of human time.

**'What's the timeline?'**  
7-9 days for Phase 1. Can demo Sprint 1 (working release notes) after 2 days.

Other questions?"

**Listen to feedback, note requirements.**

---

## Closing

**Say**:
"To summarize:
- This demo shows what Lyra will do
- We have complete implementation plan
- 7-9 days to fully working system
- Saves hours per release
- Improves consistency and quality
- Scales across projects

Do we have support to proceed with Sprint 1?"

---

## Post-Demo Actions

### If Team Says Yes:
1. ✅ Start Sprint 1 next week
2. ✅ Use `working_with_ai_implementation_guide.md` prompts
3. ✅ Demo Sprint 1 results after 2 days
4. ✅ Continue with Sprints 2-6

### If Team Has Feedback:
1. Note all feedback
2. Adjust implementation plan
3. Prioritize features based on feedback
4. Re-demo if needed

### If Team Says No:
1. Understand concerns
2. Address them in revised demo
3. Or pivot to different approach

---

## Quick Reference During Demo

### If Terminal Output Too Fast:
The demo is designed with realistic timing. If it's too fast, edit `demo/demo_agent.py` and increase `time.sleep()` values.

### If They Want to See Code:
Show `demo/demo_agent.py` - explain it's simple simulation.
Show `phase1_implementation_plan.md` - explain full version is architected.

### If They Ask "Can it do X?":
Check implementation docs:
- If in Phase 1 → "Yes, that's Sprint {N}"
- If not in Phase 1 → "That's Phase 2/3, but achievable"
- If totally new → "We can add that to requirements"

---

## Success Metrics for Your Presentation

After demo, team should:
- ✅ Understand what Lyra does
- ✅ See the value (time savings, quality)
- ✅ Believe it's feasible (you have complete plan)
- ✅ Excited to try it
- ✅ Ready to approve Sprint 1

---

**You've got this! The demo is designed to sell itself.** 🎯

