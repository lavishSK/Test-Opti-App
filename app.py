import streamlit as st
import json
import os
from google import genai
from google.genai import types
from utils.data_parser import parse_uploaded_files, build_report_schema
from utils.presets import PRESETS, KPI_LABELS, DSP_LABELS
from utils.display import render_recommendations, render_data_preview, render_insights_panel

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Programmatic AI Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "report_data": {},
    "last_result": None,
    "raw_response": "",
    "api_key": "",
    "analysis_running": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────────────────────────────────────
# CORE ANALYSIS FUNCTION (Moved to the top!)
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis(schema: str, kpi: str, dsp: str, prompt: str):
    """Call Gemini 1.5 Pro using the new google-genai SDK, enforce JSON structure."""
    
    client = genai.Client(api_key=st.session_state.api_key)

    system_instruction = """You are a senior programmatic advertising optimizer specializing in automotive LMA campaigns on TTD, CM360, and DV360. 12+ years in automotive digital media.
    You have REAL campaign data in the user message. Reference specific sites, zip codes, spend amounts, and benchmarks from the actual reports.
    Use your extensive training data to provide industry benchmarks for automotive programmatic display (VDP rates, viewability, OOG standards) and TTD bid optimization best practices.
    
    Return ONLY a valid JSON object matching this exact structure:
    {
      "summary": "2-3 sentence executive summary with specific data references",
      "data_insights": ["insight with numbers", "insight 2", "insight 3", "insight 4"],
      "recommendations": [
        {
          "category": "site_exclusion|zip_exclusion|deal_exclusion|bid_adjustment|bid_factor|audience|creative|pacing",
          "priority": "HIGH|MEDIUM|LOW",
          "title": "Specific action title with concrete details",
          "rationale": "Why, with actual report data (specific numbers, site names, zip codes)",
          "action_items": ["Specific action with exact values"],
          "estimated_impact": "Expected improvement with specific numbers",
          "web_source": "Relevant industry benchmark data or source"
        }
      ],
      "benchmark_context": "Industry benchmark context based on your knowledge base",
      "next_steps": ["Prioritized action 1", "action 2", "action 3"]
    }"""

    user_msg = f"""DATA SCHEMA & CONTENT:
{schema}

PRIMARY KPI: {KPI_LABELS.get(kpi, kpi)}
DSP PLATFORM: {DSP_LABELS.get(dsp, dsp)}

OPTIMIZATION REQUEST:
{prompt}

Generate specific, data-driven recommendations referencing actual numbers from the reports above."""

    status = st.status("🔍 AI Analysis Running...", expanded=True)
    progress = st.progress(0, "Initializing...")

    try:
        with status:
            st.write("📡 Connecting to Gemini API...")
            progress.progress(20, "Connecting...")

            progress.progress(50, "Crunching campaign data...")
            st.write("📊 Analyzing reports & generating recommendations...")

            response = client.models.generate_content(
                model='gemini-1.5-pro',
                contents=user_msg,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                ),
            )

            st.session_state.raw_response = response.text
            
            parsed = json.loads(response.text)
            st.session_state.last_result = parsed

            progress.progress(100, "Done!")
            status.update(label="✅ Analysis complete!", state="complete")
            st.rerun()

    except json.JSONDecodeError:
        st.session_state.last_result = {"_raw": response.text if 'response' in locals() else "No response"}
        status.update(label="⚠️ Partial result (JSON parsing failed)", state="error")
        st.rerun()

    except Exception as e:
        status.update(label=f"❌ Error: {e}", state="error")
        st.error(f"Analysis failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Programmatic AI Optimizer")
    st.caption("Powered by Gemini 1.5 Pro · Built for Ad Ops Teams")
    st.divider()

    # API key
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key or os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get your free key at aistudio.google.com",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.divider()

    # Report uploads
    st.markdown("### 📁 Upload Reports")
    uploaded_files = st.file_uploader(
        "Drop CSV / XLSX reports",
        accept_multiple_files=True,
        type=["csv", "xlsx", "xls"],
        help="Supports: OOG report, Viewability, CM360 Spotlights, TTD Performance, Build Doc",
    )

    if uploaded_files:
        with st.spinner("Parsing reports..."):
            st.session_state.report_data = parse_uploaded_files(uploaded_files)
        st.success(f"✅ {len(uploaded_files)} report(s) loaded")
        for f in uploaded_files:
            ext = f.name.split(".")[-1].upper()
            st.markdown(f"- `{ext}` **{f.name}**")

    # Demo data toggle
    st.divider()
    use_demo = st.toggle(
        "Load Demo Data (GMC/Buick LMA)",
        value=not bool(uploaded_files),
        help="Uses the 5 real GMC/Buick LMA demo reports",
    )

    if use_demo and not uploaded_files:
        from utils.demo_data import DEMO_SCHEMA, DEMO_STATS
        st.session_state.report_data = {"demo": True, "schema": DEMO_SCHEMA, "stats": DEMO_STATS}
        st.info("📦 5 demo reports loaded\nGMC / Buick LMA Campaign")

    # Quick presets
    st.divider()
    st.markdown("### ⚡ Quick Presets")
    
    preset_keys = {
        "🚫 OOG Zip Exclusions": "oog",
        "👁 Low Viewability Sites": "viewability",
        "💰 Bid Optimization": "bid",
        "♻ TTD Spend Waste": "ttd_waste",
        "🎯 Full Campaign Audit": "full",
    }

    def handle_preset_change():
        choice = st.session_state.preset_selector
        if choice != "— Select —":
            p = PRESETS[preset_keys[choice]]
            st.session_state["preset_kpi"] = p["kpi"]
            st.session_state["preset_prompt"] = p["prompt"]

    st.selectbox(
        "Load preset prompt",
        ["— Select —", "🚫 OOG Zip Exclusions", "👁 Low Viewability Sites",
         "💰 Bid Optimization", "♻ TTD Spend Waste", "🎯 Full Campaign Audit"],
        label_visibility="collapsed",
        key="preset_selector",
        on_change=handle_preset_change
    )

