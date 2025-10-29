# Documentation Specialist Quick Reference
## BMAD-EDI v4.0 - Enhanced Phase 7 Archival

**Version:** 1.0
**Date:** 2025-10-29

---

## Quick Start

### 1. Run Archive Script (30 seconds)

```bash
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  [ticket-id] [webedi-id] "[Company Name]" \
  --trading-partner "[Partner Name]" \
  --resolution-type "fixed"
```

**Example:**
```bash
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  13624970 5124 "Singtech Inc" \
  --trading-partner "Target" \
  --resolution-type "fixed"
```

### 2. Save Investigation Artifacts

```bash
# Save investigation report
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\analysis\investigation_report.md"

# Save NotebookLM queries
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\investigation\notebooklm_queries.md"
```

### 3. Save Resolution Artifacts

```bash
# Save customer response
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\resolution\customer_response.md"

# Save internal notes
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\resolution\internal_notes.md"
```

### 4. Complete Verification Checklist

Copy template and fill out:
```bash
cp "C:\Users\sleep\.claude\skills\media-analysis\templates\DOCUMENTATION_SPECIALIST_VERIFICATION_CHECKLIST.md" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\resolution\verification_checklist.md"
```

### 5. Review TICKET_SUMMARY.md

```bash
cat "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company]\TICKET_SUMMARY.md"
```

**Check for:**
- All sections filled (minimal "See investigation report" placeholders)
- File count accurate
- Timeline complete
- Quality metrics present
- No broken links

### 6. Hand Off to QA-Validator

Confirm:
- [X] Resolution folder complete
- [X] TICKET_SUMMARY.md reviewed
- [X] Verification checklist 100% complete
- [X] Customer history updated
- [X] All artifacts saved

---

## Resolution Types

Choose appropriate type with `--resolution-type`:

- **fixed** (default) - Issue resolved completely
- **workaround** - Temporary solution provided
- **duplicate** - Duplicate of another ticket
- **escalated** - Escalated to engineering
- **no-issue** - No issue found

---

## Folder Structure (Auto-Created)

```
resolution/[WebEDI-ID]_[Company_Name]/
├── TICKET_SUMMARY.md                    # Quick reference index
├── original_files/                       # Original media + customer files
├── analysis/                             # Phase 0 + investigation reports
│   ├── phase0_metadata.json
│   ├── phase0_analysis.md
│   └── investigation_report.md
├── investigation/                        # NotebookLM queries, notes, evidence
├── resolution/                           # Customer response, notes, summary
│   ├── customer_response.md
│   ├── internal_notes.md
│   └── verification_checklist.md
└── metadata/                             # Ticket metadata, timeline, metrics
    ├── ticket_metadata.json
    └── timeline.json
```

---

## What Gets Archived Automatically

### Phase 0 Artifacts (if available)
- `analysis/phase0_metadata.json` - Pre-extracted metadata
- `analysis/phase0_analysis.md` - Initial analysis report
- `original_files/[filename]` - Original media file

### Generated Files
- `TICKET_SUMMARY.md` - Complete resolution index
- `metadata/ticket_metadata.json` - Ticket info
- `metadata/timeline.json` - Event timeline

### Customer History
- Entry added to `customers/[WebEDI-ID]_[Company].md`
- Includes Phase 0 confidence score
- Links to resolution folder

---

## What You Need to Add Manually

### Investigation Artifacts
- `analysis/investigation_report.md` - Save Investigation PRD
- `investigation/notebooklm_queries.md` - Save all queries and responses
- `investigation/investigation_notes.md` - Working notes (optional)
- `investigation/evidence.md` - Supporting evidence (optional)

### Resolution Artifacts
- `resolution/customer_response.md` - Customer-facing response
- `resolution/internal_notes.md` - Team notes
- `resolution/verification_checklist.md` - Copy and fill out template
- `resolution/resolution_summary.md` - Executive summary (optional)

---

## Verification Checklist (Essential Checks Only)

### Before QA Handoff

