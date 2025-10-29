# Analyst Agent Integration Guide - Phase 0 Metadata Consumption

**Agent 6 - BMAD-EDI Workflow Integration Specialist**

## Overview

This guide explains how the Analyst agent (Phase 1) should consume pre-extracted metadata from Phase 0 (Pre-Investigation Analysis).

## Enhanced Analyst Workflow

### Step 1: Check for Phase 0 Metadata

**Before starting extraction, check if Phase 0 has already processed the ticket:**

```bash
# Define ticket processing folder
TICKET_ID="13624970"  # Extract from context or user input
PROCESSING_DIR="C:\Users\sleep\Documents\tickets\processing"
TICKET_FOLDER="$PROCESSING_DIR/ticket_$TICKET_ID"
METADATA_FILE="$TICKET_FOLDER/metadata.json"

# Check if Phase 0 metadata exists
if [ -f "$METADATA_FILE" ]; then
    echo "[+] Phase 0 metadata available"
    echo "[*] Loading pre-extracted data..."
else
    echo "[!] No Phase 0 metadata found"
    echo "[*] Proceeding with manual extraction"
fi
```

### Step 2: Load and Verify Pre-Extracted Metadata

**If metadata.json exists, load and assess confidence:**

```python
import json

# Load metadata
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Extract fields
ticket_id = metadata.get('ticket_id', 'UNKNOWN')
customer_name = metadata.get('customer_name', '')
company = metadata.get('company', '')
trading_partner = metadata.get('trading_partner', '')
transaction_type = metadata.get('transaction_type', '')
message_id = metadata.get('message_id', '')
severity = metadata.get('severity', 'NORMAL')
issue_title = metadata.get('issue_title', '')
root_cause = metadata.get('root_cause', '')
recommended_actions = metadata.get('recommended_actions', [])

# Check confidence
confidence = metadata.get('confidence', 0.0)
extraction_method = metadata.get('extraction_method', 'unknown')

print(f"[*] Confidence: {confidence:.2%}")
print(f"[*] Extraction Method: {extraction_method.upper()}")

# Decision tree
if confidence >= 0.85:
    print("[+] HIGH CONFIDENCE - Ready to proceed")
    action = "ACCEPT"
elif confidence >= 0.70:
    print("[!] MEDIUM CONFIDENCE - Verification recommended")
    action = "VERIFY"
else:
    print("[!] LOW CONFIDENCE - Manual extraction required")
    action = "OVERRIDE"
```

### Step 3: Display Pre-Extracted Data to User

**Show Analyst the extracted information for review:**

```
================================================================================
[PHASE 0 COMPLETE - METADATA AVAILABLE]
================================================================================

Ticket: {ticket_id}
File: {processed_file}
Confidence: {confidence:.2%} ({HIGH|MEDIUM|LOW})
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
...

================================================================================
[ANALYST OPTIONS]
================================================================================

1. ACCEPT → Use pre-extracted data as-is (HIGH confidence only)
2. VERIFY → Review and correct extracted data (MEDIUM/HIGH confidence)
3. OVERRIDE → Perform manual extraction (LOW confidence or user preference)

[ACTION]: _
```

### Step 4: Handle Analyst Decision

**A. ACCEPT (High Confidence >= 0.85)**

```python
# Use metadata as-is
print("[+] Analyst accepted pre-extracted metadata")

# Generate formatted output using metadata
formatted_output = f"""
================================================================================
TICKET: {company} - {trading_partner} - {issue_title}
================================================================================

Extraction Phase:

• Customer Name: {customer_name}
• Company Name: {company}
• Company ID Number: [To be filled by Analyst if available]
• Phone Number: [To be filled by Analyst if available]
• Email: [To be filled by Analyst if available]
• Trading Partner: {trading_partner}
• Document Types: {transaction_type}
• Error/Issue: {issue_title}
• Message IDs/Control Numbers: {message_id}
• Integration Type: [To be determined by Analyst]
• Priority: {severity}

Ticket Description:

{root_cause}

Recommended Actions:
{chr(10).join(f'- {action}' for action in recommended_actions)}

[SOURCE: Phase 0 Gemini Extraction - Confidence: {confidence:.2%}]
"""

print(formatted_output)
# Proceed to Phase 2 (PM-Investigator)
```

**B. VERIFY (Medium Confidence 0.70-0.84)**

