"""Quick-action presets for common optimization workflows."""

KPI_LABELS = {
    "vdp":        "VDP Rate — Vehicle Detail Page Views (maximize)",
    "site_visit": "Site Visit Rate — Drive users to dealership site",
    "viewability":"Viewability Rate ≥70% (Build Doc benchmark)",
    "oog":        "Out-of-Geo Rate ≤15% (Build Doc benchmark)",
    "cpa":        "CPA ≤ $0.16 (Build Doc primary KPI)",
    "ctr":        "Click-Through Rate (CTR) optimization",
    "custom":     "Custom KPI — defined in prompt below",
}

DSP_LABELS = {
    "ttd":    "The Trade Desk (TTD)",
    "cm360":  "Campaign Manager 360 (CM360)",
    "dv360":  "Display & Video 360 (DV360)",
    "xandr":  "Xandr / Microsoft Invest",
    "amazon": "Amazon DSP",
}

PRESETS = {
    "oog": {
        "kpi": "oog",
        "prompt": (
            "Campaign: GMC/Buick LMA Texas 2026 (San Angelo TX DMA).\n"
            "OOG benchmark per Build Doc: <15%.\n"
            "CRITICAL: Zip 75217 (Dallas-Ft Worth) has 4,689 total OOG incidents at 100% rate — needs immediate exclusion.\n"
            "Zip 79720 (Odessa-Midland) has 1,738 OOG incidents at 100% rate — evaluate exclusion.\n"
            "Identify all other zips with OOG incidents and prioritize by severity.\n"
            "Recommend geo-fence tightening strategy for HPA vs InMarket placements.\n"
            "Search web for TTD geo-targeting best practices for local automotive dealers."
        ),
    },
    "viewability": {
        "kpi": "viewability",
        "prompt": (
            "Campaign: GMC/Buick LMA Display 2026.\n"
            "Viewability benchmark per Build Doc: ≥70%. Overall Mobile In-App is 83% (good).\n"
            "Sites with 0% viewability from report: yaytext.com, woodmagazine.com, wltx.com,\n"
            "augustachronicle.com, thefashionspot.com, wired.com, wcnc.com, thewrap.com,\n"
            "timesdaily.com, caffeineinformer.com, community.babycenter.com, cooking.nytimes.com.\n"
            "Recommend site exclusions for all 0% viewability sites.\n"
            "Cross-reference against known low-viewability site lists.\n"
            "Search for TTD viewability optimization best practices for display campaigns."
        ),
    },
    "bid": {
        "kpi": "cpa",
        "prompt": (
            "Campaign: GMC LMA TTD Display 2026.\n"
            "Current bids: Base $1.35, Max $3.31, Pre-approved ceiling $2.92, Increment $0.25.\n"
            "Build Doc CPA target: <$0.16.\n"
            "Total TTD spend: $5,607 | 2.4M impressions | avg eCPM ~$2.31.\n"
            "High eCPM inefficient sites: businessinsider.com ($4.27), fortune.com ($4.20),\n"
            "people.com ($4.15), mensjournal.com ($4.17), the-sun.com ($4.25).\n"
            "Automotive-relevant site: autoblog.com ($4.04), cargurus.com ($3.62) — keep.\n"
            "Suggest site-level bid factor adjustments within TTD.\n"
            "Recommend bid reduction for high-eCPM non-automotive sites.\n"
            "Search for automotive LMA TTD bid optimization case studies."
        ),
    },
    "ttd_waste": {
        "kpi": "cpa",
        "prompt": (
            "Analyze TTD spend efficiency for GMC LMA campaign.\n"
            "Total: $5,607 spend | 2.4M imps | 450 sites.\n"
            "Top spend sites: 1617391485 app ($1,303), yahoo.com ($819), 295646461 app ($596).\n"
            "Numeric site IDs (1617391485, 295646461, com.block.juggle, com.aws.android)\n"
            "are likely low-quality game/utility app inventory — evaluate exclusion.\n"
            "Calculate potential savings from excluding top wasteful sites.\n"
            "Search for known low-quality mobile app bundles in automotive programmatic.\n"
            "Identify which TTD supply vendors should be blocked."
        ),
    },
    "full": {
        "kpi": "vdp",
        "prompt": (
            "Full campaign audit: GMC/Buick LMA Texas & Arkansas 2026.\n\n"
            "PRIORITIES:\n"
            "1. OOG: Exclude zip 75217 (4,689 total incidents) and 79720 (1,738 incidents) immediately.\n"
            "2. Viewability: Exclude all sites with 0% viewability (yaytext.com, woodmagazine.com, etc.)\n"
            "3. TTD Sites: Flag high-eCPM low-automotive-intent sites (businessinsider, fortune, people, mensjournal).\n"
            "4. TTD Apps: Evaluate unknown app bundle IDs (1617391485, 295646461) for inclusion.\n"
            "5. Bids: Recommend bid adjustments within $1.35–$2.92 range per Build Doc.\n"
            "6. CM360: 300x250 format shows 13.33% VDP rate on GMC Acadia — recommend scaling.\n\n"
            "KPI targets from Build Doc: CPA <$0.16, Viewability >70%, OOG <15%, IVT <1%.\n"
            "Search web for GMC LMA programmatic optimization case studies and automotive display\n"
            "best practices 2025-2026."
        ),
    },
}
