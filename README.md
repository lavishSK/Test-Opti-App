### Modify Report Parser

Edit `utils/data_parser.py` → add new `_detect_report_type()` logic or new parser function.

---

## 🚧 Roadmap

- [ ] Support for Google Sheets API integration
- [ ] Export recommendations to Excel/CSV
- [ ] Historical comparison (track optimizations over time)
- [ ] Multi-campaign batch analysis
- [ ] DV360 API integration for direct exclusion list updates
- [ ] Slack notifications for critical OOG violations
- [ ] Custom LLM model selection (GPT-4, Gemini)

---

## 📈 Performance

- Average analysis time: **8-15 seconds** (includes web search)
- Memory usage: **~200MB** per session
- Supports files up to **200MB** (Streamlit default limit)

---

# Programmatic AI Optimizer

AI-powered campaign optimization tool for programmatic advertising teams. Built with **Streamlit** and **Google Gemini 1.5**, designed for automotive LMA campaigns but works with any DSP (TTD, CM360, DV360, Xandr).

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 What It Does

Upload your campaign reports → AI analyzes them with web search → Get **specific, actionable recommendations**:

- 🚫 **Site & Zip Exclusions** — Identify low-performing inventory, OOG violations, 0% viewability sites
- 💰 **Bid Adjustments** — Recommended bid factors and CPM caps per site/format
- 📍 **Geo Optimization** — Flag out-of-geo zip codes with incident counts
- 🌐 **Industry Benchmarks** — Real-time web search for automotive programmatic best practices
- 📊 **Live Data Preview** — See OOG violations, viewability failures, TTD spend waste before running AI

**Supports:**
- TTD Campaign Performance Reports (site×zip level)
- Out-of-Geo (OOG) Reports
- CM360/DCM Viewability Reports  
- CM360 Spotlight / Conversion Reports
- Campaign Build Docs (SDF/110-col spec)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/programmatic-optimizer.git
cd programmatic-optimizer
2. Install DependenciesBashpip install -r requirements.txt
3. Set Your Google Gemini API KeyGet your key at aistudio.google.comOption A: Environment VariableBashexport GEMINI_API_KEY='your-api-key-here'
Option B: Enter in the AppThe sidebar has an API key input field (stored in session only).4. Run the AppBashstreamlit run app.py
The app opens at http://localhost:8501📂 Project Structureprogrammatic-optimizer/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml          # Streamlit config (theme, port)
├── assets/
│   └── style.css            # Custom CSS styling
├── utils/
│   ├── data_parser.py       # Report file parsing logic
│   ├── demo_data.py         # GMC/Buick LMA demo data
│   ├── display.py           # UI rendering functions
│   └── presets.py           # Quick-action presets
└── demo_reports/            # (Optional) Sample report files


