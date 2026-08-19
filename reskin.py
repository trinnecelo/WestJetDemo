"""Reskin the SC Pharma demo screens as a WestJet OCC delay-risk agent.

Reads ../demoboost_S3qJfnDS/screens/screen-0N.html (the raw Demoboost iframe
HTML we pulled earlier), does a set of exact-substring substitutions to swap
pharma content for WestJet flight-ops content, and writes the results to
./screens/screen-0N.html here.

Substitutions are applied in order — longest/most-distinctive first — with
exact substring matching (no regex). Each atomic sentence and each <strong>
label is its own entry, because the Demoboost HTML splits bullet text across
<strong>/<li>/<p> boundaries so multi-clause finds don't match reliably.
"""
from pathlib import Path

SRC = Path(__file__).parent.parent / "demoboost_S3qJfnDS" / "screens"
DST = Path(__file__).parent / "screens"

# ─────────────────────────────────────────────────────────────────────────────
# Sentences (may span whitespace as-is in the source, incl. embedded newlines).
# Order: longer / more specific first, so a shorter string never eats part of
# a longer replacement's target.
# ─────────────────────────────────────────────────────────────────────────────
SUBS: list[tuple[str, str]] = [
    # ── "How This Was Identified" paragraph (has literal \n between sentences) ──
    (
        "Celonis analysed the process link between the open Quality Usage Decision and the upcoming Production Order.\n"
        "Batch Release for this intermediate material is generally executed 3 days later than the design value, when all QC tests are green.\n"
        "This delay then causes production and shipping to be delayed by at least 5 days.",
        "Celonis Prediction Builder correlated live ACARS position data for the inbound leg with historical turnaround patterns for B737 MAX 8 at YYC.\n"
        "When the inbound aircraft is predicted to arrive less than 15 minutes ahead of scheduled push, on-time departure probability drops from 87% to 22%.\n"
        "This gate turnaround delay then cascades across three downstream rotations of the same tail.",
    ),

    # ── "Why Recommended?" body (label + body separated by \n or a </strong>\n) ──
    (
        "Option 1 is recommended as it eliminates administrative friction, prevents trapped working capital, and neutralizes cascading delays across the global network. This alignment recovers 10 days of total supply chain lead time while maintaining 100% compliance standards by leveraging the verified 'Passed' status of all technical quality checks.",
        "Option 1 preserves the 07:35 MT departure, prevents 4.7 hours of network delay propagation across three rotations of C-GWSA, and keeps the crew pairing intact. It leverages a fully-serviced standby aircraft already at YYC, so execution risk is contained to a gate change and boarding-pass reissue.",
    ),

    # ── Opening summary + prompt ──
    (
        "The AI Batch Accelerator has detected a critical scheduling conflict. This batch is predicted to be late due to a pending release from the quality quarantine area.",
        "The AI Delay Risk Agent has detected a critical turnaround conflict. This flight is predicted to depart late because the inbound aircraft is running behind, compressing the ground turn below minimum block.",
    ),
    (
        "Based on the automated schedule across quality and production, you have the following options:",
        "Based on the live flight and aircraft rotation status, you have the following options:",
    ),
    (
        "Would you like to see mitigation options for this order?",
        "Would you like to see mitigation options?",
    ),

    # ── Option 1 body ──
    (
        "Accelerate final Usage Decision (UD) by bypassing the standard administrative queue for verified compliant batches.",
        "Swap to standby aircraft C-GWSK (B737 MAX 8) currently at YYC gate C50 — clean maintenance status and matching seat configuration.",
    ),
    # Option 1 bullets (structured <li> variants, each standalone)
    (
        "Secure the February 2nd production slot, preventing 8 days of idle capacity at the Raleigh filling line.",
        "Preserve the 07:35 MT departure and prevent 42 downstream misconnects at YYZ.",
    ),
    (
        "Safeguard $1.2M in Work-In-Progress Value and maintain path to the US market for 150k patient units.",
        "Save approximately CAD $24k in rebooking and APPR compensation exposure while protecting 174 passengers.",
    ),
    # Option 1 risk — two variants: with and without "(P20–P70)" insertion
    (
        "Risk: Minimal – All critical quality tests (P20–P70) are verified as 'Passed' in LIMS. Accelerated release only impacts manual administrative lead time.",
        "Risk: Minimal — standby aircraft is release-to-service, same type-rating, and boarding-pass reissue is automated in the PSS.",
    ),
    (
        "Risk: Minimal – All critical quality tests are verified as 'Passed' in LIMS. Accelerated release only impacts manual administrative lead time.",
        "Risk: Minimal — standby aircraft is release-to-service, same type-rating, and boarding-pass reissue is automated in the PSS.",
    ),

    # ── Option 2 body ──
    (
        "Keep the current quality release timeline and reschedule the Raleigh Filling Slot to the next available opening (in 8 days).",
        "Keep the original aircraft and slide the departure to 08:20 MT (45-minute delay).",
    ),
    (
        "Raleigh filling line remains idle for 8 days. Total throughput for the Respiratory line decreases by 15% this quarter.",
        "D-15 miss on WS 1187; approximately 42 passengers misconnect at YYZ; reserve crew callout required for return leg WS 1188.",
    ),
    # Flat-preview variant that inserted "Oncology"
    (
        "Raleigh filling line remains idle for 8 days. Total throughput for the Oncology line decreases by 15% this quarter.",
        "D-15 miss on WS 1187; approximately 42 passengers misconnect at YYZ; reserve crew callout required for return leg WS 1188.",
    ),
    (
        "Risk: Moderate - Triggers an immediate $450k write-off due to loss of commercial shelf-life utility. Increases regional stock-out probability to 85% for the Pennsylvania hub.",
        "Risk: Moderate — reserve crew activation costs CAD $6.4k, and Canadian APPR passenger compensation (CAD $400/pax) triggers if arrival delay exceeds 3 hours.",
    ),

    # ── Actions Taken bullet bodies ──
    (
        "Release executed 48 hours ahead of historical releases, clearing the 'unnecessary blockage' in the final review phase.",
        "C-GWSK assigned to WS 1187 at gate C50; C-GWSA released for its scheduled maintenance check.",
    ),
    (
        "Successfully synchronized the release with Production Order #PO-88212, eliminating the idle time at the Raleigh filling node.",
        "Same crew pairing carried over (identical type rating on B737 MAX 8); no reserve callout triggered.",
    ),
    (
        "Updated initiation sequences and planned start dates in SAP for all product orders.",
        "Gate change pushed to the PSS, WestJet app, and airport FIDS; 174 boarding passes reissued automatically.",
    ),

    # ── Impact Metrics bullet bodies ──
    (
        "Secured, preventing 150k units from failing to reach patients on time for their medical treatment.",
        "WS 1187 secured for 07:35 MT push, protecting the network D-15 target for Sept 15.",
    ),
    (
        "Eliminated 10 days of inventory stalling, improving working capital and protecting $1.2M in batch value.",
        "174 passengers and 42 downstream YYZ connections preserved; avoided approximately CAD $24k in rebooking and APPR exposure.",
    ),
    (
        "Avoided 8 days of production idle time and outbound disruption planning by maintaining the original manufacturing sequence.",
        "4.7 hours of delay propagation across three rotations of C-GWSA avoided; crew duty compliance maintained.",
    ),

    # ── Potential Impact bullet bodies (right of <strong> labels) ──
    (
        "8 days of idle capacity at the Raleigh Plant",
        "174 passengers on WS 1187 plus 42 downstream misconnects at YYZ",
    ),
    (
        "5 day delay in treatment delivery",
        "4.7 hours of delay propagation across three rotations of tail C-GWSA",
    ),

    # ── Alert header field values ──
    (
        "Pending Quality Specialist Review and Approval is blocking the next scheduled supply chain process step",
        "Compressed ground turn — insufficient buffer for deplaning, cleaning, catering, fueling, and boarding before the 07:35 MT push",
    ),
    (
        "All Quality Checks passed - Ready for Release, pending Final Usage Decision (UD)",
        "Inbound leg WS 1186 (YYZ → YYC) delayed; predicted arrival 06:52 MT — 43 min ground turn against a 45 min minimum",
    ),

    # ── <strong> labels (each replaced as a standalone string) ──
    ("Production Stalling:", "Passenger Impact:"),
    ("Patient Accessibility:", "Network Cascade:"),
    ("Usage Decision (UD) Finalized:", "Aircraft Swap Executed:"),
    ("Production Slot Recovery:", "Crew Assignment Synced:"),
    ("Automated Schedule Alignment:", "Passenger Systems Updated:"),
    ("On-Time Patient Delivery:", "On-Time Departure:"),
    ("Optimized Inventory Turnover:", "Passenger Continuity:"),
    ("Operational Stability:", "Network Stability:"),
    ("Option 1: Priority Release (recommended)", "Option 1: Aircraft Swap (recommended)"),
    ("Option 2: Reschedule Downstream Production", "Option 2: Accept the Delay"),

    # ── Message-list preview truncations ──
    (
        "Actions Taken: Usage Decision (UD) Finalize...",
        "Actions Taken: Aircraft Swap Execut...",
    ),
    (
        "Recommended Mitigation Plan: Batch #BCH-CH-...",
        "Recommended Mitigation Plan: Flight WS 1187",
    ),
    # aria-label preview variant with template placeholders
    (
        "Recommended Mitigation Plan: Batch #BCH-CH-XXXXX",
        "Recommended Mitigation Plan: Flight WS 1187",
    ),

    # ── Alert-header title (two variants) ──
    (
        "🚨 BATCH RELEASE RISK DETECTED: Batch #BCH-26-CH-116",
        "🚨 FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ)",
    ),
    (
        "BATCH RELEASE RISK DETECTED: Batch #BCH-26-CH-116",
        "FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ)",
    ),
    (
        "Recommended Mitigation Plan: Batch #BCH-26-CH-116",
        "Recommended Mitigation Plan: Flight WS 1187",
    ),

    # ── Field label pairs and short values ──
    ("API: Inactivated Influenza Vaccine Antigen", "C-GWSA · B737 MAX 8 · 174 seats"),
    ("Dear Quality Specialist,", "Dear OCC Duty Manager,"),
    ("Dear Quality Specialist", "Dear OCC Duty Manager"),
    ("Batch type:", "Aircraft:"),
    ("Critical Deadline:", "Critical Turn Deadline:"),
    ("Sept 15, 2025, 13:00 CET", "Sept 15, 2025, 07:00 MT"),
    ("Days to act until delay:", "Time to act:"),

    # ── Personas ──
    ("SC Pharma Release Risk Agent", "WestJet OCC Delay Risk Agent"),
    ("SSU Pharma Delay Alert Agent", "WestJet Crew Ops Assistant"),
    ("Julian Düring (You)", "Alex Morgan (You)"),
    ("Julian Düring", "Alex Morgan"),

    # ── Timestamps + short values ──
    ("5:35 PM", "6:15 AM"),
    ("5:36 PM", "6:16 AM"),
    ("2 days", "45 minutes"),

    # ── Strip Demoboost's typing-placeholder residue on the header
    #    (source screens showed progressive reveal like "…116 XX", "…116 XXXX"). ──
    ("FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ) XXXX",
     "FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ)"),
    ("FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ) XX",
     "FLIGHT DELAY RISK DETECTED: Flight WS 1187 (YYC → YYZ)"),
]


