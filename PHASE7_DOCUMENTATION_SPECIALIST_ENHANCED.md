# PHASE 7: FILE ORGANIZATION & ARCHIVING (Documentation Specialist Agent)
## ENHANCED FOR BMAD-EDI v4.0

**ENHANCED: Now includes Phase 0 analysis archival for complete audit trail**

**Automatic file organization after ticket resolution:**

## RECOMMENDED METHOD: Automated Archival Script

Use the enhanced archival automation script for consistent, comprehensive archival:

```bash
# Run automated enhanced archival script
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  [ticket-id] [WebEDI-ID] "[Company_Name]" \
  --trading-partner "[Partner_Name]" \
  --resolution-type "fixed"

# Example:
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  13624970 5124 "Singtech Inc" \
  --trading-partner "Target" \
  --resolution-type "fixed"
```

### What Automated Archival Does

The archive_ticket.py script handles complete resolution package creation:

1. **Creates enhanced resolution folder structure:**
   - `resolution/[WebEDI-ID]_[Company_Name]/`
   - Subdirectories: original_files/, analysis/, investigation/, resolution/, metadata/

2. **Archives Phase 0 artifacts:**
   - `analysis/phase0_metadata.json` (metadata from Gemini/OCR)
   - `analysis/phase0_analysis.md` (initial analysis report)
   - `original_files/[filename]` (original media file)

3. **Archives investigation artifacts (when available):**
   - `investigation/investigation_report.md`
   - `investigation/notebooklm_queries.md`
   - `investigation/root_cause_analysis.md`

4. **Generates comprehensive documentation:**
   - `TICKET_SUMMARY.md` (complete index with all metadata)
   - `metadata/ticket_metadata.json`
   - `metadata/timeline.json`

5. **Updates customer history:**
   - Appends ticket entry to `customers/[WebEDI-ID]_[Company_Name].md`

### Benefits of Automated Archival

- [+] Complete audit trail from Phase 0 to resolution
- [+] Standardized folder structure (no manual errors)
- [+] Comprehensive TICKET_SUMMARY.md index
- [+] Automatic metadata generation
- [+] Customer history integration
- [+] Quality metrics tracking
- [+] Time savings (30 seconds vs 5 minutes manual)

### Enhanced Resolution Folder Structure

```
resolution/
└── [WebEDI-ID]_[Company_Name]/
    ├── TICKET_SUMMARY.md (Complete index - QUICK REFERENCE)
    │
    ├── original_files/
    │   ├── [original_filename].pdf/png/mp3/mp4
    │   └── [Any additional files from customer]
    │
    ├── analysis/
    │   ├── phase0_metadata.json (Phase 0 pre-extracted data)
    │   ├── phase0_analysis.md (Phase 0 full analysis)
    │   ├── investigation_report.md (Phase 5 investigation PRD)
    │   └── root_cause_analysis.md (Detailed RCA)
    │
    ├── investigation/
    │   ├── notebooklm_queries.md (All queries and responses)
    │   ├── investigation_notes.md (Working notes)
    │   └── evidence.md (Supporting evidence)
    │
    ├── resolution/
    │   ├── customer_response.md (Customer-facing response)
    │   ├── internal_notes.md (Team notes)
    │   ├── verification_checklist.md (QA checklist - Phase 8)
    │   └── resolution_summary.md (Executive summary)
    │
    └── metadata/
        ├── ticket_metadata.json (Complete ticket info)
        ├── timeline.json (Structured timeline)
        └── quality_metrics.json (Performance data)
```

## TICKET_SUMMARY.md - Your Quick Reference Index

The auto-generated TICKET_SUMMARY.md provides instant access to:

- **Quick Reference**: Ticket ID, customer, partner, severity, issue
- **Phase 0 Results**: Extraction method, confidence, pre-extracted metadata
- **Investigation Summary**: Root cause, resolution, time metrics
- **Resolution Details**: Customer notification, resolution type, timeline
- **Files Index**: Complete list of all archived files by category
- **Timeline**: Chronological event log from receipt to archive
- **Quality Metrics**: Phase 0 accuracy, investigation efficiency, time saved
- **Patterns**: Identified patterns and lessons learned

