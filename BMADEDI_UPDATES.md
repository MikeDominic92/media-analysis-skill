# bmadedi.md Manual Update Instructions

**Agent 6 - BMAD-EDI Workflow Integration Specialist**

This document contains the exact text to be inserted into `C:\Users\sleep\.claude\commands\bmadedi.md` to add Phase 0 support.

## Update 1: Insert Phase 0 Section

**Location:** After line 100, before "### PHASE 1: TICKET EXTRACTION (Analyst Agent)"

**Insert the following text:**

```markdown
### PHASE 0: PRE-INVESTIGATION ANALYSIS (AUTOMATED)

**Trigger:** Automatic (via file hooks or watcher)
**Agent:** Media Analysis Skill (Gemini + OCR)
**Input:** Raw ticket file in `incoming/`
**Output:** Pre-extracted metadata + preliminary analysis

#### Workflow

```
File placed in incoming/
    ↓
[Detect file type: PDF, image, audio, video]
    ↓
[Route to appropriate analyzer:]
  - Gemini (multimodal analysis)
  - OCR (text extraction fallback)
  - Hybrid (Gemini + OCR)
    ↓
[Extract EDI metadata:]
  - Ticket ID
  - Company name
  - Trading partner
  - Transaction type (850, 856, 810, etc.)
  - Error codes
  - Severity (HIGH, MEDIUM, LOW)
    ↓
[Generate artifacts:]
  - metadata.json (for Analyst agent)
  - preliminary_analysis.md (human-readable)
    ↓
[Move file to processing/ with standardized name]
    ↓
[Status: READY FOR ANALYST]
```

#### Artifacts Generated

**1. metadata.json** - Location: `processing/ticket_{id}/metadata.json`

Contains structured metadata:
- ticket_id, customer_name, company
- trading_partner, transaction_type, message_id
- severity, issue_title, root_cause
- recommended_actions (list)
- confidence (0.0-1.0), extraction_method (gemini/ocr/hybrid)
- timestamp, original_file, processed_file

**2. preliminary_analysis.md** - Location: `processing/ticket_{id}/preliminary_analysis.md`

Human-readable markdown with:
- Ticket overview (customer, company, trading partner, transaction, severity)
- Issue summary and root cause analysis
- Recommended actions
- Next steps for Analyst/PM-Investigator/Investigator
- Extraction details (confidence, method, file names)

#### Integration with Phase 1 (Analyst)

**Enhanced Analyst workflow:**
```
[PHASE 0 COMPLETE - METADATA AVAILABLE]

Ticket: {ticket_id}
Confidence: {confidence:.2%}

Pre-Extracted Metadata:
✓ Customer: {customer_name}
✓ Company: {company}
✓ Trading Partner: {trading_partner}
✓ Transaction: {transaction_type}
✓ Severity: {severity}

[ANALYST OPTIONS]
1. ACCEPT → Use pre-extracted data (HIGH confidence >= 0.85)
2. VERIFY → Review and correct (MEDIUM confidence 0.70-0.84)
3. OVERRIDE → Manual extraction (LOW confidence < 0.70)
```

#### Confidence Thresholds

- **HIGH (>= 0.85):** Accept pre-extracted data, proceed immediately
- **MEDIUM (0.70-0.84):** Quick verification recommended
- **LOW (< 0.70):** OCR fallback triggered, manual extraction preferred

#### Success Criteria

- [ ] File automatically analyzed when placed in incoming/
- [ ] Metadata extraction confidence > 0.85
- [ ] Processing time < 90 seconds per file
- [ ] metadata.json created for Analyst
- [ ] preliminary_analysis.md human-readable
- [ ] File moved to processing/ folder

#### Error Handling

**If extraction fails:**
1. Log error to media-analysis.log
2. Move file to `incoming/failed/` folder
3. Create error report with details
4. Fallback to manual Analyst extraction

**If confidence < 0.70:**
1. OCR fallback triggered automatically (hybrid mode)
2. If still low confidence: Flag for manual verification
3. Analyst has final verification authority

#### Time Savings

- **Without Phase 0:** 12-14 minutes (manual extraction + history + spec check)
- **With Phase 0 (HIGH confidence):** 5 minutes (metadata acceptance + history + spec check)
- **Time Saved:** 7-9 minutes per ticket (50-64% faster)
- **Annual Savings (10 tickets/day):** 300-390 hours/year

---

```

