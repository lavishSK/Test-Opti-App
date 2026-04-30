"""
Real GMC/Buick LMA demo data extracted from uploaded campaign reports.
Used when no files are uploaded (demo mode).
"""

DEMO_SCHEMA = """
=== DEMO: GMC / BUICK LMA CAMPAIGN REPORTS (5 Files) ===

=== REPORT 1: TTD Campaign Performance (27,275 rows) ===
Campaign: MRGKG375120_2026_NA_TTD_GMC_GMC_LMA_Display_InMarket_LITTLEROCK-PINEBLUFF AR
Columns: Site, Ad Group, Campaign, Inventory Contract, Zip, Impressions, Advertiser Cost (USD)
Total Spend: $5,607.27 | Total Impressions: 2,422,429 | Unique Sites: 450

TOP 15 SITES BY IMPRESSIONS:
  1617391485 (unknown app): 671,942 imps, $1,303.49 — eCPM $1.94
  www.yahoo.com: 323,497 imps, $819.38 — eCPM $2.53
  295646461 (unknown app): 218,538 imps, $596.03 — eCPM $2.73
  com.weather.weather: 214,475 imps, $621.17 — eCPM $2.90
  com.block.juggle: 109,147 imps, $235.63 — eCPM $2.16
  com.aws.android: 62,306 imps, $196.74 — eCPM $3.16
  com.tripledot.solitaire: 57,179 imps, $89.74 — eCPM $1.57
  mail.yahoo.com: 68,839 imps, $146.69 — eCPM $2.13
  www.msn.com: 66,645 imps, $177.78 — eCPM $2.67
  jp.gocro.smartnews.android: 45,383 imps, $109.93 — eCPM $2.42

HIGH eCPM SITES (waste / low-intent candidates):
  ⚠️ www.businessinsider.com: 314 imps, $1.34 — eCPM $4.27
  ⚠️ www.the-sun.com: 214 imps, $0.91 — eCPM $4.25
  ⚠️ fortune.com: 200 imps, $0.84 — eCPM $4.20
  ⚠️ www.mensjournal.com: 238 imps, $0.99 — eCPM $4.17
  ⚠️ people.com: 184 imps, $0.76 — eCPM $4.15
  ⚠️ www.autoblog.com: 315 imps, $1.27 — eCPM $4.04 (NOTE: automotive-relevant — evaluate)
  ⚠️ www.washingtonpost.com: 392 imps, $1.44 — eCPM $3.67
  ✅ www.cargurus.com: 640 imps, $2.32 — eCPM $3.62 (automotive intent — keep)

TOP ZIPS BY IMPRESSIONS:
  72204 (Little Rock AR): 122,137 imps, $288.33
  72034 (Conway AR): 103,006 imps, $231.73
  72223 (Little Rock AR): 91,205 imps, $217.53
  71913 (Hot Springs AR): 88,535 imps, $206.76
  72205 (Little Rock AR): 88,422 imps, $210.33

=== REPORT 2: OOG (Out-of-Geo) Report ===
Campaign: 2026_XSAG_SAGTX_SCR_GMC/BUICK_LMA_Display_GEN_Base
Target Geo: San Angelo TX DMA and surrounding Texas markets

🔴 CRITICAL OOG VIOLATIONS (Rate = 100% — NOT in target geo):
  Zip 75217 (Dallas-Ft. Worth TX): 2,312 incidents — GMC SierraLD HPA 320x50
  Zip 75217 (Dallas-Ft. Worth TX): 1,166 incidents — GMC Terrain HPA 320x50
  Zip 75217 (Dallas-Ft. Worth TX): 1,138 incidents — GMC SierraHD HPA 320x50
  Zip 75217 (Dallas-Ft. Worth TX): 1,073 incidents — Buick Envista HPA 320x50
  Zip 79720 (Odessa-Midland TX): 1,738 incidents — Buick Envista HPA 320x50
  (Total zip 75217 OOG incidents: 4,689 — immediate exclusion required)

⚠️ MINOR OOG INCIDENTS (1 each — monitor):
  Zip 78727 (Austin TX), Zip 80640 (Denver CO), Zip 80210 (Denver CO),
  Zip 20011 (Washington DC), Zip 78228 (San Antonio TX)

=== REPORT 3: Viewability Report ===
Campaign: GMC LMA + Buick LMA Display
Overall Mobile In-App: GMC=82.6%, Buick=83.8% ✅ (ABOVE 70% benchmark)

ZERO VIEWABILITY SITES (immediate exclusion candidates):
  yaytext.com, woodmagazine.com, wltx.com, augustachronicle.com,
  thefashionspot.com, wired.com, caffeineinformer.com, wcnc.com,
  thewrap.com, timesdaily.com, community.babycenter.com, cooking.nytimes.com,
  theheartysoul.com, theskimm.com, thesportster.com, swimsuit.si.com,
  steelerswire.usatoday.com, theflowspace.com, characterhub.com, cbs8.com

=== REPORT 4: CM360 Spotlight Report ===
Placements: SCR_XSAG_SAGTX_GMC_LMA_GEN_2026 Display formats (160x600, 300x250, 320x50, 728x90)
Models tracked: GMC Acadia, Sierra LD, Sierra HD, Terrain, Buick Envista, Buick Multiline
Conversion event namespaces: XBIR_T2, XBIR_T1, BuickGMC_T1, BuickGMC_T2, BG_BUICK_T2, BG_GMC_T2
Conversion events: Site-Visit, VDP, Click-To-Call (Sales), Click-To-Call (Service),
                   Window Sticker, Vehicle Search, Email Leads, Hours-And-Directions,
                   Locate-A-Dealer
TOP PERFORMING PLACEMENT:
  Placement 10361224 (GMC Acadia 300x250): VDP Rate 13.33% (2 conversions / 15 ads booked)
Most placements showing 0 conversions — new/low-volume, needs more data.

=== REPORT 5: Build Doc (Campaign Blueprint — TTD SDF) ===
DSP: The Trade Desk (TTD)
Brand: GMC | Tier: LMA | Audience: GEN | Strategy: HPA + InMarket
Tactic: Display Standard (HPA) + Display Consideration
Primary KPI: CPA ≤ $0.16
Viewability Benchmark: ≥70%
IVT Benchmark: <1%
Brand Safety Benchmark: <1%
Out of Geo Benchmark: <15%
Mobile Inventory Benchmark: >20%
iOS Inventory Benchmark: >10%
Starting Base Bid Q1: $1.35 | Starting Max Bid: $3.3076
Pre-Approved Base Bid ceiling: $2.916 (notify account manager when reached)
Bid Increase Increment: $0.25 (requires CM approval beyond pre-approved ceiling)
NonCon Max CPM: $13.00
Audience Segment: GMC HPA (STA_ALL_3P_ALL_PRE_0026_MixGmcHpa, ID: raaqf8y)
Existing Exclusion Lists:
  - MRG Monthly Exclusion List (ID: 592005290)
  - Precision Global Exclusion List - Sites (ID: 277230429)
  - Precision Global Exclusion List - Apps (ID: 330726097)
Existing Inclusion List: FY26 Monthly Inclusion List (ID: 571429003)
DV Brand Safety: dv-51005077 | DV Viewability: IAB 70
Blocked Vendors: Primis/Sekindo, Epsilon CPE, Outbrain, Taboola
Conversion Pixel IDs:
  BG VDP New (qzunbzl), BG VDP Used (inaw187), BG Site Visit, BG Click to Call (ei85tof),
  BG Window Sticker (5t221f7), BG Email Leads (nvv3rcq), BG Inventory Search (nfy0l4b)
Frequency Cap: 25 imps/month | 20/week | 10/day | 4/8hr
Ad Format Bid Mod Mapping: Display Standard Bid Mods
"""

DEMO_STATS = {
    "ttd_sites": "450",
    "total_spend": "$5,607",
    "avg_viewability": "83.2%",
    "top_oog_zip": "75217",
    "total_impressions": "2.4M",
    "oog_critical": "4,689",
    "zero_view_sites": "20+",
    "base_bid": "$1.35",
}
