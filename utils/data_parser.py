"""
Parses uploaded campaign report files and extracts structured data
for downstream analysis and AI prompt injection.
"""
import io
import pandas as pd
from typing import Any


# ── File type detection ───────────────────────────────────────────────────────

def _detect_report_type(filename: str, df: pd.DataFrame) -> str:
    """Heuristically identify which report type a file is."""
    fn = filename.lower()
    cols = [c.lower() for c in df.columns]

    if "out of geo" in " ".join(cols) or "oog" in fn:
        return "oog"
    if "viewable rate" in " ".join(cols) or "viewability" in fn:
        return "viewability"
    if "total spotlight" in " ".join(cols) or "spotlight" in fn or "cm360" in fn:
        return "cm360"
    if "advertiser cost" in " ".join(cols) or "ttd" in fn or "inventory contract" in " ".join(cols):
        return "ttd"
    if "base bid" in " ".join(cols) or "build" in fn or "dsp" in " ".join(cols[:5]):
        return "build_doc"
    return "unknown"


def _read_file(uploaded_file) -> pd.DataFrame:
    """Read CSV or XLSX into a DataFrame."""
    name = uploaded_file.name.lower()
    content = uploaded_file.read()
    uploaded_file.seek(0)
    buf = io.BytesIO(content)

    if name.endswith(".csv"):
        return pd.read_csv(buf)
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(buf)
    raise ValueError(f"Unsupported file type: {uploaded_file.name}")


# ── Per-report parsers ────────────────────────────────────────────────────────

def _parse_oog(df: pd.DataFrame) -> dict:
    high = df[df.get("Out of Geo Incident Rate", pd.Series(dtype=float)).fillna(0) > 0]
    top = high.sort_values("Out of Geo Incidents", ascending=False).head(20)
    summary = []
    for _, row in top.iterrows():
        summary.append({
            "zip": row.get("Zip Code", ""),
            "dma": row.get("DMA/MMA", ""),
            "incidents": int(row.get("Out of Geo Incidents", 0)),
            "rate": float(row.get("Out of Geo Incident Rate", 0)),
            "placement": str(row.get("Placement Name", ""))[:80],
        })
    return {
        "type": "oog",
        "total_rows": len(df),
        "total_incidents": int(df.get("Out of Geo Incidents", pd.Series([0])).sum()),
        "top_violations": summary,
    }


def _parse_viewability(df: pd.DataFrame) -> dict:
    low = df[df.get("Viewable Rate", pd.Series(dtype=float)).fillna(1) < 0.01]
    avg = df["Viewable Rate"].mean() if "Viewable Rate" in df.columns else None
    return {
        "type": "viewability",
        "total_rows": len(df),
        "avg_viewable_rate": round(float(avg), 4) if avg else None,
        "zero_viewability_sites": list(low.get("Delivery Site", pd.Series()).dropna().unique()[:30]),
        "below_50pct_sites": list(
            df[df.get("Viewable Rate", pd.Series(dtype=float)).fillna(1) < 0.5]
            .get("Delivery Site", pd.Series()).dropna().unique()[:30]
        ),
    }


def _parse_ttd(df: pd.DataFrame) -> dict:
    if "Impressions" in df.columns and "Advertiser Cost (USD)" in df.columns:
        site_agg = (
            df.groupby("Site", dropna=False)
            .agg(impressions=("Impressions", "sum"), spend=("Advertiser Cost (USD)", "sum"))
            .reset_index()
        )
        site_agg["ecpm"] = (site_agg["spend"] / site_agg["impressions"] * 1000).round(2)
        top_imp = site_agg.sort_values("impressions", ascending=False).head(15)
        high_ecpm = site_agg[site_agg["impressions"] > 100].sort_values("ecpm", ascending=False).head(15)

        zip_agg = None
        if "Zip" in df.columns:
            zip_agg = (
                df.groupby("Zip", dropna=False)
                .agg(impressions=("Impressions", "sum"), spend=("Advertiser Cost (USD)", "sum"))
                .reset_index()
                .sort_values("impressions", ascending=False)
                .head(15)
            )

        return {
            "type": "ttd",
            "total_rows": len(df),
            "total_impressions": int(df["Impressions"].sum()),
            "total_spend": round(float(df["Advertiser Cost (USD)"].sum()), 2),
            "unique_sites": int(df["Site"].nunique()),
            "top_sites_by_impressions": top_imp.to_dict("records"),
            "high_ecpm_sites": high_ecpm.to_dict("records"),
            "top_zips": zip_agg.to_dict("records") if zip_agg is not None else [],
        }
    return {"type": "ttd", "total_rows": len(df), "columns": list(df.columns[:20])}


