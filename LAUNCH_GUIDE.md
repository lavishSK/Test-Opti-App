# 🚀 LAUNCH GUIDE - Final 5% Checklist

**You're about to launch a production-ready AI optimization platform for your 20-person team!**

---

## ✅ Pre-Launch Checklist (2 minutes)

Copy this checklist and tick off as you go:

- [ ] Downloaded the complete project folder
- [ ] Have GitHub account ready
- [ ] Have credit card ready (for Anthropic API - pay-as-you-go)
- [ ] Have 30 minutes free time for full deployment

---

## 🎯 STEP 1: Get Your Anthropic API Key (5 minutes)

### A. Create Account
1. Go to: **https://console.anthropic.com**
2. Click "Sign Up" (use your work email)
3. Verify email
4. Add payment method (required for API access)
   - Don't worry: Pay-as-you-go pricing
   - ~$0.02-$0.10 per analysis
   - No monthly fees

### B. Generate API Key
1. Click "API Keys" in left sidebar
2. Click "Create Key"
3. Name it: `Programmatic-Optimizer-Production`
4. Copy the key: `sk-ant-api03-...` (starts with `sk-ant`)
5. **Save it somewhere safe** (you can't view it again!)

### C. Test the Key (Optional)
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY_HERE" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'
```

If you see a JSON response → ✅ Key works!

**✅ Checkpoint:** You have a working API key starting with `sk-ant-`

---

## 🎯 STEP 2: Test Locally First (10 minutes)

### A. Extract the Project
```bash
# Navigate to downloads folder
cd ~/Downloads

# Extract the folder
unzip programmatic-optimizer.zip  # or just extract via Finder/Explorer

# Enter the directory
cd programmatic-optimizer
```

### B. Install Dependencies
**Mac/Linux:**
```bash
# Quick setup script
chmod +x setup.sh
./setup.sh

# OR manual:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### C. Set API Key
**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

**Windows PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

**Windows CMD:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### D. Validate Setup
```bash
python test_setup.py
```

**Expected output:**
```
🎯 Results: 8/8 tests passed
✅ ALL TESTS PASSED! Ready to deploy.
```

### E. Run the App
```bash
streamlit run app.py
```

Browser opens at: **http://localhost:8501**

### F. Test It Works
1. Toggle "Load Demo Data (GMC/Buick LMA)" ✅
2. Select preset: "🎯 Full Campaign Audit"
3. Click "▶ Run AI Optimization Analysis"
4. Wait 10-15 seconds
5. See recommendations appear ✅

**✅ Checkpoint:** App runs locally and generates recommendations

---

## 🎯 STEP 3: Push to GitHub (8 minutes)

### A. Create GitHub Repository

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name:** `programmatic-optimizer`
   - **Description:** `AI-powered campaign optimization for programmatic advertising teams`
   - **Visibility:** 🔒 **PRIVATE** (recommended - contains business logic)
   - **DO NOT** check "Initialize with README" (we have one)
3. Click "Create repository"

### B. Push Your Code

GitHub shows you commands - use these:

```bash
# Make sure you're in the project directory
cd programmatic-optimizer

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Programmatic AI Optimizer v1.0"

# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/programmatic-optimizer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Use GitHub username
- Use Personal Access Token as password (not your GitHub password)
- Generate token at: https://github.com/settings/tokens

### C. Verify Upload

1. Refresh your GitHub repo page
2. You should see all files:
   - ✅ app.py
   - ✅ utils/ folder
   - ✅ README.md
   - ✅ requirements.txt
   - ✅ .streamlit/ folder
3. **Check .gitignore worked:**
   - ❌ Should NOT see .env files
   - ❌ Should NOT see any .csv or .xlsx files
   - ❌ Should NOT see API keys

**✅ Checkpoint:** Code is on GitHub, no secrets committed

---

## 🎯 STEP 4: Deploy to Streamlit Cloud (10 minutes)

### A. Sign In to Streamlit Cloud

1. Go to: **https://share.streamlit.io**
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your repos

### B. Create New App

1. Click "New app" (top right)
2. Fill in the form:

**Repository:**
- Select: `YOUR_USERNAME/programmatic-optimizer`

**Branch:**
- `main`

**Main file path:**
- `app.py`

**App URL (choose a subdomain):**
- `your-team-name-optimizer` (e.g., `acme-ad-ops-optimizer`)
- This becomes: `https://your-team-name-optimizer.streamlit.app`

### C. Add API Key as Secret

**BEFORE clicking Deploy:**

1. Click "Advanced settings..."
2. Click "Secrets" tab
3. Add this **exactly** (TOML format):

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

**⚠️ CRITICAL:**
- Use quotes around the key
- Use equals sign (not colon)
- This is TOML format, not JSON

### D. Deploy!

1. Click "Deploy!"
2. Wait 2-3 minutes (building environment)
3. Watch the logs - you'll see:
   ```
   Installing dependencies...
   Starting app...
   You can now view your Streamlit app in your browser!
   ```

### E. Test Deployment

1. Your app is now live at: `https://your-subdomain.streamlit.app`
2. Open the URL
3. Test with demo data:
   - Toggle "Load Demo Data"
   - Run an analysis
   - Verify recommendations appear

**✅ Checkpoint:** App is live and accessible via public URL

---

## 🎯 STEP 5: Share with Your Team (2 minutes)

### A. Prepare Team Email

```
Subject: NEW TOOL: AI Campaign Optimizer - Now Live 🚀

Hi team,

We now have an AI-powered optimization tool for all programmatic campaigns!

🔗 Access it here: https://your-subdomain.streamlit.app

What it does:
• Upload any TTD/CM360/DV360 reports
• Describe your optimization goals
• Get specific recommendations (site exclusions, bid adjustments, geo targeting)
• Backed by real campaign data + web research

How to use:
1. Upload your campaign reports (CSV/XLSX)
2. Select your KPI (VDP, Viewability, OOG, CPA, etc.)
3. Write your targeting context and goals
4. Click "Run Analysis"
5. Get actionable recommendations in ~15 seconds

Or just toggle "Load Demo Data" to see it in action first.

Quick Start Guide: [attach QUICKSTART.md]

Questions? Reply to this email or Slack me.

- [Your Name]
```

### B. Bookmark for Quick Access

Add to your team's:
- Slack pinned links
- Internal wiki/Notion
- Browser bookmarks bar
- Weekly standup agenda

### C. Train the Team (Optional)

Schedule a 15-minute Zoom:
1. Show demo data example (2 min)
2. Upload real report and run analysis (5 min)
3. Explain preset buttons (2 min)
4. Q&A (6 min)

**✅ Checkpoint:** Team has access and knows how to use it

---

## 🎯 STEP 6: Monitor & Maintain (Ongoing)

### A. Check Usage & Costs

**Anthropic Console:**
- https://console.anthropic.com
- Dashboard → Usage
- Typical cost: $5-20/month for 20-person team using it weekly

**Streamlit Cloud:**
- https://share.streamlit.io/YOUR_USERNAME
- View app analytics
- Monitor uptime

### B. Update the App (When Needed)

**To push updates:**
```bash
# Make changes to code locally
git add .
git commit -m "Update: improved OOG detection"
git push origin main

# Streamlit Cloud auto-redeploys in ~2 minutes
```

**To manually redeploy:**
1. Go to share.streamlit.io
2. Find your app
3. Click "⋮" menu → "Reboot app"

### C. Rotate API Key (Quarterly Recommended)

1. Generate new key at console.anthropic.com
2. Go to Streamlit Cloud → your app → Settings → Secrets
3. Update `ANTHROPIC_API_KEY` value
4. Save (app reboots automatically)

**✅ Checkpoint:** Monitoring in place

---

## 🎉 CONGRATULATIONS - YOU'RE LIVE!

### What You Just Launched:

✅ **Production AI platform** for 20-person team
✅ **Handles unlimited campaigns** (any client, any DSP, any vertical)
✅ **Real-time web search** for industry benchmarks
✅ **Smart auto-detection** of report types
✅ **Specific, actionable recommendations** with exact values
✅ **Professional UI** with dark theme
✅ **Secure deployment** (private repo, encrypted secrets)
✅ **Zero maintenance** (Streamlit Cloud handles hosting)
✅ **Auto-deploys** (git push → live in 2 minutes)

### Cost Breakdown:
- **Streamlit Cloud:** FREE (Community tier)
- **GitHub:** FREE (for private repos)
- **Anthropic API:** ~$5-20/month (pay-as-you-go)
- **Your time:** 30 minutes setup, then maintenance-free

### Team Usage:
- **URL:** https://your-subdomain.streamlit.app
- **Access:** Anyone with link (no login needed)
- **Capacity:** Unlimited users simultaneously
- **Speed:** ~10-15 seconds per analysis

---

## 📊 Next Week's Goals

**Day 1:** Team training session
**Day 2-3:** Team tests with demo data
**Day 4-5:** Team uses with real campaigns
**Week 2:** Collect feedback, iterate on presets

---

## 🆘 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| "Invalid API key" | Regenerate at console.anthropic.com, update Streamlit secrets |
| App won't start | Check logs in Streamlit Cloud dashboard |
| Import errors | Verify requirements.txt is complete, reboot app |
| Slow analysis | Normal - web search takes 10-15 seconds |
| Wrong recommendations | Refine prompt with more specific context |
| Can't push to GitHub | Check Personal Access Token at github.com/settings/tokens |
| Secrets not loading | Verify TOML format: `KEY = "value"` with quotes |

---

## 📞 Support Resources

**Documentation:**
- Quick Start: `QUICKSTART.md`
- Full Guide: `README.md`
- Deployment: `DEPLOYMENT.md`
- Architecture: `ARCHITECTURE.md`

**External Help:**
- Anthropic API Docs: https://docs.anthropic.com
- Streamlit Docs: https://docs.streamlit.io
- GitHub Docs: https://docs.github.com

**Team Contact:**
- Internal Slack: #ad-ops-tools
- Email: [your team lead]

---

## 🎯 Success Metrics (Track These)

**Week 1:**
- [ ] All 20 team members accessed the tool
- [ ] At least 10 real analyses run
- [ ] Zero deployment issues

**Month 1:**
- [ ] 100+ analyses completed
- [ ] 5+ campaigns optimized based on recommendations
- [ ] Team feedback collected
- [ ] 1-2 preset improvements implemented

**Quarter 1:**
- [ ] Tool is part of standard optimization workflow
- [ ] Measurable KPI improvements on optimized campaigns
- [ ] Cost savings documented (time + media waste reduction)

---

## 🚀 You're Done!

**The remaining 5% is now 100% complete.**

Your team has a professional, AI-powered optimization platform that will:
- Save hours of manual analysis time
- Catch issues faster (OOG, viewability, spend waste)
- Provide data-backed recommendations
- Scale across unlimited campaigns

**Now go optimize some campaigns! 🎯**

---

_Built with Claude Sonnet 4 · Deployed on Streamlit Cloud · Powered by Your Team_