### Example TICKET_SUMMARY.md Snippet

```markdown
# Ticket Summary: 13624970

**Generated:** 2025-10-29 14:30:00
**Status:** RESOLVED
**Duration:** 45 minutes

## Quick Reference

**Ticket ID:** 13624970
**Customer:** Singtech Inc
**WebEDI ID:** 5124
**Trading Partner:** Target
**Transaction Type:** 850 PO
**Severity:** High
**Issue:** 997 FA rejection on TD5 segment

## Phase 0 Analysis Results

**Method:** Gemini 2.5 Pro + PaddleOCR
**Confidence:** 0.92 (HIGH)
**Extracted:** 2025-10-29T13:15:00Z

**Pre-Extracted Metadata:**
- Ticket ID: 13624970
- Company: Singtech Inc
- Trading Partner: Target
- Transaction Type: 850 PO
- Severity: High

**Files:**
- Original: `original_files/2025-10-29_13624970_Singtech.pdf`
- Metadata: `analysis/phase0_metadata.json`
- Analysis: `analysis/phase0_analysis.md`

## Investigation Summary

**Lead Investigator:** Claude (BMAD-EDI v4.0)
**Investigation Time:** 45 seconds
**Root Cause:** Missing qualifier in TD5 segment
**Resolution:** Updated WebEDI mapper to include required TD5-01 qualifier

**Files:**
- Investigation Report: `investigation/investigation_report.md`
- NotebookLM Queries: `investigation/notebooklm_queries.md`

## Resolution Details

**Resolved:** 2025-10-29
**Resolution Type:** fixed
**Customer Notified:** 2025-10-29

**Files:**
- Customer Response: `resolution/customer_response.md`
- Internal Notes: `resolution/internal_notes.md`
- Verification: `resolution/verification_checklist.md`

## Quality Metrics

### Phase 0 Performance
- **Extraction Accuracy:** 100%
- **Time Saved:** 3 minutes (vs manual)
- **Fields Extracted:** 12/12
- **OCR Fallback Used:** No

### Investigation Performance
- **Questions Asked:** 3 (vs standard 8-15)
- **Queries Executed:** 1
- **Investigation Time:** 45 seconds
- **Confidence Level:** 0.95
- **NotebookLM Sources:** 3

### Overall Efficiency
- **Total Time (Phase 0 + Investigation):** 4 minutes
- **Time Savings vs Manual:** 8 minutes
```

## Archive Script Options

### Resolution Types

Use `--resolution-type` to categorize resolution:

- **fixed**: Issue resolved completely (default)
- **workaround**: Temporary solution provided
- **duplicate**: Duplicate of another ticket
- **escalated**: Escalated to engineering
- **no-issue**: No issue found

### Examples

```bash
# Standard resolution
python archive_ticket.py 13624970 5124 "Singtech Inc" \
  --trading-partner "Target" \
  --resolution-type "fixed"

# Workaround provided
python archive_ticket.py 13620086 5124 "Singtech Inc" \
  --trading-partner "Target" \
  --resolution-type "workaround"

# Escalated ticket
python archive_ticket.py 13625000 4719 "Werk-Brau Co Inc" \
  --trading-partner "Walmart" \
  --resolution-type "escalated"
```

## ALTERNATIVE METHOD: Manual Archival (Legacy)

If automated script unavailable, use manual method:

### Step 1: Create Customer Folder (if needed)

```bash
# Check if folder exists
ls "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]"

# If not exists, create enhanced structure
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]"
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\original_files"
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis"
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\investigation"
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\resolution"
mkdir "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\metadata"
```

### Step 2: Archive Phase 0 Artifacts (IMPORTANT - NEW)

```bash
# Find Phase 0 processing folder
ls "C:\Users\sleep\Documents\tickets\processing\*[ticket-id]*"

# Copy Phase 0 metadata
cp "C:\Users\sleep\Documents\tickets\processing\[processing-folder]\metadata.json" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis\phase0_metadata.json"

# Copy Phase 0 analysis
cp "C:\Users\sleep\Documents\tickets\processing\[processing-folder]\*_analysis.md" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis\phase0_analysis.md"

# Copy original media file
cp "C:\Users\sleep\Documents\tickets\processing\[processing-folder]\[original-file].*" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\original_files\"
```

