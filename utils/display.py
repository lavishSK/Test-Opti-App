"""
Streamlit UI rendering functions for optimization recommendations,
data previews, and insights panels.
"""
import streamlit as st
import pandas as pd


def render_recommendations(result: dict):
    """Render parsed AI recommendations in Streamlit."""
    
    # Handle raw text fallback
    if "_raw" in result:
        st.warning("⚠️ Received non-JSON response from AI")
        st.text_area("Raw Response", result["_raw"], height=400)
        return

    # Executive Summary
    if result.get("summary"):
        st.markdown("#### 📋 Executive Summary")
        st.info(result["summary"])
        st.divider()

    # Data Insights
    if result.get("data_insights"):
        with st.expander("💡 **Data Insights from Reports**", expanded=True):
            for insight in result["data_insights"]:
                st.markdown(f"→ {insight}")

    # Recommendations
    recs = result.get("recommendations", [])
    if recs:
        st.markdown(f"#### 🎯 {len(recs)} Optimization Recommendations")
        
        for i, rec in enumerate(recs, 1):
            category = rec.get("category", "general")
            priority = rec.get("priority", "MEDIUM")
            
            # Color coding
            colors = {
                "HIGH": "🔴",
                "MEDIUM": "🟡", 
                "LOW": "🟢"
            }
            emoji = colors.get(priority, "⚪")
            
            cat_labels = {
                "site_exclusion": "🚫 Site Exclusion",
                "zip_exclusion": "📍 Zip/Geo Exclusion",
                "deal_exclusion": "💼 Deal Exclusion",
                "bid_adjustment": "💰 Bid Adjustment",
                "bid_factor": "📊 Bid Factor",
                "audience": "👥 Audience",
                "creative": "🎨 Creative",
                "pacing": "⏱ Pacing",
            }
            cat_label = cat_labels.get(category, category.title())
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{i}. {rec.get('title', 'Recommendation')}**")
                with col2:
                    st.markdown(f"{emoji} `{priority}` · {cat_label}")
                
                st.markdown(rec.get("rationale", ""))
                
                # Action items as colored pills
                if rec.get("action_items"):
                    st.markdown("**Actions:**")
                    actions_html = ""
                    for action in rec["action_items"]:
                        # Determine action type for color
                        action_lower = action.lower()
                        if any(kw in action_lower for kw in ["exclude", "block", "remove", "negate"]):
                            badge_color = "#f87171"
                        elif any(kw in action_lower for kw in ["increase", "raise", "boost"]):
                            badge_color = "#4ade80"
                        elif any(kw in action_lower for kw in ["decrease", "reduce", "lower"]):
                            badge_color = "#fb923c"
                        elif any(kw in action_lower for kw in ["monitor", "watch", "track"]):
                            badge_color = "#60a5fa"
                        else:
                            badge_color = "#a78bfa"
                        
                        actions_html += f'<span style="display:inline-block;background:{badge_color}20;border:1px solid {badge_color}60;color:{badge_color};padding:2px 8px;margin:2px;border-radius:4px;font-size:0.85em;font-family:monospace">{action}</span>'
                    
                    st.markdown(actions_html, unsafe_allow_html=True)
                
                # Estimated impact
                if rec.get("estimated_impact"):
                    st.success(f"📈 **Impact:** {rec['estimated_impact']}")
                
                # Web source
                if rec.get("web_source"):
                    st.caption(f"📚 Source: [{rec['web_source']}]({rec['web_source']})")

    # Benchmark context
    if result.get("benchmark_context"):
        st.divider()
        with st.expander("📊 **Industry Benchmarks (Web Research)**"):
            st.markdown(result["benchmark_context"])

    # Next steps
    if result.get("next_steps"):
        st.divider()
        st.markdown("#### 🚀 Next Steps")
        for i, step in enumerate(result["next_steps"], 1):
            st.markdown(f"{i}. {step}")