## Update 2: Enhance Phase 1 Section

**Location:** After "### PHASE 1: TICKET EXTRACTION (Analyst Agent)" section header

**Insert the following text BEFORE "**FIRST OUTPUT - Copy-Paste Ready Format:**":**

```markdown

#### Step 1: Check for Phase 0 Metadata

**Before starting extraction, check if Phase 0 has already processed the ticket:**

```bash
# Define ticket processing folder
PROCESSING_DIR="C:\Users\sleep\Documents\tickets\processing"
TICKET_ID="[ticket-id]"  # Extract from context or user input
TICKET_FOLDER="$PROCESSING_DIR/ticket_$TICKET_ID"
METADATA_FILE="$TICKET_FOLDER/metadata.json"

# Check if Phase 0 metadata exists
if [ -f "$METADATA_FILE" ]; then
    echo "[+] Phase 0 metadata available"
    echo "[*] Loading pre-extracted data..."

    # Load confidence score
    CONFIDENCE=$(jq -r '.confidence' "$METADATA_FILE")
    echo "[*] Confidence: $CONFIDENCE"

    # Decision tree
    if (( $(echo "$CONFIDENCE >= 0.85" | bc -l) )); then
        echo "[+] HIGH CONFIDENCE - Ready to proceed"
        ACTION="ACCEPT"
    elif (( $(echo "$CONFIDENCE >= 0.70" | bc -l) )); then
        echo "[!] MEDIUM CONFIDENCE - Verification recommended"
        ACTION="VERIFY"
    else
        echo "[!] LOW CONFIDENCE - Manual extraction required"
        ACTION="OVERRIDE"
    fi
else
    echo "[!] No Phase 0 metadata found"
    echo "[*] Proceeding with manual extraction"
    ACTION="MANUAL"
fi
```

#### Step 2: Load Pre-Extracted Metadata (if available)

**If Phase 0 metadata exists, load and display for verification:**

```python
import json

# Load metadata
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Display pre-extracted data
print(f"""
================================================================================
[PHASE 0 COMPLETE - METADATA AVAILABLE]
================================================================================

Ticket: {metadata['ticket_id']}
File: {metadata['processed_file']}
Confidence: {metadata['confidence']:.2%} ({'HIGH' if metadata['confidence'] >= 0.85 else 'MEDIUM' if metadata['confidence'] >= 0.70 else 'LOW'})
Extraction Method: {metadata['extraction_method'].upper()}

Pre-Extracted Metadata:
✓ Customer: {metadata.get('customer_name', 'N/A')}
✓ Company: {metadata.get('company', 'N/A')}
✓ Trading Partner: {metadata.get('trading_partner', 'N/A')}
✓ Transaction: {metadata.get('transaction_type', 'N/A')}
✓ Message ID: {metadata.get('message_id', 'N/A')}
✓ Severity: {metadata.get('severity', 'NORMAL')}
✓ Issue: {metadata.get('issue_title', 'N/A')}

Root Cause:
{metadata.get('root_cause', 'Pending analysis')}

Recommended Actions:
""")

for i, action in enumerate(metadata.get('recommended_actions', []), 1):
    print(f"{i}. {action}")

print(f"""
================================================================================
[ANALYST OPTIONS]
================================================================================

1. ACCEPT → Use pre-extracted data as-is (HIGH confidence only)
2. VERIFY → Review and correct extracted data (MEDIUM/HIGH confidence)
3. OVERRIDE → Perform manual extraction (LOW confidence or user preference)

[ACTION]: {ACTION}
================================================================================
""")
```

#### Step 3: Handle Analyst Decision

**A. ACCEPT (High Confidence >= 0.85)**

Use pre-extracted metadata as-is and generate formatted output:

```python
# Use metadata directly
print("[+] Analyst accepted pre-extracted metadata")

# Generate formatted output (continue with existing FIRST OUTPUT format)
# ... (existing Phase 1 output format)
```

**B. VERIFY (Medium Confidence 0.70-0.84)**

Review preliminary_analysis.md, cross-check against ticket file, make corrections:

```python
print("[*] Analyst reviewing pre-extracted metadata for accuracy...")

# Read preliminary analysis for reference
analysis_file = Path(ticket_folder) / "preliminary_analysis.md"
if analysis_file.exists():
    with open(analysis_file, 'r', encoding='utf-8') as f:
        print(f.read())