### Step 3: Move Files from incoming/ (if applicable)

```bash
# Move ticket PDF (if still in incoming/)
mv "C:\Users\sleep\Documents\tickets\incoming\[ticket-id]_[company].pdf" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\original_files\ticket_[ticket-id].pdf"

# Move audio (if exists)
mv "C:\Users\sleep\Documents\tickets\incoming\recording_[ticket-id].mp3" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\original_files\audio_[ticket-id].mp3"

# Move screenshots (if exist)
mv "C:\Users\sleep\Documents\tickets\incoming\screenshot_[ticket-id]_*.png" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\original_files\"
```

### Step 4: Save Investigation Artifacts

```bash
# Save Investigation PRD as investigation_report.md
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis\investigation_report.md"

# Save NotebookLM queries
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\investigation\notebooklm_queries.md"
```

### Step 5: Save Resolution Artifacts

```bash
# Save customer response
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\resolution\customer_response.md"

# Save internal notes
Write: "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\resolution\internal_notes.md"
```

### Step 6: Update Customer History

Create or update: `customers/[WebEDI-ID]_[Company_Name].md`

Add ticket entry:

```markdown
### Ticket #[ID] - [YYYY-MM-DD]
**Status**: Resolved
**Scale**: [L0/L1/L2/L3/L4]
**Complexity**: [Score 0-8]

**Summary**: [Brief description]
**Root Cause**: [Technical summary]
**Resolution**: [What was done]
**Time**: [Investigation time]
**Phase 0 Confidence**: [0.XX] ([extraction_method])

**Documents**:
- Phase 0 Analysis: resolution/[folder]/analysis/phase0_analysis.md
- Investigation PRD: resolution/[folder]/analysis/investigation_report.md
- Customer Response: resolution/[folder]/resolution/customer_response.md
- TICKET_SUMMARY: resolution/[folder]/TICKET_SUMMARY.md

**Patterns Identified**:
- [Pattern 1]

**Lessons Learned**:
- [Lesson 1]
```

### Step 7: Update Customer Index

Update: `customers/CUSTOMER_INDEX.md`

### Step 8: Enhanced Verification Checklist

Use the comprehensive checklist template:

```bash
# Copy verification checklist template
cp "C:\Users\sleep\.claude\skills\media-analysis\templates\DOCUMENTATION_SPECIALIST_VERIFICATION_CHECKLIST.md" \
   "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\resolution\verification_checklist.md"
```

Fill out all sections:
- [ ] Phase 0 artifacts archived
- [ ] Investigation artifacts archived
- [ ] Resolution artifacts archived
- [ ] Metadata files created
- [ ] TICKET_SUMMARY.md index created
- [ ] Customer history updated
- [ ] Customer index updated
- [ ] File organization complete
- [ ] Quality checks passed
- [ ] Ready for QA validation

## Verification Checklist (Enhanced)

### Phase 0 Artifacts
- [ ] Original media file archived (`original_files/`)
- [ ] Phase 0 metadata JSON archived (`analysis/phase0_metadata.json`)
- [ ] Phase 0 analysis markdown archived (`analysis/phase0_analysis.md`)
- [ ] Confidence score documented
- [ ] OCR extraction archived (if used)

### Investigation Artifacts
- [ ] Investigation report archived (`investigation/investigation_report.md`)
- [ ] NotebookLM queries archived (`investigation/notebooklm_queries.md`)
- [ ] Root cause analysis archived (`investigation/root_cause_analysis.md`)
- [ ] Timeline documented

### Resolution Artifacts
- [ ] Customer response drafted (`resolution/customer_response.md`)
- [ ] Internal notes documented (`resolution/internal_notes.md`)
- [ ] Verification checklist completed (`resolution/verification_checklist.md`)
- [ ] Resolution summary created

### Metadata and Index
- [ ] TICKET_SUMMARY.md created (root of resolution folder)
- [ ] Ticket metadata JSON created (`metadata/ticket_metadata.json`)
- [ ] Timeline JSON created (`metadata/timeline.json`)
- [ ] All files listed in index
- [ ] Links to related resources added