def render_data_preview(report_data: dict):
    """Render live data preview tables from uploaded reports."""
    
    if not report_data or not report_data.get("reports"):
        st.info("📂 Upload campaign reports or enable demo data to see live previews.")
        return
    
    reports = report_data.get("reports", {})
    
    # OOG violations
    if "oog" in reports:
        oog = reports["oog"]
        st.markdown("### 🔴 Out-of-Geo (OOG) Violations")
        st.caption(f"Total incidents: {oog.get('total_incidents', 0):,} across {oog.get('total_rows', 0):,} rows")
        
        if oog.get("top_violations"):
            df = pd.DataFrame(oog["top_violations"])
            df["action"] = df["incidents"].apply(
                lambda x: "🔴 EXCLUDE NOW" if x > 100 else "⚠️ MONITOR"
            )
            st.dataframe(
                df[["zip", "dma", "incidents", "rate", "action"]].rename(columns={
                    "zip": "Zip Code",
                    "dma": "DMA/MMA", 
                    "incidents": "OOG Incidents",
                    "rate": "OOG Rate",
                    "action": "Status"
                }),
                use_container_width=True,
                hide_index=True,
            )
        st.divider()
    
    # Viewability
    if "viewability" in reports:
        view = reports["viewability"]
        st.markdown("### 👁 Viewability Report")
        avg = view.get("avg_viewable_rate")
        if avg:
            st.metric("Average Viewable Rate", f"{avg*100:.1f}%", 
                     delta=f"{(avg-0.7)*100:+.1f}pp vs. 70% benchmark")
        
        if view.get("zero_viewability_sites"):
            st.markdown("**⛔ Zero Viewability Sites (Immediate Exclusion):**")
            sites_str = ", ".join(view["zero_viewability_sites"][:20])
            st.error(sites_str)
        
        if view.get("below_50pct_sites"):
            st.markdown("**⚠️ Below 50% Viewability:**")
            sites_str = ", ".join(view["below_50pct_sites"][:15])
            st.warning(sites_str)
        st.divider()
    
    # TTD Performance
    if "ttd" in reports:
        ttd = reports["ttd"]
        st.markdown("### 💸 TTD Site Performance")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spend", f"${ttd.get('total_spend', 0):,.2f}")
        col2.metric("Total Impressions", f"{ttd.get('total_impressions', 0):,}")
        col3.metric("Unique Sites", ttd.get('unique_sites', 0))
        
        tab1, tab2 = st.tabs(["📊 Top Sites by Volume", "⚠️ High eCPM (Waste)"])
        
        with tab1:
            if ttd.get("top_sites_by_impressions"):
                df = pd.DataFrame(ttd["top_sites_by_impressions"])
                df["spend"] = df["spend"].apply(lambda x: f"${x:.2f}")
                df["ecpm"] = df["ecpm"].apply(lambda x: f"${x:.2f}")
                df["impressions"] = df["impressions"].apply(lambda x: f"{x:,}")
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab2:
            if ttd.get("high_ecpm_sites"):
                df = pd.DataFrame(ttd["high_ecpm_sites"])
                df["spend"] = df["spend"].apply(lambda x: f"${x:.2f}")
                df["ecpm"] = df["ecpm"].apply(lambda x: f"${x:.2f}")
                df["impressions"] = df["impressions"].apply(lambda x: f"{x:,}")
                df["action"] = "🚫 EXCLUDE or CAP BID"
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
    
    # Build Doc
    if "build_doc" in reports:
        bd = reports["build_doc"]
        st.markdown("### 📋 Campaign Build Doc Benchmarks")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Primary KPI", bd.get("primary_kpi", "—"))
            st.metric("Viewability Target", bd.get("viewability_benchmark", "—"))
            st.metric("OOG Target", bd.get("oog_benchmark", "—"))
            st.metric("IVT Target", bd.get("ivt_benchmark", "—"))
        
        with col2:
            st.metric("Starting Base Bid", bd.get("starting_base_bid", "—"))
            st.metric("Starting Max Bid", bd.get("starting_max_bid", "—"))
            st.metric("Pre-Approved Ceiling", bd.get("pre_approved_base_bid", "—"))
            st.metric("Frequency Cap", bd.get("frequency", "—"))
        
        if bd.get("site_blocks"):
            with st.expander("🚫 Existing Site/App Blocks"):
                st.text(bd["site_blocks"])