# Analyst makes corrections, then generates formatted output
# ... (existing Phase 1 output format with corrections)
```

**C. OVERRIDE (Low Confidence < 0.70 or Manual Preference)**

Perform full manual extraction (use pre-extracted data as hints only):

```python
print("[!] Analyst performing manual extraction")
print("[*] Pre-extracted metadata available for reference:")
print(f"  [HINT] Possible ticket ID: {metadata.get('ticket_id', 'N/A')}")
print(f"  [HINT] Possible company: {metadata.get('company', 'N/A')}")
# ... etc

# Proceed with traditional manual extraction workflow
# ... (existing Phase 1 manual extraction)
```

---

```

## Update 3: Update MCP Tool Usage Section

**Location:** In "## MCP TOOL USAGE" section, before "### NotebookLM (via Skill)"

**Insert the following text:**

```markdown
### Media Analysis Skill (Phase 0 Only)
**AUTO-TRIGGERED** - Pre-investigation analysis

```bash
cd "C:\Users\sleep\.claude\skills\media-analysis" && \
python workflow.py "C:\Users\sleep\Documents\tickets\incoming\ticket.pdf"
```

**Features:**
- Gemini 2.5 Pro multimodal analysis
- PaddleOCR fallback for low confidence
- Hybrid mode (Gemini + OCR)
- Automated metadata extraction
- File organization (incoming → processing)
- metadata.json + preliminary_analysis.md generation

**Confidence Thresholds:**
- >= 0.85: HIGH (proceed immediately)
- 0.70-0.84: MEDIUM (verify)
- < 0.70: LOW (manual extraction)

---

```

## Update 4: Update File Structure Section

**Location:** In "## FILE STRUCTURE" section, update the structure diagram

**Replace the existing "├── incoming/" section with:**

```markdown
├── incoming/                              # ACTIVE tickets (unresolved) - Phase 0 input
│   ├── failed/                            # Phase 0 failed extractions
│   │   ├── [failed-file].pdf              # Files that Phase 0 couldn't process
│   │   └── [failed-file]_error.txt        # Error reports with details
│   ├── [ticket-id]_[company].pdf          # Example: 13620086_Singtech.pdf
│   ├── recording_[ticket-id].mp3          # Audio files
│   └── screenshot_[ticket-id]_desc.png    # Screenshots
│
├── processing/                            # Phase 0 output / Phase 1 input
│   └── ticket_[id]/                       # Example: ticket_13620086/
│       ├── metadata.json                  # Phase 0 extracted metadata
│       ├── preliminary_analysis.md        # Phase 0 human-readable analysis
│       └── [standardized-filename].pdf    # Example: 2025-10-29_13620086_Singtech_TradingPartner-HomeDepot_856-ASN.pdf
│
```

## Update 5: Update Agent Coordination Section

**Location:** In "## AGENT COORDINATION" section, update the first handoff

**Replace "Analyst → PM-Investigator:" with:**

```markdown
Analyst → PM-Investigator:
"Extraction complete. Phase 0 metadata: [confidence: X.XX, method: {gemini|ocr|hybrid}, action: {ACCEPT|VERIFY|OVERRIDE}].
Customer history loaded. Trading Partner spec [checked/not available].
Complexity assessed as [L0/L1/L2/L3]. Ready for investigation planning."
```

## Summary of Changes

**Total Updates:** 5 major sections

1. **Phase 0 Section** - NEW section before Phase 1
2. **Phase 1 Enhancement** - Metadata consumption steps
3. **MCP Tool Usage** - Media Analysis Skill documentation
4. **File Structure** - Updated directory structure
5. **Agent Coordination** - Updated handoff message

**Manual Edit Required:** Due to file size, these updates must be manually inserted into bmadedi.md

**Verification:**
- After updates, search for "PHASE 0" to verify insertion
- Search for "metadata.json" to verify Phase 1 updates
- Search for "Media Analysis Skill" to verify MCP tool section

**Testing:**
- Place test ticket in incoming/
- Run workflow.py to verify Phase 0
- Verify Analyst can load metadata.json
- Confirm handoff to PM-Investigator includes Phase 0 info

---

**Agent 6 - BMAD-EDI Workflow Integration Specialist**
**bmadedi.md Update Instructions Complete**

