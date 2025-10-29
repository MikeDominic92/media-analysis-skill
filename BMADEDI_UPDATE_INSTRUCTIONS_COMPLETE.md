# bmadedi.md Update Instructions - Phase 0 Integration

**Quick Reference for Manual Updates**

## Location 1: Add Phase 0 Section

**Insert AFTER line 100:** `## COMPLETE WORKFLOW`
**Insert BEFORE:** `### PHASE 1: TICKET EXTRACTION (Analyst Agent)`

```markdown
### PHASE 0: PRE-INVESTIGATION ANALYSIS (AUTOMATED)

**Trigger:** Automatic (file placed in incoming/ folder)
**Agent:** Media Analysis Skill (Gemini 2.5 Pro + PaddleOCR)
**Input:** Raw ticket file (PDF, image, audio, video)
**Output:** Pre-extracted metadata + preliminary analysis
**Time:** 30-90 seconds per file

**Process:**

1. **File Detection:** File appears in `C:\Users\sleep\Documents\tickets\incoming\`
2. **Gemini Analysis:** Extract metadata using Gemini 2.5 Pro multimodal analysis
3. **Confidence Check:** If confidence < 0.70, trigger OCR fallback
4. **Metadata Extraction:**
   - Ticket ID, Customer Name, Company Name
   - Trading Partner, Transaction Type
   - Message ID, Severity, Issue Title
   - Root Cause (preliminary), Recommended Actions
5. **Generate Artifacts:**
   - metadata.json (structured data)
   - preliminary_analysis.md (human-readable)
6. **Standardize Filename:** YYYY-MM-DD_{ticket-id}_{company}_TradingPartner-{partner}_{transaction}.ext
7. **Move to Processing:** Create processing/ticket_{id}/ folder
8. **Status:** READY FOR ANALYST VERIFICATION

**Confidence Thresholds:**
- >= 0.85 (HIGH): Accept as-is, proceed immediately
- 0.70-0.84 (MEDIUM): Analyst verification recommended
- < 0.70 (LOW): Manual extraction required

**Manual Trigger:**
```bash
cd "C:\Users\sleep\.claude\skills\media-analysis"
python workflow.py "C:\Users\sleep\Documents\tickets\incoming\ticket.pdf"
```

**Output Structure:**
```
processing/ticket_{id}/
├── metadata.json                    # Structured metadata
├── preliminary_analysis.md          # Human-readable summary
└── [standardized-filename]          # Processed file
```

**Time Savings:**
- HIGH confidence: 5-10 minutes saved
- MEDIUM confidence: 3-5 minutes saved
- LOW confidence: 1-2 minutes saved

**Manual Override:** Analyst can always perform manual extraction regardless of confidence

---
```

## Location 2: Update Phase 1 Analyst Section

**Insert AFTER:** `### PHASE 1: TICKET EXTRACTION (Analyst Agent)`
**Insert BEFORE:** `**FIRST OUTPUT - Copy-Paste Ready Format:**`

```markdown
**Step 0: Check for Phase 0 Metadata (NEW)**

Before manual extraction, check if Phase 0 has processed the ticket:

```bash
# Check for pre-extracted metadata
TICKET_FOLDER="C:\Users\sleep\Documents\tickets\processing\ticket_{id}"
METADATA_FILE="$TICKET_FOLDER\metadata.json"

if [ -f "$METADATA_FILE" ]; then
    echo "[+] Phase 0 metadata available"
    CONFIDENCE=$(jq -r '.confidence' "$METADATA_FILE")

    if confidence >= 0.85:
        echo "[+] HIGH CONFIDENCE - Ready to proceed"
        ACTION="ACCEPT"
    elif confidence >= 0.70:
        echo "[!] MEDIUM CONFIDENCE - Verification recommended"
        ACTION="VERIFY"
    else:
        echo "[!] LOW CONFIDENCE - Manual extraction required"
        ACTION="OVERRIDE"
    fi
else
    echo "[!] No Phase 0 metadata - Manual extraction"
fi
```

**Analyst Options:**

1. **ACCEPT (High Confidence >= 0.85):**
   - Use pre-extracted metadata as-is
   - Skip manual extraction entirely
   - Proceed directly to formatted output
   - Time saved: 5-10 minutes

2. **VERIFY (Medium Confidence 0.70-0.84):**
   - Review preliminary_analysis.md
   - Cross-check key fields
   - Make corrections if needed
   - Time saved: 3-5 minutes

3. **OVERRIDE (Low Confidence < 0.70):**
   - Use Phase 0 metadata as hints
   - Perform complete manual extraction
   - Time saved: 1-2 minutes

**Display Pre-Extracted Data:**

```
================================================================================
[PHASE 0 COMPLETE - METADATA AVAILABLE]
================================================================================

