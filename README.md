# WholeUp AI: Senior Multi-Agent Marketing & Autonomous Media Buyer

An enterprise-grade Multi-Agent System designed specifically for high-growth digital marketing agencies. It models the strategic mindset of a **5+ year elite growth marketing director and direct-response media buyer**.

---

## 🏗️ Architecture

```
                  ┌──────────────────────────────────────────────┐
                  │          USER INPUT: Niche & Offer           │
                  └──────────────────────┬───────────────────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │  Agent 1: Avatar & Competitor Researcher    │
                   │  - Nightmares, Desires, Objections         │
                   └─────────────────────┬──────────────────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │  Agent 2: SEO & Search Intent Architect     │
                   │  - Commercial Keywords, Negative Lists     │
                   └─────────────────────┬──────────────────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │  Agent 3: Direct-Response Copywriter       │
                   │  - 3x Meta Ad Variations, 5x Viral Reels   │
                   └─────────────────────┬──────────────────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │  Agent 4: Creative & Visual Art Director    │
                   │  - Canva Layouts, Image Prompts, B-Roll    │
                   └─────────────────────┬──────────────────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │  Agent 5: Agency Director & CMO Audit      │
                   │  - Fluff Audit, Meta Policy, Final Sign-off│
                   └────────────────────────────────────────────┘

    ========================================================================
    ⚡ 24/7 AUTONOMOUS AD OPTIMIZER (META MARKETING API & GOOGLE ADS)
    ========================================================================
     [Live Ad Metrics] ──► [Agent 6: Media Buyer Bot]
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
    [Kill Bleeder]          [Scale Winner]           [Fatigue Alert]
    Spend > 2.5x CPA        ROAS > 3.0x & CPL cheap  Frequency > 3.2
    0 Leads ➔ PAUSE AD      Scale Budget +20%        Rotate Creative
```

---

## 🚀 Quick Start Guide

### 1. Requirements & Setup
All dependencies are pre-installed in the local virtual environment `.venv`:
```powershell
cd C:\Users\NEEL\.gemini\antigravity\scratch\agency-growth-ai
.\.venv\Scripts\activate
```

### 2. Launch the Interactive Web Dashboard
```powershell
.\.venv\Scripts\streamlit.exe run run_dashboard.py
```
This opens the web control panel where you can:
- Generate complete campaign packages.
- Monitor live or simulated ads in real-time.
- Click **"Run Autonomous Optimizer"** to auto-kill bleeders and scale winners.
- Manually pause or activate any ad.

### 3. Or Run via Terminal CLI
```powershell
.\.venv\Scripts\python.exe run_cli.py
```

---

## 🔑 Connecting Your Live API Keys

Open the `.env` file in `agency-growth-ai/`:

1. **Google Gemini API Key** (Free):
   - Get key at: https://aistudio.google.com
   - Set: `GEMINI_API_KEY=AIzaSy...`
2. **Meta Marketing API** (To auto-pause live Facebook/Instagram ads):
   - Go to: https://developers.facebook.com
   - Generate Access Token with `ads_management` and `ads_read` permissions.
   - Set `META_ACCESS_TOKEN=EAAB...` and `META_AD_ACCOUNT_ID=act_123456789`.

*Note: If no API keys are provided yet, the system automatically runs in **High-Fidelity Simulation Sandbox Mode**, allowing full testing of campaigns, ad monitoring, and auto-pause triggers without errors.*

---

## 🛡️ Financial Safeguards & Guardrails
- **Bleeder Rule:** Automatically pauses any ad that spends more than `2.5x Target CPA` with 0 leads.
- **High CPC Rule:** Automatically stops ads where click costs spike beyond acceptable limits.
- **Creative Fatigue Alert:** Flags ads where audience frequency exceeds 3.2.
- **Budget Scaling:** Scaled strictly in +20% increments to avoid breaking Meta's machine learning phase.
- **Hard Spend Cap:** Prevents daily budget from ever exceeding the user-configured cap (e.g. ₹5,000/day).