```python
print("[*] Analyst reviewing pre-extracted metadata for accuracy...")

# Show preliminary_analysis.md for reference
analysis_file = Path(ticket_folder) / "preliminary_analysis.md"
if analysis_file.exists():
    with open(analysis_file, 'r', encoding='utf-8') as f:
        preliminary_analysis = f.read()
    print("\n--- Preliminary Analysis ---")
    print(preliminary_analysis)

# Analyst reviews and makes corrections
print("\n[*] Analyst should:")
print("  1. Review preliminary_analysis.md")
print("  2. Cross-check against ticket file")
print("  3. Make necessary corrections")
print("  4. Update metadata.json if needed")

# After verification, generate formatted output with corrections
# ... (same as ACCEPT, but with analyst-verified data)
```

**C. OVERRIDE (Low Confidence < 0.70 or Manual Preference)**

```python
print("[!] Analyst performing manual extraction")
print("[*] Pre-extracted metadata available for reference:")

# Show extracted data as hints
print(f"  [HINT] Possible ticket ID: {ticket_id}")
print(f"  [HINT] Possible company: {company}")
print(f"  [HINT] Possible trading partner: {trading_partner}")
# ... etc

# Analyst performs full manual extraction
# (Traditional Phase 1 workflow)
```

### Step 5: Document Metadata Source

**Always note where metadata came from:**

```python
# Add metadata provenance to ticket extraction
metadata_source = {
    "method": extraction_method,  # gemini, ocr, or hybrid
    "confidence": confidence,
    "phase0_processed": True,
    "analyst_action": action,  # ACCEPT, VERIFY, or OVERRIDE
    "analyst_corrections": []  # List of fields corrected
}

# If Analyst made corrections
if action == "VERIFY":
    metadata_source["analyst_corrections"] = [
        "Corrected trading partner name",
        "Updated severity from NORMAL to HIGH",
        # ... etc
    ]

# Include in Investigation PRD
```

### Step 6: Handoff to Phase 2 (PM-Investigator)

**Pass validated metadata to PM-Investigator:**

```
================================================================================
HANDOFF: Analyst → PM-Investigator
================================================================================

[+] Extraction complete
[+] Customer history loaded: [YES/NO]
[+] Trading Partner spec checked: [AVAILABLE/NOT AVAILABLE]
[+] Complexity assessed as: [L0/L1/L2/L3]

Metadata Source:
- Phase 0 Extraction: {extraction_method.upper()}
- Confidence: {confidence:.2%}
- Analyst Action: {action}
- Corrections Made: {len(analyst_corrections)}

Ready for investigation planning.
================================================================================
```

## Integration Benefits

**Time Savings:**
- HIGH confidence (>= 0.85): Skip manual extraction entirely (~5-10 minutes saved)
- MEDIUM confidence (0.70-0.84): Faster verification than full extraction (~3-5 minutes saved)
- LOW confidence (< 0.70): Metadata hints still helpful (~1-2 minutes saved)

**Accuracy Improvements:**
- Consistent metadata extraction format
- Reduced human error in data entry
- Multiple extraction sources (Gemini + OCR fallback)
- Confidence scoring guides Analyst attention

**Workflow Efficiency:**
- Standardized filenames for easy organization
- Pre-analyzed root cause and recommendations
- Immediate trading partner identification
- Severity pre-assessment

## Example: Full Analyst Workflow with Phase 0

**Scenario:** Ticket 13624970 arrives in incoming/

**Phase 0 (Automatic):**
1. Gemini extracts metadata (confidence: 0.92)
2. Generates metadata.json and preliminary_analysis.md
3. Moves file to processing/ticket_13624970/
4. Status: READY FOR ANALYST

**Phase 1 (Analyst):**