def _parse_cm360(df: pd.DataFrame) -> dict:
    top_cols = ["Placement", "Placement ID", "Total Ads Booked",
                "Total Spotlights", "Total Spotlight Rate"]
    available = [c for c in top_cols if c in df.columns]
    sample = df[available].head(20).to_dict("records") if available else []
    return {
        "type": "cm360",
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "sample_placements": sample,
    }


def _parse_build_doc(df: pd.DataFrame) -> dict:
    row = df.dropna(how="all").iloc[0] if len(df) > 0 else pd.Series()

    def safe(col):
        return str(row.get(col, "")) if not pd.isna(row.get(col, None)) else ""

    return {
        "type": "build_doc",
        "primary_kpi": safe("Primary KPI"),
        "primary_benchmark": safe("Primary Benchmark"),
        "viewability_benchmark": safe("Viewability Benchmark"),
        "ivt_benchmark": safe("IVT Benchmark"),
        "brand_safety_benchmark": safe("Brand Safety Benchmark"),
        "oog_benchmark": safe("Out of Geo Benchmark"),
        "mobile_inventory_benchmark": safe("Mobile Inventory Benchmark"),
        "starting_base_bid": safe("Starting Base Bid Q1"),
        "starting_max_bid": safe("Starting Max Bid"),
        "pre_approved_base_bid": safe("Pre-Approved Base Bid(Notify MRG when reached. Anything beyond this requires CM approval)"),
        "noncon_max_cpm": safe("NonCon Max CPM"),
        "audience": safe("Audience (AS)"),
        "contract_group": safe("Contract Group"),
        "site_blocks": safe("Site/App Blocks [Free Form]"),
        "dv_brand_safety": safe("DoubleVerify Brand Safety [SDF]"),
        "dv_viewability": safe("Double Verify Viewability [SDF]"),
        "supply_vendor_blocks": safe("Supply Vendor Blocks [SDF]"),
        "frequency": safe("Frequency"),
    }


# ── Public API ────────────────────────────────────────────────────────────────

def parse_uploaded_files(uploaded_files) -> dict:
    """Parse a list of uploaded Streamlit file objects into structured dicts."""
    result = {"demo": False, "reports": {}}
    stats = {}

    for uf in uploaded_files:
        try:
            df = _read_file(uf)
            rtype = _detect_report_type(uf.name, df)

            parsers = {
                "oog": _parse_oog,
                "viewability": _parse_viewability,
                "ttd": _parse_ttd,
                "cm360": _parse_cm360,
                "build_doc": _parse_build_doc,
            }

            parsed = parsers.get(rtype, lambda d: {"type": rtype, "rows": len(d)})(df)
            result["reports"][rtype] = parsed

        except Exception as e:
            result["reports"][f"error_{uf.name}"] = {"error": str(e)}

    # Build stats for sidebar metrics
    ttd = result["reports"].get("ttd", {})
    oog = result["reports"].get("oog", {})
    view = result["reports"].get("viewability", {})

    stats["ttd_sites"] = str(ttd.get("unique_sites", "—"))
    stats["total_spend"] = f"${ttd.get('total_spend', 0):,.0f}" if ttd.get("total_spend") else "—"
    stats["avg_viewability"] = f"{view.get('avg_viewable_rate', 0)*100:.1f}%" if view.get("avg_viewable_rate") else "—"

    top_oog = oog.get("top_violations", [{}])
    stats["top_oog_zip"] = str(top_oog[0].get("zip", "—")) if top_oog else "—"

    result["stats"] = stats
    return result


