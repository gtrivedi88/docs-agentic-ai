# Lyra Demo - Pre-Presentation Checklist

## 24 Hours Before Presentation

### Technical Setup
- [ ] Run `./setup_demo.sh` to install dependencies
- [ ] Test: `python src/main.py create-release-notes v2.1`
- [ ] Verify: Output file created in `demo/outputs/`
- [ ] Test: `python src/main.py info`
- [ ] Test: `python src/main.py version`
- [ ] Time the demo (should take ~3 seconds)
- [ ] Clear `demo/outputs/` directory for fresh demo

### Presentation Prep
- [ ] Read `demo/PRESENTATION_SCRIPT.md` (memorize flow)
- [ ] Review `README_DEMO.md` (know what's hardcoded)
- [ ] Prepare answers to expected questions
- [ ] Have implementation docs ready to show (but don't present them in detail)

### Environment Prep
- [ ] Terminal: Increase font size (readable from back of room)
- [ ] Terminal: Set to fullscreen
- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Test screen sharing (if remote presentation)

---

## 1 Hour Before Presentation

### Final Checks
- [ ] Run demo once: `python src/main.py create-release-notes v2.1 --show-hardcoded`
- [ ] Verify terminal output looks good
- [ ] Clear output directory again: `rm demo/outputs/*`
- [ ] Open terminal to demo directory: `cd demo-lyra`
- [ ] Have command ready to paste: `python src/main.py create-release-notes v2.1 --show-hardcoded`

### Materials Ready
- [ ] Laptop charged / plugged in
- [ ] Demo runs without internet (all local data)
- [ ] Have implementation docs accessible (but not open)
- [ ] Have answers to FAQ ready

---

## During Presentation

### Setup (30 seconds before starting)
```bash
cd demo-lyra
clear
# Terminal should be clean and ready
```

### Part 1: Problem Statement (2 min)
- [ ] Explain current manual process
- [ ] Emphasize time cost (4-8 hours)
- [ ] Mention error-prone nature

### Part 2: Solution Overview (1 min)
- [ ] Introduce Lyra concept
- [ ] Mention autonomous agent
- [ ] Transition to live demo

### Part 3: Run Demo (3 min)
- [ ] Paste command: `python src/main.py create-release-notes v2.1 --show-hardcoded`
- [ ] Let them see "What's Hardcoded" explanation
- [ ] Confirm to continue
- [ ] Narrate as agent runs
- [ ] Let terminal output speak for itself (don't talk over it too much)

### Part 4: Show Output (1 min)
- [ ] Open: `demo/outputs/openshift_v2.1_release_notes.md`
- [ ] Scroll through to show:
  - Professional structure
  - Citations to Jira/GitHub
  - Breaking changes section
  - Migration guide links
  - Quality and completeness

### Part 5: Explain Demo vs Real (1 min)
- [ ] Run: `python src/main.py info`
- [ ] Point out what's hardcoded
- [ ] Point out what will be real
- [ ] Mention full implementation timeline

### Part 6: Q&A (2 min)
- [ ] Answer questions (see FAQ below)
- [ ] Note additional requirements
- [ ] Gauge interest level

---

## Expected Questions & Answers

### Q: "Is the output actually generated or pre-written?"
**A**: "In this demo, it's pre-written to show quality. The full version will actually generate content using Mistral AI. The workflow you saw - searching Jira, GitHub, distilling with smart tools - that's real logic, just with sample data."

### Q: "How do we know it won't hallucinate?"
**A**: "Three safeguards:
1. Agent only uses data from your systems (Jira, GitHub, etc.)
2. Every claim has citations - you can verify
3. Built-in quality review before finalizing
4. Human review before publishing (Phase 1)
Plus, we can tune the LLM temperature and prompts for accuracy."

### Q: "Can it handle our project?"
**A**: "Yes. This demo shows OpenShift, but it's project-agnostic. You configure:
- Your Jira project key
- Your GitHub repos
- Your Confluence space
- Your style guidelines
Everything else is automatic."

### Q: "What if our data is in different systems?"
**A**: "We've designed for 6 data sources: Jira, GitHub, GitLab, Confluence, Slack, Google Docs. If you have others, we can add them - the architecture supports it."

### Q: "How long to implement?"
**A**: "7-9 days for Phase 1 using our sprint plan:
- Sprint 1 (2 days): Working release notes generator
- Sprints 2-6 (5-7 days): Add more sources and features

After 2 days, you can test real release notes generation."

### Q: "What does it cost to run?"
**A**: "Mistral API costs ~$0.10-0.50 per document generated. Compare to 4-8 hours of human time."

### Q: "What if we want different output format?"
**A**: "Templates are customizable. We can output .md, .adoc, .rst, or any format. The demo shows .md, but it's configurable."

### Q: "Can it update existing docs?"
**A**: "Yes - that's Sprint 6. Full CRUD: Create, Read (audit), Update, Delete."

### Q: "What about security/access control?"
**A**: "Uses service accounts with read-only access to Jira/GitHub/etc. No write permissions needed (Phase 1). All credentials in secure .env file."

---

## After Presentation

### Immediate Actions
- [ ] Send README_DEMO.md to team
- [ ] Send link to implementation docs (if they want details)
- [ ] Schedule follow-up if needed
- [ ] Note all feedback and requirements

### If Approved
- [ ] Schedule Sprint 1 kickoff
- [ ] Prepare development environment
- [ ] Get API credentials (Jira, GitHub tokens)
- [ ] Start Sprint 1 using `working_with_ai_implementation_guide.md` prompts

### If Feedback Needed
- [ ] Document all requested changes
- [ ] Update implementation plan if needed
- [ ] Schedule re-demo if significant changes

---

## Success Metrics

Demo is successful if:
- ✅ Team understands the vision
- ✅ Team sees value (time savings, quality)
- ✅ Team believes it's feasible
- ✅ Team approves moving forward with Sprint 1
- ✅ Team is excited (not skeptical)

---

## Backup Plan

### If Demo Fails Technically:
- Have the output file already generated
- Show it manually
- Explain: "Technical glitch, but here's what it generates"
- Walk through the code to show it's real

### If Questions You Can't Answer:
- "Great question. Let me check the implementation docs."
- "I'll follow up with details on that."
- "Let me add that to requirements."

### If Skepticism About AI:
- Emphasize: "This is NOT generating from thin air"
- "It only uses YOUR data from YOUR systems"
- "Everything is cited and verifiable"
- "Human review before publishing"

---

## Demo Timing Breakdown

- Setup: 0s (command already typed)
- Planning: 0.5s
- Jira exploration: 1.5s
- Smart tool (Jira): 1.3s
- GitHub exploration: 1.5s
- Smart tool (GitHub): 1.2s
- Confluence: 0.9s
- Synthesis: 2.0s
- Critique: 1.3s
- Summary: instant

**Total: ~3.2 seconds**

---

## Key Messages to Emphasize

1. **Speed**: "3 seconds vs 4-8 hours"
2. **Quality**: "87% quality score, professional output"
3. **Completeness**: "Never miss a ticket or PR"
4. **Consistency**: "Always follows style guide"
5. **Scalability**: "Same system, all projects, all doc types"
6. **Transparency**: "Every claim cited, verifiable"
7. **Planned**: "Complete implementation ready, 7-9 days"

---

**Good luck! This demo will sell itself if you let it.** 🚀