Ticket: {ticket_id}
File: {processed_file}
Confidence: {confidence:.2%} (HIGH|MEDIUM|LOW)
Extraction Method: {GEMINI|OCR|HYBRID}

Pre-Extracted Metadata:
✓ Customer: {customer_name}
✓ Company: {company}
✓ Trading Partner: {trading_partner}
✓ Transaction: {transaction_type}
✓ Message ID: {message_id}
✓ Severity: {severity}
✓ Issue: {issue_title}

Root Cause:
{root_cause}

Recommended Actions:
1. {action_1}
2. {action_2}

================================================================================
[ANALYST OPTIONS]
================================================================================

1. ACCEPT → Use pre-extracted data as-is
2. VERIFY → Review and correct metadata
3. OVERRIDE → Perform manual extraction

[ACTION]: _
```

```

## Location 3: Update Workflow Diagrams

**Find and replace in Scale Assessment section:**

**OLD:**
```
L0: Quick Query → NotebookLM → Answer → Document
L1: Analyst → PM-Investigator → Investigator (NotebookLM) → Documentation Specialist
L2+: Full agent pipeline + Story tracking + NotebookLM verification
```

**NEW:**
```
L0: Quick Query → Phase 0 (if file) → NotebookLM → Answer → Document
L1: Phase 0 → Analyst (verify) → PM-Investigator → Investigator (NotebookLM) → Documentation Specialist
L2+: Phase 0 → Full agent pipeline + Story tracking + NotebookLM verification
```

## Location 4: Update File Structure Section

**Find section:** `## FILE STRUCTURE` (around line 45)

**Update incoming/ folder description:**

**OLD:**
```
├── incoming/                              # ACTIVE tickets (unresolved)
│   ├── [ticket-id]_[company].pdf         # Example: 13620086_Singtech.pdf
│   ├── recording_[ticket-id].mp3         # Audio files
│   └── screenshot_[ticket-id]_desc.png   # Screenshots
```

**NEW:**
```
├── incoming/                              # RAW tickets (awaiting Phase 0)
│   ├── failed/                           # Failed Phase 0 extractions
│   ├── [ticket-id]_[company].pdf         # Example: 13620086_Singtech.pdf
│   ├── recording_[ticket-id].mp3         # Audio files
│   └── screenshot_[ticket-id]_desc.png   # Screenshots
```

**Add processing/ folder (insert after incoming/):**

```
├── processing/                            # ACTIVE investigations (post-Phase 0)
│   └── ticket_{id}/                      # Per-ticket folder
│       ├── metadata.json                 # Phase 0 extracted metadata
│       ├── preliminary_analysis.md       # Phase 0 analysis
│       └── [standardized-filename]       # Processed ticket file
```

## Testing After Updates

1. **Verify bmadedi.md syntax:**
```bash
# Check for markdown errors
cat "C:\Users\sleep\.claude\commands\bmadedi.md" | grep "PHASE 0"
```

2. **Test Phase 0 processing:**
```bash
cd "C:\Users\sleep\.claude\skills\media-analysis"
python test_phase0.py
```

3. **Verify /bmadedi command:**
```bash
# In Claude Code, type:
/bmadedi
# Should now show Phase 0 in workflow
```

## Quick Summary

**3 Main Changes:**
1. Add Phase 0 section (automated pre-analysis)
2. Update Phase 1 Analyst section (metadata consumption)
3. Update workflow diagrams (include Phase 0)

**Time to Complete:** 5-10 minutes

**Files to Update:** 1 file (bmadedi.md)

**Testing Required:** Yes (test_phase0.py)

**Impact:** 70-80% faster ticket processing for high-confidence extractions

---

**Reference Documents:**
- Complete implementation: `workflow.py`
- Testing script: `test_phase0.py`
- Full integration guide: `PHASE0_INTEGRATION.md`
- Analyst workflow guide: `ANALYST_INTEGRATION_GUIDE.md`
- Completion report: `PHASE3_AGENT1_COMPLETION_REPORT.md`
