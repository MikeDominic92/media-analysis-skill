# Phase 0 Quick Reference Card

**BMAD-EDI Workflow Integration - Phase 0 (Pre-Investigation Analysis)**

## Quick Start

```bash
# 1. Authenticate (one-time)
cd C:\Users\sleep\.claude\skills\media-analysis
python gemini_analyzer.py auth

# 2. Place ticket in incoming
cp ticket.pdf C:\Users\sleep\Documents\tickets\incoming\

# 3. Process ticket (manual)
python workflow.py C:\Users\sleep\Documents\tickets\incoming\ticket.pdf

# 4. OR enable auto-watcher
python watch-incoming.py
```

## What Phase 0 Does

1. Detects ticket file in incoming/
2. Extracts metadata with Gemini 2.5 Pro
3. Falls back to OCR if confidence < 0.70
4. Generates standardized filename
5. Creates processing/ticket_{id}/ folder
6. Saves metadata.json + preliminary_analysis.md
7. Removes file from incoming/
8. Status: READY FOR ANALYST

**Time:** < 90 seconds | **Confidence Target:** >= 0.85

## Confidence Levels

| Confidence | Label | Analyst Action |
|------------|-------|----------------|
| >= 0.85 | HIGH | ACCEPT (use as-is) |
| 0.70-0.84 | MEDIUM | VERIFY (quick review) |
| < 0.70 | LOW | OVERRIDE (manual extraction) |

## Artifacts Generated

**metadata.json** - Structured metadata for Analyst
```json
{
  "ticket_id": "13624970",
  "company": "Ace Hardware Supply Co.",
  "trading_partner": "Home Depot",
  "transaction_type": "856 ASN",
  "severity": "HIGH",
  "issue_title": "856 ASN Rejection - Invalid SCAC Code",
  "root_cause": "Missing carrier SCAC code",
  "confidence": 0.92,
  "extraction_method": "gemini"
}
```

**preliminary_analysis.md** - Human-readable summary
- Ticket overview
- Issue summary
- Root cause
- Recommended actions
- Next steps

## Analyst Integration

**Step 1: Check for metadata**
```bash
METADATA_FILE="C:\Users\sleep\Documents\tickets\processing\ticket_{id}\metadata.json"
if [ -f "$METADATA_FILE" ]; then
    # Load metadata
    CONFIDENCE=$(jq -r '.confidence' "$METADATA_FILE")
fi
```

**Step 2: Load and verify**
```python
import json
with open(metadata_file, 'r') as f:
    metadata = json.load(f)

confidence = metadata['confidence']
if confidence >= 0.85:
    action = "ACCEPT"
elif confidence >= 0.70:
    action = "VERIFY"
else:
    action = "OVERRIDE"
```

**Step 3: Use metadata**
- ACCEPT: Use pre-extracted data, proceed to Phase 2
- VERIFY: Quick review, make corrections, proceed to Phase 2
- OVERRIDE: Manual extraction with metadata hints

## Directory Structure

```
C:\Users\sleep\Documents\tickets\
├── incoming/               # Phase 0 input
│   ├── failed/            # Failed extractions + error reports
│   └── [raw-files]
├── processing/            # Phase 0 output / Phase 1 input
│   └── ticket_{id}/
│       ├── metadata.json
│       ├── preliminary_analysis.md
│       └── [standardized-filename].pdf
└── media-analysis.log     # Phase 0 processing log
```

## Filename Format

**Pattern:** `YYYY-MM-DD_{ticket-id}_{company}_TradingPartner-{partner}_{transaction}.ext`

**Example:** `2025-10-29_13624970_AceHardware_TradingPartner-HomeDepot_856-ASN.pdf`

## Testing

```bash
# Test Phase 0
python test_phase0.py

# Test with specific file
python test_phase0.py C:\path\to\ticket.pdf

# Check results
ls C:\Users\sleep\Documents\tickets\processing\
cat C:\Users\sleep\Documents\tickets\processing\ticket_*/metadata.json
```

## Troubleshooting

**No metadata.json:**
- Check: incoming/failed/ for error reports
- Review: media-analysis.log for details
- Try: Manual extraction (Phase 1 traditional workflow)

**Low confidence (<0.70):**
- Phase 0 triggered OCR fallback automatically
- Check: preliminary_analysis.md for hints
- Recommend: OVERRIDE (manual extraction)

**Gemini authentication expired:**
```bash
python gemini_analyzer.py auth
```

**Processing takes too long:**
- Normal: 30-60 seconds (Gemini)
- With OCR: +20-30 seconds
- If > 90 seconds: Check network connection

## Time Savings

| Scenario | Without Phase 0 | With Phase 0 | Saved |
|----------|----------------|--------------|-------|
| HIGH confidence | 12-14 min | 5 min | 7-9 min (50-64%) |
| MEDIUM confidence | 12-14 min | 7 min | 5-7 min (36-50%) |
| LOW confidence | 12-14 min | 10 min | 2-4 min (14-29%) |

**Annual Savings (10 tickets/day):** 300-390 hours/year

## Key Files

| File | Purpose |
|------|---------|
| workflow.py | Phase 0 implementation |
| test_phase0.py | Verification test script |
| PHASE0_INTEGRATION.md | Complete integration guide |
| ANALYST_INTEGRATION_GUIDE.md | Phase 1 workflow updates |
| BMADEDI_UPDATES.md | Manual bmadedi.md updates |
| AGENT6_COMPLETION_REPORT.md | Full mission report |

## Support

**Documentation:** See files in `C:\Users\sleep\.claude\skills\media-analysis\`

**Logs:** `C:\Users\sleep\Documents\tickets\media-analysis.log`

**Failed Extractions:** `C:\Users\sleep\Documents\tickets\incoming\failed\`

**Test:** `python test_phase0.py`

## Success Criteria

- [X] File automatically analyzed
- [X] Confidence > 0.85
- [X] Processing < 90 seconds
- [X] metadata.json created
- [X] preliminary_analysis.md created
- [X] File moved to processing/
- [X] Ready for Analyst within 2 minutes

---

**Agent 6 - BMAD-EDI Workflow Integration Specialist**
**Phase 0 Integration Complete**
**2025-10-29**