- [ ] Archive script ran successfully
- [ ] TICKET_SUMMARY.md exists and is complete
- [ ] Investigation report saved
- [ ] Customer response saved
- [ ] Verification checklist 100% complete
- [ ] Customer history updated
- [ ] All subdirectories present
- [ ] File count matches TICKET_SUMMARY.md
- [ ] No Phase 0 artifacts missing (if applicable)
- [ ] No broken links in TICKET_SUMMARY.md

**Full Checklist:** 81+ points in verification_checklist.md

---

## Common Issues

### Issue: Phase 0 artifacts not found

**Message:**
```
[!] Warning: Phase 0 artifacts not found for ticket 13624970
```

**Resolution:**
- Normal if ticket didn't go through Phase 0
- Script continues successfully
- TICKET_SUMMARY.md shows "Unknown" for Phase 0 data
- No action needed - proceed with investigation artifacts

### Issue: Script fails with argument error

**Resolution:**
- Check company name has quotes: `"Singtech Inc"` not `Singtech Inc`
- Check all required arguments present: ticket-id, webedi-id, company
- Verify Python 3.8+ installed: `python --version`

### Issue: TICKET_SUMMARY.md has many placeholders

**Resolution:**
- Normal before saving investigation artifacts
- Complete investigation phase
- Save all artifacts to resolution folder
- TICKET_SUMMARY.md reflects available data only

---

## Time Budget

**Total Phase 7 Time:** ~5 minutes

- Run archive script: 30 seconds
- Save investigation artifacts: 1 minute
- Save resolution artifacts: 1 minute
- Copy and fill verification checklist: 2 minutes
- Review TICKET_SUMMARY.md: 30 seconds

**vs Manual Method:** ~10 minutes
**Time Saved:** ~5 minutes per ticket

---

## Quality Standards

### TICKET_SUMMARY.md
- Minimal placeholders (< 20% of fields)
- All available data filled in
- Links work correctly
- File count accurate

### Verification Checklist
- All 81+ checks completed
- Sign-off sections filled
- Performance metrics documented
- Issues section filled if any problems

### Customer History
- Entry added with date
- Phase 0 confidence included
- Resolution folder link correct
- Patterns identified documented

---

## Help and Documentation

### Quick Help
```bash
python archive_ticket.py --help
```

### Full Documentation
```bash
cat "C:\Users\sleep\.claude\skills\media-analysis\PHASE7_DOCUMENTATION_SPECIALIST_ENHANCED.md"
```

### Verification Checklist Template
```bash
cat "C:\Users\sleep\.claude\skills\media-analysis\templates\DOCUMENTATION_SPECIALIST_VERIFICATION_CHECKLIST.md"
```

### Complete Workflow
```bash
cat "C:\Users\sleep\.claude\commands\bmadedi.md" | grep -A 200 "PHASE 7"
```

---

## Key Reminders

1. **ALWAYS use automated script** - Ensures consistency
2. **Review TICKET_SUMMARY.md** - Before QA handoff
3. **Complete ALL checklist items** - 81+ required
4. **Phase 0 artifacts valuable** - Even if low confidence
5. **Enhanced structure mandatory** - All 5 subdirectories
6. **Customer history must be updated** - Include Phase 0 metrics

---

## Hand-Off to QA-Validator

When ready for QA validation, provide:

1. **Resolution folder path:**
   ```
   C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]
   ```

2. **TICKET_SUMMARY.md status:**
   - Completeness: [X]% filled
   - Placeholders: [X] remaining
   - File count: [X] files

3. **Verification checklist status:**
   - Completed: [X]/81+ checks
   - Issues found: [X] (list in checklist)
   - Sign-off: Ready/Not Ready

4. **Customer history:**
   - Updated: Yes/No
   - Phase 0 confidence: [0.XX]
   - Resolution link: Correct/Incorrect

---

**Quick Reference Version:** 1.0
**Last Updated:** 2025-10-29
**Generated by:** BMAD-EDI v4.0 Documentation Specialist Enhancement

---

## One-Command Quick Start

For fastest workflow, use this single command:

```bash
# Archive ticket (replace values)
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  [ticket-id] [webedi-id] "[Company]" \
  --trading-partner "[Partner]" \
  --resolution-type "fixed" && \
echo "[+] Archive complete. Now save investigation and resolution artifacts."
```

Then save your artifacts and complete the verification checklist.

**That's it!**