def render_insights_panel(report_data: dict):
    """Render key insights and patterns from uploaded data."""
    
    if not report_data or not report_data.get("reports"):
        st.info("📊 Upload reports to see automated insights.")
        return
    
    reports = report_data.get("reports", {})
    insights = []
    
    # OOG insights
    if "oog" in reports:
        oog = reports["oog"]
        total = oog.get("total_incidents", 0)
        if total > 0:
            insights.append({
                "icon": "🔴",
                "title": "Critical OOG Violations Detected",
                "desc": f"{total:,} total OOG incidents found. This is ABOVE the 15% Build Doc benchmark.",
                "severity": "high"
            })
            top = oog.get("top_violations", [])
            if top and top[0].get("incidents", 0) > 100:
                insights.append({
                    "icon": "📍",
                    "title": f"Zip {top[0]['zip']} Needs Immediate Exclusion",
                    "desc": f"{top[0]['incidents']:,} OOG incidents in {top[0]['dma']}. "
                           f"Add to geo-exclusion list ASAP.",
                    "severity": "high"
                })
    
    # Viewability insights
    if "viewability" in reports:
        view = reports["viewability"]
        avg = view.get("avg_viewable_rate")
        if avg and avg < 0.7:
            insights.append({
                "icon": "👁",
                "title": "Viewability Below Target",
                "desc": f"Average viewability is {avg*100:.1f}%, below the 70% benchmark. "
                       f"Consider site exclusions.",
                "severity": "medium"
            })
        zero_sites = len(view.get("zero_viewability_sites", []))
        if zero_sites > 0:
            insights.append({
                "icon": "⛔",
                "title": f"{zero_sites} Sites with 0% Viewability",
                "desc": "These sites are serving non-viewable inventory. Exclude immediately.",
                "severity": "high"
            })
    
    # TTD insights
    if "ttd" in reports:
        ttd = reports["ttd"]
        high_ecpm = ttd.get("high_ecpm_sites", [])
        if high_ecpm:
            avg_ecpm = ttd.get("total_spend", 0) / ttd.get("total_impressions", 1) * 1000
            top_waste = high_ecpm[0]
            insights.append({
                "icon": "💸",
                "title": f"High eCPM Waste: {top_waste['Site']}",
                "desc": f"eCPM ${top_waste['ecpm']:.2f} vs. campaign avg ${avg_ecpm:.2f}. "
                       f"Consider bid cap or exclusion.",
                "severity": "medium"
            })
    
    # Build Doc insights
    if "build_doc" in reports:
        bd = reports["build_doc"]
        if bd.get("starting_base_bid") and bd.get("pre_approved_base_bid"):
            insights.append({
                "icon": "💰",
                "title": "Bid Range Defined",
                "desc": f"Base bid: {bd['starting_base_bid']}, "
                       f"Pre-approved ceiling: {bd['pre_approved_base_bid']}. "
                       f"Increments require CM approval beyond ceiling.",
                "severity": "info"
            })
    
    # Render insights
    if insights:
        st.markdown("### 💡 Key Insights")
        for ins in insights:
            if ins["severity"] == "high":
                with st.container(border=True):
                    st.error(f"{ins['icon']} **{ins['title']}**")
                    st.caption(ins['desc'])
            elif ins["severity"] == "medium":
                with st.container(border=True):
                    st.warning(f"{ins['icon']} **{ins['title']}**")
                    st.caption(ins['desc'])
            else:
                with st.container(border=True):
                    st.info(f"{ins['icon']} **{ins['title']}**")
                    st.caption(ins['desc'])
    else:
        st.info("No critical insights detected. Your campaign metrics look healthy!")