🛠 Usage GuideStep 1: Upload Reports or Use Demo DataUpload: CSV or XLSX files via the sidebarDemo: Toggle "Load Demo Data" to use real GMC/Buick LMA campaign reportsSupported report types are auto-detected:TTD Performance → site/zip/spend columnsOOG Report → "Out of Geo Incident" columnsViewability → "Viewable Rate" columnsCM360 Spotlights → "Total Spotlight" columnsBuild Doc → "Base Bid" / "Primary KPI" columnsStep 2: Configure KPI & ContextSelect Primary KPI (VDP Rate, Viewability, OOG, CPA, etc.)Choose your DSP Platform (TTD, CM360, DV360, Xandr)Write or select a preset prompt:🚫 OOG Zip Exclusions👁 Low Viewability Sites💰 Bid Optimization♻ TTD Spend Waste🎯 Full Campaign AuditExample prompt:Campaign: GMC LMA Texas 2026 (San Angelo TX DMA).
Target KPI: VDP Rate >0.5%, CPA <$0.16.
Flag all OOG zip codes with >50 incidents (Zip 75217 has 2,312 hits).
Identify low-viewability sites (<50%).
Analyze TTD spend efficiency — flag high-eCPM low-intent sites.
Base bid: $1.35, Max: $3.31. Pre-approved ceiling: $2.92.
Step 3: Run AnalysisClick "▶ Run AI Optimization Analysis"The AI will:Parse your uploaded report dataSearch the web for automotive programmatic benchmarksGenerate specific recommendations with exact valuesReturn structured JSON with action itemsStep 4: Review ResultsNavigate tabs:🚀 Optimize — AI recommendations with priority levels📊 Live Data Preview — Tables of OOG violations, viewability, TTD sites💡 Insights — Auto-detected patterns and red flags🔧 Raw API Response — Full JSON output for debugging🌐 Deploy to Streamlit Cloud (Free)PrerequisitesGitHub accountGoogle Gemini API keyStepsPush to GitHub:Bashgit add .
git commit -m "Initial commit"
git push origin main
Go to share.streamlit.ioClick "New app":Repository: your-username/programmatic-optimizerBranch: mainMain file: app.pyAdd Secrets (in Advanced Settings):Ini, TOMLGEMINI_API_KEY = "your-api-key-here"
Deploy! Your app will be live at:https://your-app-name.streamlit.app
🔐 Environment VariablesVariableRequiredDescriptionGEMINI_API_KEYYesYour Google Gemini API key from aistudio.google.comFor local development:Bashexport GEMINI_API_KEY='your-api-key-here'
For Streamlit Cloud:Add to the Secrets section in app settings (TOML format).📊 Demo DataThe app includes real GMC/Buick LMA campaign data from 5 reports:TTD Performance — 27,275 rows, $5,607 spend, 450 sitesOOG Report — Zip 75217 (Dallas) with 4,689 incidentsViewability — 83% avg, 20+ zero-viewability sites flaggedCM360 Spotlights — 700+ conversion columns, 300×250 format at 13.33% VDP rateBuild Doc — Base bid $1.35, CPA target $0.16, OOG benchmark <15%Enable in sidebar: "Load Demo Data (GMC/Buick LMA)"🧪 Example Use CasesUse Case 1: OOG CleanupProblem: Campaign showing 100% OOG rate in specific zip codesSolution: Load OOG report → select "OOG Zip Exclusions" preset → AI identifies zip 75217 with 4,689 incidents → recommends immediate geo-exclusionUse Case 2: Viewability OptimizationProblem: Viewability below 70% benchmarkSolution: Upload viewability report → select "Low Viewability Sites" → AI flags 20+ sites with 0% viewability → generates exclusion listUse Case 3: TTD Spend EfficiencyProblem: High eCPM on non-automotive sitesSolution: Upload TTD performance data → select "TTD Spend Waste" → AI identifies businessinsider.com at $4.27 eCPM vs. $2.31 avg → recommends bid cap or exclusionUse Case 4: Full Campaign AuditProblem: Need comprehensive optimization across all KPIsSolution: Upload all 5 reports → select "Full Campaign Audit" → AI generates 8-12 prioritized recommendations across OOG, viewability, bids, and creative🛡 Security & PrivacyAPI Key: Never committed to git (see .gitignore)Report Data: Processed locally, not stored after session endsAI Calls: Sent to Google Gemini API (read their privacy policy)No Tracking: App doesn't collect analytics or usage data🤝 ContributingThis is an internal tool but contributions are welcome!Fork the repoCreate a feature branch (git checkout -b feature/amazing-feature)Commit changes (git commit -m 'Add amazing feature')Push to branch (git push origin feature/amazing-feature)Open a Pull Request📝 LicenseMIT License — see LICENSE file for details.💬 SupportIssues? Open a GitHub issue or contact the team lead.Questions about reports? Check utils/data_parser.py for supported schemas.Need a new preset? Edit utils/presets.py and add your workflow.🎨 CustomizationAdd a New PresetEdit utils/presets.py:PythonPRESETS = {
    "my_preset": {
        "kpi": "ctr",
        "prompt": "Your custom optimization prompt here..."
    }
}
Change ThemeEdit .streamlit/config.toml:Ini, TOML[theme]
primaryColor = "#f5a623"  # Amber
backgroundColor = "#0d0f14"
secondaryBackgroundColor = "#141720"
textColor = "#e8eaf0"
Modify Report ParserEdit utils/data_parser.py → add new _detect_report_type() logic or new parser function.🚧 Roadmap[ ] Support for Google Sheets API integration[ ] Export recommendations to Excel/CSV[ ] Historical comparison (track optimizations over time)[ ] Multi-campaign batch analysis[ ] DV360 API integration for direct exclusion list updates[ ] Slack notifications for critical OOG violations[ ] Custom LLM model selection (GPT-4, Gemini)📈 PerformanceAverage analysis time: 8-15 seconds (includes web search)Memory usage: ~200MB per sessionSupports files up to 200MB (Streamlit default limit)Built with ❤️ by the Ad Ops TeamPowered by Google Gemini 1.5 · Streamlit · Python