### Customer History
- [ ] Customer history file updated
- [ ] Phase 0 analysis results documented
- [ ] Resolution folder link added
- [ ] Customer index updated

### Final Checks
- [ ] All files copied successfully (no corruption)
- [ ] File permissions correct (readable)
- [ ] Folder structure complete
- [ ] Total file count documented
- [ ] Resolution package tested (can be accessed)
- [ ] Incoming folder cleaned (files removed from processing/)

## Why Archive Phase 0 Data?

### 1. Complete Audit Trail
- Track extraction accuracy over time
- Document confidence scores and methods
- Verify automated analysis quality
- Compliance and quality assurance

### 2. Knowledge Base Growth
- Build dataset for future training
- Identify patterns in ticket types
- Improve extraction algorithms
- Benchmark automation effectiveness

### 3. Quality Metrics
- Monitor automation success rate
- Track time savings from Phase 0
- Identify improvement opportunities
- Compare Gemini vs OCR performance

### 4. Debugging & Troubleshooting
- Diagnose extraction failures
- Root cause analysis for errors
- Identify problematic file types
- Improve future accuracy

## Troubleshooting

### Issue: Phase 0 artifacts not found

**Symptom:**
```
[!] Warning: Phase 0 artifacts not found for ticket 13624970
```

**Causes:**
- Ticket didn't go through Phase 0 media analysis
- Processing folder was manually cleaned
- File watcher service wasn't running

**Solutions:**
1. Check if `processing/[ticket-id]/` folder exists
2. Verify media-analysis watcher service is running
3. Script continues but skips Phase 0 archival (safe fallback)
4. Manually create artifacts if needed

### Issue: Archive script fails

**Symptom:**
Script exits with error or creates incomplete structure

**Solutions:**
1. Check Python environment: `python --version`
2. Verify tickets directory exists: `ls ~/Documents/tickets`
3. Check permissions on resolution folder
4. Run with verbose output to see specific error
5. Fall back to manual archival method

### Issue: TICKET_SUMMARY.md missing data

**Symptom:**
Many fields show "N/A" or placeholders

**Causes:**
- Phase 0 metadata incomplete
- Investigation artifacts not saved yet
- Template variables not replaced

**Solutions:**
1. Complete investigation before archiving
2. Save investigation report to resolution folder
3. Re-run archive script after investigation complete
4. Manually update TICKET_SUMMARY.md if needed

## Performance Metrics

### Time Savings with Enhanced Archival
- **Manual extraction + manual archival:** ~10 minutes per ticket
- **Phase 0 + automated archival:** ~1 minute
- **Time saved:** ~9 minutes per ticket
- **Annual savings (10 tickets/day):** ~375 hours/year

### Quality Improvements
- **Complete audit trail:** 100% of tickets (vs 20% manual)
- **Phase 0 accuracy tracking:** Automated
- **Pattern detection:** Enabled by archived metrics
- **Continuous improvement:** Data-driven

## Quick Reference Commands

```bash
# Archive completed ticket (recommended)
python "C:\Users\sleep\.claude\skills\media-analysis\archive_ticket.py" \
  [ticket-id] [webedi-id] "[company-name]" \
  --trading-partner "[partner]" \
  --resolution-type "fixed"

# View resolution summary
cat "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\TICKET_SUMMARY.md"

# View Phase 0 metadata
cat "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis\phase0_metadata.json"

# View Phase 0 analysis
cat "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]\analysis\phase0_analysis.md"

# Check folder structure
ls -R "C:\Users\sleep\Documents\tickets\resolution\[WebEDI-ID]_[Company_Name]"

# Verify customer history updated
cat "C:\Users\sleep\Documents\tickets\customers\[WebEDI-ID]_[Company_Name].md"
```

---

**Documentation Specialist agents should ALWAYS use automated archival script (archive_ticket.py) during Phase 7 to ensure complete audit trail, standardized structure, and knowledge base growth.**

**Key Reminder:** The TICKET_SUMMARY.md file is your quick reference index for the entire resolution package. Review it before handing off to QA-Validator to ensure all artifacts are properly archived.