def rewrite(text: str) -> tuple[str, list[tuple[str, int]]]:
    hits: list[tuple[str, int]] = []
    for find, replace in SUBS:
        n = text.count(find)
        if n:
            text = text.replace(find, replace)
        hits.append((find[:70], n))
    return text, hits


def inject_charset(html: str) -> str:
    """Add <meta charset="utf-8"> right after <head …> if missing.

    Demoboost's original HTTP response advertised UTF-8, but the extracted
    documentElement.outerHTML has no charset meta. Without one, opening the
    file directly via file:// makes em-dashes and emoji mojibake into ISO-8859.
    """
    if "<meta charset=" in html.lower():
        return html
    i = html.lower().find("<head")
    if i < 0:
        return html
    j = html.find(">", i) + 1
    return html[:j] + '<meta charset="utf-8">' + html[j:]


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    sources = sorted(SRC.glob("screen-*.html"))
    if not sources:
        raise SystemExit(f"no source screens in {SRC}")
    for src in sources:
        raw = src.read_text(encoding="utf-8")
        new, hits = rewrite(raw)
        new = inject_charset(new)
        out = DST / src.name
        out.write_text(new, encoding="utf-8")
        applied = sum(1 for _, n in hits if n > 0)
        total = sum(n for _, n in hits)
        print(
            f"{src.name}: applied {applied}/{len(hits)} substitutions, "
            f"{total} replacements total, {len(raw):,} → {len(new):,} bytes"
        )


if __name__ == "__main__":
    main()