# ─────────────────────────────────────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_optimize, tab_data, tab_insights, tab_raw = st.tabs([
    "🚀 Optimize", "📊 Live Data Preview", "💡 Insights", "🔧 Raw API Response"
])

# ── TAB 1 — OPTIMIZE ─────────────────────────────────────────────────────────
with tab_optimize:
    col_cfg, col_results = st.columns([1, 2], gap="large")

    with col_cfg:
        st.markdown("### ⚙️ Configuration")

        kpi = st.selectbox(
            "Primary KPI",
            list(KPI_LABELS.keys()),
            format_func=lambda k: KPI_LABELS[k],
            index=list(KPI_LABELS.keys()).index(
                st.session_state.get("preset_kpi", "vdp")
            ) if st.session_state.get("preset_kpi", "vdp") in KPI_LABELS else 0,
        )
        dsp = st.selectbox(
            "DSP Platform",
            list(DSP_LABELS.keys()),
            format_func=lambda k: DSP_LABELS[k],
        )
        prompt_text = st.text_area(
            "Targeting Context & Optimization Goals",
            value=st.session_state.get(
                "preset_prompt",
                "Campaign: GMC/Buick LMA Texas & Arkansas 2026 Display.\n"
                "Target KPI: VDP Rate >0.5%, CPA <$0.16.\n"
                "Flag all OOG zip codes with >50 incidents.\n"
                "Identify low-viewability sites (<50%).\n"
                "Analyze TTD spend efficiency — flag high-eCPM low-intent sites.\n"
                "Reference Build Doc benchmarks: OOG <15%, Viewability >70%.\n"
                "Base bid: $1.35, Max: $3.31. Pre-approved ceiling: $2.92.",
            ),
            height=220,
            placeholder="Describe your campaign, KPI targets, and what to optimize...",
        )

        # Report health metrics
        if st.session_state.report_data:
            st.markdown("---")
            st.markdown("**📈 Report Health**")
            stats = st.session_state.report_data.get("stats", {})
            m1, m2 = st.columns(2)
            m3, m4 = st.columns(2)
            m1.metric("TTD Sites", stats.get("ttd_sites", "—"))
            m2.metric("Top OOG Zip", stats.get("top_oog_zip", "—"))
            m3.metric("Avg Viewability", stats.get("avg_viewability", "—"))
            m4.metric("Total Spend", stats.get("total_spend", "—"))

        run = st.button(
            "▶ Run AI Optimization Analysis",
            type="primary",
            disabled=not st.session_state.api_key,
            use_container_width=True,
        )
        if not st.session_state.api_key:
            st.warning("⚠️ Enter your Gemini API key in the sidebar to run analysis.")

    # ── Results column ──────────────────────────────────────────────────────
    with col_results:
        st.markdown("### 🎯 Optimization Recommendations")

        if run:
            schema = build_report_schema(st.session_state.report_data)
            run_analysis(schema, kpi, dsp, prompt_text)

        if st.session_state.last_result:
            render_recommendations(st.session_state.last_result)
        else:
            st.info(
                "👈 Configure your KPI, select a preset or write your context, "
                "then click **Run AI Optimization Analysis** to get specific, "
                "data-driven recommendations backed by your uploaded reports."
            )
            _col1, _col2 = st.columns(2)
            with _col1:
                st.markdown("""
**What this tool does:**
- 🚫 Identifies site & zip exclusions from real data
- 💰 Recommends specific bid adjustments
- 👁 Flags viewability & OOG violations
- 🌐 Generates industry benchmark context
""")
            with _col2:
                st.markdown("""
**Report types supported:**
- TTD Campaign Performance (site×zip)
- Out-of-Geo (OOG) reports
- CM360 / DCM Viewability reports
- CM360 Spotlight / Conversion reports
- Campaign Build Docs (110-col spec)
""")

# ── TAB 2 — DATA PREVIEW ─────────────────────────────────────────────────────
with tab_data:
    render_data_preview(st.session_state.report_data)

# ── TAB 3 — INSIGHTS ─────────────────────────────────────────────────────────
with tab_insights:
    render_insights_panel(st.session_state.report_data)

# ── TAB 4 — RAW API RESPONSE ─────────────────────────────────────────────────
with tab_raw:
    if st.session_state.raw_response:
        st.code(st.session_state.raw_response, language="json")
        st.download_button(
            "⬇ Download Raw JSON",
            data=st.session_state.raw_response,
            file_name="optimizer_raw_response.json",
            mime="application/json",
        )
    else:
        st.info("Run an analysis first to see the raw API response here.")