def build_report_schema(report_data: dict) -> str:
    """Convert parsed report data into a rich text schema for the AI prompt."""
    if report_data.get("demo"):
        from utils.demo_data import DEMO_SCHEMA
        return DEMO_SCHEMA

    reports = report_data.get("reports", {})
    lines = ["=== UPLOADED REPORT SCHEMAS ===\n"]

    # TTD
    ttd = reports.get("ttd")
    if ttd:
        lines.append("=== TTD CAMPAIGN PERFORMANCE ===")
        lines.append(f"Total rows: {ttd.get('total_rows', 0):,}")
        lines.append(f"Total impressions: {ttd.get('total_impressions', 0):,}")
        lines.append(f"Total spend: ${ttd.get('total_spend', 0):,.2f}")
        lines.append(f"Unique sites: {ttd.get('unique_sites', 0)}")
        if ttd.get("top_sites_by_impressions"):
            lines.append("\nTOP SITES BY IMPRESSIONS:")
            for s in ttd["top_sites_by_impressions"]:
                lines.append(f"  {s['Site']}: {s['impressions']:,} imps, ${s['spend']:.2f}, eCPM ${s['ecpm']:.2f}")
        if ttd.get("high_ecpm_sites"):
            lines.append("\nHIGH eCPM SITES (waste candidates):")
            for s in ttd["high_ecpm_sites"]:
                lines.append(f"  ⚠️ {s['Site']}: {s['impressions']:,} imps, eCPM ${s['ecpm']:.2f}")
        if ttd.get("top_zips"):
            lines.append("\nTOP ZIPS BY IMPRESSIONS:")
            for z in ttd["top_zips"][:10]:
                lines.append(f"  {z['Zip']}: {z['impressions']:,} imps, ${z['spend']:.2f}")
        lines.append("")

    # OOG
    oog = reports.get("oog")
    if oog:
        lines.append("=== OUT-OF-GEO (OOG) REPORT ===")
        lines.append(f"Total rows: {oog.get('total_rows', 0):,}")
        lines.append(f"Total OOG incidents: {oog.get('total_incidents', 0):,}")
        if oog.get("top_violations"):
            lines.append("\nTOP OOG VIOLATIONS:")
            for v in oog["top_violations"]:
                flag = "🔴 CRITICAL" if v["incidents"] > 100 else "⚠️"
                lines.append(f"  {flag} Zip {v['zip']} ({v['dma']}): {v['incidents']:,} incidents, Rate={v['rate']*100:.0f}%")
        lines.append("")

    # Viewability
    view = reports.get("viewability")
    if view:
        avg = view.get("avg_viewable_rate")
        lines.append("=== VIEWABILITY REPORT ===")
        if avg:
            lines.append(f"Average viewable rate: {avg*100:.1f}%")
        if view.get("zero_viewability_sites"):
            lines.append(f"\nZERO VIEWABILITY SITES (exclude): {', '.join(view['zero_viewability_sites'])}")
        if view.get("below_50pct_sites"):
            lines.append(f"\nBELOW 50% VIEWABILITY: {', '.join(view['below_50pct_sites'])}")
        lines.append("")

    # CM360
    cm = reports.get("cm360")
    if cm:
        lines.append("=== CM360 SPOTLIGHT REPORT ===")
        lines.append(f"Total rows: {cm.get('total_rows', 0):,}, Columns: {cm.get('total_columns', 0)}")
        if cm.get("sample_placements"):
            lines.append("\nSAMPLE PLACEMENTS:")
            for p in cm["sample_placements"][:5]:
                lines.append(f"  {p}")
        lines.append("")

    # Build Doc
    bd = reports.get("build_doc")
    if bd:
        lines.append("=== CAMPAIGN BUILD DOC BENCHMARKS ===")
        for k, v in bd.items():
            if v and k != "type":
                lines.append(f"  {k.replace('_', ' ').title()}: {v}")
        lines.append("")

    if not reports:
        lines.append("No reports uploaded. Please upload campaign reports or enable demo data.")

    return "\n".join(lines)