```
[ANALYST SESSION START]

[*] Checking for Phase 0 metadata...
[+] Phase 0 metadata available
[*] Loading pre-extracted data...

================================================================================
[PHASE 0 COMPLETE - METADATA AVAILABLE]
================================================================================

Ticket: 13624970
File: 2025-10-29_13624970_AceHardware_TradingPartner-HomeDepot_856-ASN-Rejection.pdf
Confidence: 92% (HIGH)
Extraction Method: GEMINI

Pre-Extracted Metadata:
✓ Customer: John Doe
✓ Company: Ace Hardware Supply Co.
✓ Trading Partner: Home Depot
✓ Transaction: 856 ASN
✓ Message ID: ASN-20250129-001
✓ Severity: HIGH
✓ Issue: 856 ASN Rejection - Invalid SCAC Code

Root Cause:
Missing carrier SCAC code in shipment details, preventing trading partner
from validating shipment.

Recommended Actions:
1. Add SCAC code to N1 segment (Carrier Name)
2. Verify weight values in HL segment (Hierarchical Level)
3. Re-transmit corrected 856 ASN

================================================================================
[ANALYST OPTIONS]
================================================================================

1. ACCEPT → Use pre-extracted data as-is
2. VERIFY → Review and correct extracted data
3. OVERRIDE → Perform manual extraction

[ACTION]: 1 (ACCEPT)

[+] Analyst accepted pre-extracted metadata

[*] Generating formatted output...

================================================================================
TICKET: Ace Hardware Supply Co. - Home Depot - 856 ASN Rejection - Invalid SCAC Code
================================================================================

Extraction Phase:

• Customer Name: John Doe
• Company Name: Ace Hardware Supply Co.
• Company ID Number: [To be verified in customer database]
• Trading Partner: Home Depot
• Document Types: 856 ASN
• Error/Issue: 856 ASN Rejection - Invalid SCAC Code
• Message IDs/Control Numbers: ASN-20250129-001
• Priority: HIGH

Ticket Description:

Missing carrier SCAC code in shipment details, preventing trading partner
from validating shipment. The 856 ASN was rejected by Home Depot due to
missing SCAC code in N1 segment and potentially missing weight values in
HL segment.

[SOURCE: Phase 0 Gemini Extraction - Confidence: 92%]

[*] Loading customer history...
[+] Customer file found: customers/7514_AceHardwareSupplyCo.md
[*] Previous tickets with Home Depot: 2
[*] Pattern identified: ASN formatting issues (3 occurrences)

[*] Checking Trading Partner spec...
[+] Trading Partner folder found: Trading_Partners/Home_Depot/
[+] Reading: 856_ASN_Specification.pdf
[*] Exact requirements verified

[*] Assessing complexity...
[*] Complexity Score: 2 (L0-Simple)
  - Error Clarity: 0 (Clear error code)
  - System Scope: 0 (Single system)
  - Pattern Recognition: 0 (Known pattern)
  - Customer History: 2 (New issue for this customer)

[HANDOFF] Analyst → PM-Investigator

[+] Extraction complete
[+] Customer history loaded: YES
[+] Trading Partner spec checked: AVAILABLE
[+] Complexity assessed as: L0

Metadata Source:
- Phase 0 Extraction: GEMINI
- Confidence: 92%
- Analyst Action: ACCEPT
- Corrections Made: 0

Ready for investigation planning.
```

**Time Comparison:**

- **Without Phase 0:** Manual extraction (~8-10 minutes) + history lookup (~2 min) + spec check (~2 min) = 12-14 minutes
- **With Phase 0 (HIGH confidence):** Accept metadata (~1 min) + history lookup (~2 min) + spec check (~2 min) = 5 minutes
- **Time Saved:** 7-9 minutes per ticket (50-64% faster)

## Error Scenarios

**Scenario 1: Phase 0 Extraction Failed**
```
[!] No Phase 0 metadata found
[!] Check: C:\Users\sleep\Documents\tickets\incoming\failed\
[!] Review error report: ticket_13624970_error.txt
[*] Proceeding with manual extraction
```

**Scenario 2: Low Confidence Extraction**
```
[!] Phase 0 confidence: 0.65 (LOW)
[!] Extraction Method: HYBRID (Gemini + OCR fallback)
[*] Metadata available for reference but requires verification
[ACTION]: 3 (OVERRIDE - Manual extraction)
```

**Scenario 3: Metadata Corruption**
```
[!] metadata.json file corrupted or invalid format
[!] Attempting to read preliminary_analysis.md instead...
[*] Proceeding with manual extraction
```

## Best Practices

1. **Always check for Phase 0 metadata first**
   - Don't skip this step even for simple tickets
   - Metadata may reveal unexpected complexity

2. **Trust high-confidence extractions (>= 0.85)**
   - Gemini 2.5 Pro is highly accurate for EDI tickets
   - Spot-check occasionally to maintain quality

3. **Verify medium-confidence extractions (0.70-0.84)**
   - Quick review can catch edge cases
   - Document corrections for future improvements

4. **Override low-confidence extractions (< 0.70)**
   - Manual extraction more reliable in these cases
   - Use extracted data as hints only

5. **Document Analyst actions**
   - Record whether metadata was accepted, verified, or overridden
   - Note any corrections made
   - Feed this back for Phase 0 improvements

6. **Maintain metadata provenance**
   - Always note extraction source in Investigation PRD
   - Include confidence scores in documentation
   - Helps with quality assurance and debugging

## Summary

Phase 0 integration transforms the Analyst workflow from manual extraction to intelligent verification. High-confidence extractions can be accepted immediately, medium-confidence extractions require quick verification, and low-confidence extractions fallback to manual processing. This adaptive approach saves 50-64% of extraction time while maintaining accuracy and quality.

**Key Takeaway:** The Analyst agent becomes a verifier and quality controller rather than a pure data entry role, allowing more focus on complex analysis and investigation planning.

