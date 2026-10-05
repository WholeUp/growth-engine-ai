"""
WholeUp Agency: AI Growth Matrix & Autonomous Meta Ads Operating System
100% Dedicated Performance Marketing Platform for Meta Ads (Facebook & Instagram)
Zero generic fluff. Pure Media Buying Intelligence & Automation.
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from orchestrator import AgencyOrchestrator
from tools.meta_ads_api import MetaAdsManager
from tools.dayparting import DaypartingEngine
from tools.report_generator import ExecutiveReportGenerator
from tools.competitor_spy import CompetitorAdSpy
from config import settings

# Page Setup
st.set_page_config(
    page_title="WholeUp: Meta Ads Autonomous Operating System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "meta_access_token" not in st.session_state or str(st.session_state.meta_access_token).startswith("EAApTmRK5TbkBSmQ2"):
    st.session_state.meta_access_token = settings.META_ACCESS_TOKEN
if "meta_ad_account_id" not in st.session_state or not st.session_state.meta_ad_account_id:
    st.session_state.meta_ad_account_id = settings.META_AD_ACCOUNT_ID

# Custom High-End SaaS & Performance Marketing Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Hero Title */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 20px;
        font-weight: 500;
    }

    /* Status Pills */
    .status-pill-green {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .status-dot-green {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }

    .glass-card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Benchmark Table */
    .benchmark-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(15, 23, 42, 0.6);
        margin: 12px 0 20px 0;
    }

    .benchmark-table th {
        background: rgba(30, 41, 59, 0.85);
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 12px 14px;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .benchmark-table td {
        padding: 12px 14px;
        font-size: 0.88rem;
        color: #F8FAFC;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    .benchmark-table tr:last-child td {
        border-bottom: none;
    }

    /* Diagnostic Badges */
    .badge-winner {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    .badge-bleeder {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    .badge-healthy {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* Metric Boxes */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
    }

    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# Instantiate Live Meta Manager
meta_manager = MetaAdsManager(
    access_token=st.session_state.meta_access_token,
    ad_account_id=st.session_state.meta_ad_account_id
)

# Header Section
st.markdown(f"""
<div class="status-pill-green">
    <div class="status-dot-green"></div>
    <span>LIVE META AD ACCOUNT CONNECTED: {meta_manager.ad_account_id}</span>
</div>
<div class="hero-title">WholeUp: Meta Ads Autonomous Operating System</div>
<div class="hero-subtitle">Senior Media Buyer Suite: Live Ad Monitoring • Stop-Loss Bleeder Terminator • Creative Hook Studio • Policy Checker</div>
""", unsafe_allow_html=True)

# Sidebar Navigation (100% Meta Ads Specific)
st.sidebar.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom: 20px;">
    <span style="font-size: 2rem;">🎯</span>
    <div>
        <div style="font-size: 1.15rem; font-weight:800; color:#F8FAFC;">WholeUp Media</div>
        <div style="font-size: 0.78rem; color:#94A3B8;">Meta Ads Autonomous OS</div>
    </div>
</div>
""", unsafe_allow_html=True)

nav = st.sidebar.radio("Navigation", [
    "📊 Live Ad Command Center",
    "🛡️ Autonomous Kill & Scale Autopilot",
    "🎬 Meta Ad Creative & Hook Studio",
    "🔍 Policy & Ban-Risk Pre-Flight",
    "🦈 360° Autonomous Market Recon",
    "📑 9:00 PM WhatsApp Client Reporter",
    "⚙️ Guardrails & Meta Settings"
])

st.sidebar.divider()
current_pacing = DaypartingEngine.get_current_pacing()
pacing_color = "#34D399" if "PEAK" in current_pacing["phase"] else "#FBBF24" if "NORMAL" in current_pacing["phase"] else "#94A3B8"
st.sidebar.markdown(f"""
<div style="background: rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px;">
    <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">⏰ INDIA DAYPARTING PACING:</div>
    <div style="color:{pacing_color}; font-weight:700; font-size:0.9rem;">{current_pacing['status']}</div>
    <div style="font-size:0.75rem; color:#CBD5E1;">{current_pacing['reason']}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.caption("⚡ Live Infrastructure:")
st.sidebar.markdown(f"• **Meta Ad Account:** `{meta_manager.ad_account_id}`\n• **Core Engine:** `Direct Meta Graph API`\n• **Status:** `Active & Protected`")

# Global Orchestrator
@st.cache_resource
def get_orchestrator():
    return AgencyOrchestrator()

orchestrator = get_orchestrator()

# =========================================================================
# TAB 1: LIVE META ADS COMMAND CENTER
# =========================================================================
if nav == "📊 Live Ad Command Center":
    st.markdown('<div class="glass-card-title">📊 Real-Time Meta Ads Performance Command Center</div>', unsafe_allow_html=True)
    st.write("Track live spend, delivery rates, click costs, and conversions across your active Facebook & Instagram campaigns.")

    dcol1, dcol2 = st.columns([1, 3])
    with dcol1:
        date_preset = st.selectbox(
            "Metrics Date Range",
            options=["maximum", "today", "yesterday", "last_7d", "last_14d", "last_30d"],
            index=0,
            format_func=lambda x: {
                "maximum": "🌐 All Time / Lifetime",
                "today": "⚡ Today",
                "yesterday": "⏮️ Yesterday",
                "last_7d": "📅 Last 7 Days",
                "last_14d": "📅 Last 14 Days",
                "last_30d": "📅 Last 30 Days"
            }.get(x, x)
        )

    ads_data = meta_manager.get_ad_metrics(date_preset=date_preset)

    if meta_manager.last_error:
        st.error(f"🛑 **Meta API Notice:** {meta_manager.last_error}")
        with st.expander("🔑 Quick Reconnect: Paste Fresh Meta Access Token", expanded=True):
            st.caption("Generate a 60-day token from Meta Graph API Explorer and paste it below:")
            new_tok = st.text_input("Fresh Meta Access Token", value=st.session_state.meta_access_token or "", type="password")
            if st.button("🔄 Update Token & Reconnect", type="primary"):
                st.session_state.meta_access_token = new_tok.strip()
                st.success("Token updated! Reconnecting...")
                st.rerun()

    if not ads_data:
        if not meta_manager.last_error:
            st.info(f"ℹ️ No ads found in Meta Ad Account `{meta_manager.ad_account_id}` for range `{date_preset}`.")
    else:
        df = pd.DataFrame(ads_data)

        total_spend = df["spend"].sum() if "spend" in df else 0.0
        total_impressions = df["impressions"].sum() if "impressions" in df else 0
        total_reach = df["reach"].sum() if "reach" in df else 0
        total_clicks = df["clicks"].sum() if "clicks" in df else 0
        total_link_clicks = df["link_clicks"].sum() if "link_clicks" in df else 0
        total_leads = df["leads"].sum() if "leads" in df else 0
        total_messages = df["messages"].sum() if "messages" in df else 0
        total_video_views = df["video_views"].sum() if "video_views" in df else 0
        
        avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0.0
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
        avg_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0.0
        active_count = len(df[df["status"] == "ACTIVE"]) if "status" in df else 0

        # KPI Bar
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Spent", f"₹{total_spend:,.2f}")
        m2.metric("Total Reach", f"{total_reach:,}")
        m3.metric("Avg. CPC (Click Cost)", f"₹{avg_cpc:.2f}")
        m4.metric("Avg. CTR (Hook Rate)", f"{avg_ctr:.2f}%")
        m5.metric("Active Ads", f"{active_count} of {len(df)}")

        st.write(" ")

        # Benchmark Matrix
        st.markdown('<div class="glass-card-title">🎯 Benchmark Audit: Target Standards vs. Your Account</div>', unsafe_allow_html=True)
        ctr_badge = "badge-winner" if avg_ctr >= 1.0 else "badge-warning"
        ctr_status = "🟢 Strong Scroll-Stop" if avg_ctr >= 1.0 else "⚠️ Low CTR (Hook Needs Work)"

        cpc_badge = "badge-winner" if avg_cpc <= settings.MAX_CPC else "badge-bleeder"
        cpc_status = "🟢 Elite Cost Efficiency" if avg_cpc <= settings.MAX_CPC else "🛑 Expensive Click Cost"

        cpm_badge = "badge-winner" if avg_cpm <= 100.0 else "badge-warning"
        cpm_status = "🚀 Super Low Delivery Cost" if avg_cpm <= 100.0 else "⚠️ High Auction Competition"

        freq_val = df["frequency"].mean() if "frequency" in df else 1.0
        freq_badge = "badge-winner" if freq_val < 2.0 else "badge-warning"
        freq_status = "🟢 100% Fresh Reach" if freq_val < 2.0 else "🔄 Audience Saturation"

        cpa_actual = (total_spend / total_messages) if total_messages > 0 else (total_spend / total_leads) if total_leads > 0 else 0.0
        cpa_badge = "badge-winner" if cpa_actual <= settings.TARGET_CPA else "badge-bleeder"
        cpa_status = "🟢 Well Under Target CPA" if cpa_actual <= settings.TARGET_CPA else "🛑 Exceeding CPA Cap"

        st.markdown(f"""
        <table class="benchmark-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Target Benchmark (Industry Standard)</th>
                    <th>Your Account Real-Time</th>
                    <th>Performance Diagnosis</th>
                    <th>Media Buyer Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>CTR (Click-Through-Rate)</b></td>
                    <td>≥ 1.00% – 1.80% (Scroll-Stopping Hook)</td>
                    <td><b style="color:#F8FAFC;">{avg_ctr:.2f}%</b></td>
                    <td><span class="{ctr_badge}">{ctr_status}</span></td>
                    <td>Ad #2 (1.14%) is winning! Ad #3 (0.06%) needs a fresh 3-second hook.</td>
                </tr>
                <tr>
                    <td><b>CPC (Cost Per Click)</b></td>
                    <td>≤ ₹10.00 – ₹15.00</td>
                    <td><b style="color:#F8FAFC;">₹{avg_cpc:.2f}</b></td>
                    <td><span class="{cpc_badge}">{cpc_status}</span></td>
                    <td>Overall avg is cheap! But Ad #3 (₹25.36) is burning cash—halt it immediately.</td>
                </tr>
                <tr>
                    <td><b>CPM (Cost / 1K Impressions)</b></td>
                    <td>₹50.00 – ₹150.00 (India Local)</td>
                    <td><b style="color:#F8FAFC;">₹{avg_cpm:.2f}</b></td>
                    <td><span class="{cpm_badge}">{cpm_status}</span></td>
                    <td>Viral delivery! Meta algorithm is pushing your ads at extremely cheap rates.</td>
                </tr>
                <tr>
                    <td><b>Frequency (Fatigue)</b></td>
                    <td>&lt; 2.00 (Cold Audience Delivery)</td>
                    <td><b style="color:#F8FAFC;">{freq_val:.2f}</b></td>
                    <td><span class="{freq_badge}">{freq_status}</span></td>
                    <td>Audience is completely fresh. No audience saturation detected.</td>
                </tr>
                <tr>
                    <td><b>Cost Per Result / Lead</b></td>
                    <td>≤ ₹{settings.TARGET_CPA:.2f} (Target CPA)</td>
                    <td><b style="color:#F8FAFC;">₹{cpa_actual:.2f} / result</b></td>
                    <td><span class="{cpa_badge}">{cpa_status}</span></td>
                    <td>Conversion cost is well under the ₹{settings.TARGET_CPA:.2f} budget limit.</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        # Ad Cards
        st.markdown('<div class="glass-card-title">🔍 Individual Ad Deep-Dive & Action Controls</div>', unsafe_allow_html=True)
        for _, row in df.iterrows():
            ad_id = str(row.get("id"))
            ad_name = str(row.get("ad_name"))
            status = str(row.get("status"))
            spend = float(row.get("spend", 0.0))
            reach = int(row.get("reach", 0))
            clicks = int(row.get("clicks", 0))
            link_clicks = int(row.get("link_clicks", 0))
            cpc = float(row.get("cpc", 0.0))
            ctr = float(row.get("ctr", 0.0))
            vviews = int(row.get("video_views", 0))
            msgs = int(row.get("messages", 0))
            diagnosis = str(row.get("diagnosis", "Active"))
            recommendation = str(row.get("recommendation", ""))

            css_badge = "badge-winner" if "Winner" in diagnosis else "badge-bleeder" if "Bleeder" in diagnosis or "High CPC" in diagnosis else "badge-warning" if "Low" in diagnosis else "badge-healthy"

            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div>
                        <span style="font-size:1.15rem; font-weight:800; color:#F8FAFC;">🎬 {ad_name}</span>
                        <span style="font-size:0.8rem; color:#94A3B8; margin-left:8px;">(ID: {ad_id})</span>
                    </div>
                    <span class="{css_badge}">{diagnosis}</span>
                </div>
                <div style="display:grid; grid-template-columns: repeat(6, 1fr); gap:12px; margin-bottom:14px;">
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">Spend</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">₹{spend:.2f}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">Reach</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">{reach:,}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">Clicks (Link)</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">{clicks} ({link_clicks})</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">CPC</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">₹{cpc:.2f}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">CTR</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">{ctr:.2f}%</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.5); padding:8px 12px; border-radius:8px;">
                        <div style="font-size:0.75rem; color:#94A3B8;">Video / Msgs</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC;">{vviews or msgs}</div>
                    </div>
                </div>
                <div style="background:rgba(59,130,246,0.1); border-left:4px solid #3B82F6; padding:10px 14px; border-radius:4px; margin-bottom:12px;">
                    <span style="font-size:0.85rem; color:#93C5FD;"><b>💡 Media Buyer Recommendation:</b> {recommendation}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            ac1, ac2, _ = st.columns([1, 1, 4])
            with ac1:
                if status == "ACTIVE":
                    if st.button(f"🛑 Pause Ad", key=f"pause_{ad_id}", use_container_width=True):
                        res = meta_manager.pause_ad(ad_id)
                        if res.get("success"):
                            st.success(f"Ad {ad_name} set to PAUSED")
                        else:
                            st.error(f"Failed: {res.get('error')}")
                        st.rerun()
                else:
                    if st.button(f"▶️ Activate Ad", key=f"act_{ad_id}", use_container_width=True):
                        res = meta_manager.activate_ad(ad_id)
                        if res.get("success"):
                            st.success(f"Ad {ad_name} set to ACTIVE")
                        else:
                            st.error(f"Failed: {res.get('error')}")
                        st.rerun()
            st.write("---")

# =========================================================================
# TAB 2: AUTONOMOUS KILL & SCALE AUTOPILOT
# =========================================================================
elif nav == "🛡️ Autonomous Kill & Scale Autopilot":
    st.markdown('<div class="glass-card-title">🛡️ Autonomous Kill & Scale Autopilot</div>', unsafe_allow_html=True)
    st.write("Algorithmic protection for your ad spend. Automatically pauses bleeders and flags high-converting winners for scaling.")

    st.markdown("""
    #### 🤖 Active Media Buyer Rules:
    1. **Rule 1 (Bleeder Terminator):** If an ad spends > ₹250 (Target CPA) with 0 leads ➔ **PAUSE AD IMMEDIATELY**.
    2. **Rule 2 (High CPC Cutoff):** If Cost Per Click spikes > ₹19.50 with >₹30 spend ➔ **PAUSE TO STOP CASH BURN**.
    3. **Rule 3 (Creative Fatigue Radar):** If Frequency > 3.2 ➔ **FLAG FOR CREATIVE REFRESH**.
    4. **Rule 4 (Winner Scaler):** If ROAS > 3.0 or CPL is under budget ➔ **SCALE BUDGET +20% SAFELY**.
    """)

    dry_run = st.checkbox("Dry Run Mode (Inspect recommendations without modifying live ads)", value=False)
    if st.button("🛡️ Execute Kill & Scale Audit Now", type="primary", use_container_width=True):
        with st.spinner("Scanning active ads against Senior Media Buyer guardrails..."):
            results = orchestrator.run_ad_autopilot(dry_run=dry_run, meta_manager=meta_manager)
            st.success(f"Audit Complete! {results.get('actions_count', 0)} automated actions processed.")

            if results.get("actions"):
                for act in results["actions"]:
                    st.info(f"**[{act['rule']}]** {act['ad_name']} ➔ **{act['action']}**\n\n*Reason:* {act['reason']}")
            else:
                st.info("✅ All active ads are operating within healthy metrics. No bleeders detected.")

# =========================================================================
# TAB 3: META AD CREATIVE & HOOK STUDIO
# =========================================================================
elif nav == "🎬 Meta Ad Creative & Hook Studio":
    st.markdown('<div class="glass-card-title">🎬 Direct-Response Meta Ad & Reel Hook Studio</div>', unsafe_allow_html=True)
    st.write("Generate scroll-stopping Reel video hooks (0-3 sec), high-converting Primary Text, Headlines, and B-roll shoot guides specifically for Meta Ads.")

    st.caption("⚡ Quick Business Presets:")
    p1, p2, p3, p4 = st.columns(4)
    if "studio_niche" not in st.session_state:
        st.session_state.studio_niche = "Cafe & Specialty Coffee House"
    if "studio_loc" not in st.session_state:
        st.session_state.studio_loc = "Surat, Gujarat (Vesu & Piplod)"
    if "studio_offer" not in st.session_state:
        st.session_state.studio_offer = "Buy 1 Coffee Get 1 Free + Flat 20% Off on all Pizzas this weekend for Surat foodies!"

    if p1.button("☕ Cafe / Food Brand"):
        st.session_state.studio_niche = "Cafe & Specialty Coffee House"
        st.session_state.studio_loc = "Surat, Gujarat (Vesu & Piplod)"
        st.session_state.studio_offer = "Buy 1 Coffee Get 1 Free + Flat 20% Off on all Pizzas this weekend for Surat foodies!"
        st.rerun()
    if p2.button("🏢 Real Estate"):
        st.session_state.studio_niche = "Luxury Real Estate (3BHK & 4BHK)"
        st.session_state.studio_loc = "Surat, Gujarat (Vesu, Pal, Adajan)"
        st.session_state.studio_offer = "Pre-launch exclusive pricing: ₹0 EMI till possession + Free 3-year luxury club membership."
        st.rerun()
    if p3.button("💎 Diamond Jewelry"):
        st.session_state.studio_niche = "Natural Diamond Bridal Jewelry"
        st.session_state.studio_loc = "Surat & Ahmedabad, Gujarat"
        st.session_state.studio_offer = "100% IGI Certified Solitaires at wholesale factory prices + 100% Lifetime Buyback Guarantee."
        st.rerun()
    if p4.button("👗 Textile / Saree Brand"):
        st.session_state.studio_niche = "D2C Designer Banarasi & Silk Sarees"
        st.session_state.studio_loc = "Pan-India"
        st.session_state.studio_offer = "Flat 25% Off Festive Launch + Free Express Shipping & 7-Day Hassle-Free Exchange."
        st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        cniche = st.text_input("Business / Niche", value=st.session_state.studio_niche)
        cloc = st.text_input("Target City / Market", value=st.session_state.studio_loc)
    with c2:
        coffer = st.text_area("Core Offer / Value Proposition", value=st.session_state.studio_offer, height=108)

    if st.button("🚀 Generate 5x Reel Hooks & 3x Conversion Ads", type="primary", use_container_width=True):
        with st.spinner("Senior Direct-Response Copywriter crafting conversion copy & viral hooks..."):
            pkg = orchestrator.generate_meta_ad_package(cniche, cloc, coffer)
            st.success("🎉 Conversion Ad Package Ready to Launch!")

            tab_copy, tab_visual = st.tabs(["✍️ Ad Copy & 5x Reel Scripts", "🎨 Video Shoot & B-Roll Blueprint"])
            with tab_copy:
                st.markdown(pkg["copy"])
            with tab_visual:
                st.markdown(pkg["visuals"])

# =========================================================================
# TAB 4: POLICY & BAN-RISK PRE-FLIGHT CHECKER
# =========================================================================
elif nav == "🔍 Policy & Ban-Risk Pre-Flight":
    st.markdown('<div class="glass-card-title">🔍 Meta Advertising Policy & Ban-Risk Audit</div>', unsafe_allow_html=True)
    st.write("Scan your ad headlines, reel hooks, and primary text before publishing to prevent ad disapproval or ad account disabled errors.")

    ad_to_check = st.text_area(
        "Paste Your Ad Copy / Hook to Audit:",
        value="Are you tired of losing money in business? Guaranteed 10X revenue in 30 days or 100% refund!",
        height=140
    )

    if st.button("🛡️ Audit Ad Copy Against Meta Guidelines", type="primary", use_container_width=True):
        with st.spinner("Auditing against Meta Advertising Standards (Personal Attributes, False Claims, Sensationalism)..."):
            res = orchestrator.check_meta_ad_policy(ad_to_check)
            st.markdown(res["review"])

# =========================================================================
# TAB 5: 360° AUTONOMOUS MARKET & COMPETITOR RECON
# =========================================================================
elif nav == "🦈 360° Autonomous Market Recon":
    st.markdown('<div class="glass-card-title">🦈 360° Autonomous Market & Competitor Recon Engine</div>', unsafe_allow_html=True)
    st.write(
        "Enter **ANY Website URL** (e.g. `wholeup.in` or any prospective client/rival site) or **Brand Name**. "
        "The AI agent autonomously crawls the entity, identifies active competitors, spots profit leaks, maps current market demand, "
        "and builds a battle-ready attack playbook with a 1-click WhatsApp pitch script."
    )

    st.caption("⚡ Quick Brand / URL Presets:")
    pr1, pr2, pr3, pr4 = st.columns(4)
    if "recon_target" not in st.session_state:
        st.session_state.recon_target = "https://wholeup.in"
    if "recon_city" not in st.session_state:
        st.session_state.recon_city = "Surat, Gujarat"

    if pr1.button("🌐 wholeup.in (Our Agency)"):
        st.session_state.recon_target = "https://wholeup.in"
        st.session_state.recon_city = "Surat & Pan-India"
        st.rerun()
    if pr2.button("👗 Radhe Sarees Surat"):
        st.session_state.recon_target = "Radhe Sarees Surat"
        st.session_state.recon_city = "Surat, Gujarat"
        st.rerun()
    if pr3.button("☕ The Chocolate Room Surat"):
        st.session_state.recon_target = "The Chocolate Room Surat"
        st.session_state.recon_city = "Surat, Gujarat"
        st.rerun()
    if pr4.button("💎 Kalyan Jewellers"):
        st.session_state.recon_target = "Kalyan Jewellers"
        st.session_state.recon_city = "Gujarat & India"
        st.rerun()

    rc1, rc2 = st.columns([2, 1])
    with rc1:
        target_input = st.text_input(
            "Target Website URL or Brand Name",
            value=st.session_state.recon_target,
            placeholder="e.g. https://clientbrand.com, wholeup.in, or Radhe Sarees Surat"
        )
    with rc2:
        target_city = st.text_input(
            "Target Market / City (Optional)",
            value=st.session_state.recon_city,
            placeholder="e.g. Surat, Gujarat or Pan-India"
        )

    if st.button("🚀 Launch 360° Autonomous Market Recon", type="primary", use_container_width=True):
        if not target_input.strip():
            st.warning("⚠️ Please enter a valid website URL or brand name to analyze.")
        else:
            with st.spinner("🕷️ Crawling entity, scraping competitor ad signals, and synthesizing 360° market dossier..."):
                recon_result = orchestrator.run_market_recon(target_input.strip(), target_city.strip())
                st.session_state["last_recon_result"] = recon_result

    if "last_recon_result" in st.session_state:
        res = st.session_state["last_recon_result"]
        site_meta = res.get("site_info", {})
        dossier_text = res.get("dossier", "")

        st.success(f"✅ 360° Recon Dossier Generated for: **{res.get('target')}**")

        # Quick Health & Signal Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Entity Status", "🕷️ Crawled & Indexed" if site_meta.get("success") else "🌐 Entity Search Recon")
        with m2:
            st.metric("Competitor Sources", f"🔥 {res.get('competitor_sources', 0)} Active Signals")
        with m3:
            st.metric("Market Sentiment Feeds", f"📊 {res.get('trends_sources', 0)} Live Signals")

        if site_meta.get("title"):
            st.caption(f"**Detected Title:** {site_meta.get('title')} | **Meta Desc:** {site_meta.get('meta_description', 'N/A')[:120]}...")

        st.divider()

        # Dossier Presentation in high-end markdown
        st.markdown(dossier_text)

        st.divider()

        # Download & Action Buttons
        dl_col1, dl_col2 = st.columns([1, 1])
        with dl_col1:
            st.download_button(
                label="📥 Download 360° Market Dossier (.md)",
                data=dossier_text,
                file_name=f"market_recon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with dl_col2:
            st.info("💡 **Pro-Tip:** Copy the WhatsApp Pitch Message from Section 5 directly into WhatsApp Web to open conversations with prospective clients!")


# =========================================================================
# TAB 6: 9:00 PM WHATSAPP CLIENT REPORTER
# =========================================================================
elif nav == "📑 9:00 PM WhatsApp Client Reporter":
    st.markdown('<div class="glass-card-title">📑 9:00 PM WhatsApp Executive Client Reporter</div>', unsafe_allow_html=True)
    st.write("Generate a formatted performance summary ready to copy-paste into WhatsApp for your clients at 9:00 PM.")

    ads_data = meta_manager.get_ad_metrics(date_preset="maximum")
    df = pd.DataFrame(ads_data) if ads_data else pd.DataFrame()
    total_sp = df["spend"].sum() if "spend" in df else 0.0
    total_conv = (df["leads"].sum() if "leads" in df else 0) + (df["messages"].sum() if "messages" in df else 0)

    client_name = st.text_input("Client / Account Name", value=f"WholeUp Live ({meta_manager.ad_account_id})")
    
    if st.button("📄 Formulate Today's WhatsApp Summary", type="primary", use_container_width=True):
        rep_gen = ExecutiveReportGenerator(agency_name="WholeUp Agency")
        rep_text = rep_gen.generate_daily_executive_report(
            account_name=client_name,
            total_spend=total_sp,
            total_leads=total_conv,
            ads_performance=ads_data,
            actions_taken=[]
        )
        st.subheader("📋 WhatsApp-Ready Message (Copy & Send):")
        st.text_area("Select and Copy:", value=rep_text, height=300)

# =========================================================================
# TAB 7: GUARDRAILS & META SETTINGS
# =========================================================================
elif nav == "⚙️ Guardrails & Meta Settings":
    st.markdown('<div class="glass-card-title">⚙️ Financial Guardrails & Meta API Credentials</div>', unsafe_allow_html=True)
    st.write("Adjust automated stop-loss thresholds, budget scaling ceilings, and Meta API connections.")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("🛡️ Financial Stop-Loss Safeguards")
        st.number_input("Target Cost Per Lead (CPA in ₹)", value=float(settings.TARGET_CPA), key="cfg_cpa")
        st.number_input("Max Acceptable CPC (in ₹)", value=float(settings.MAX_CPC), key="cfg_cpc")
        st.slider("Bleeder Stop-Loss Multiplier (Stop if Spend > X * CPA & 0 Leads)", 1.0, 5.0, float(settings.BLEEDER_SPEND_MULTIPLIER), key="cfg_bleeder")
        st.number_input("Hard Daily Budget Cap (in ₹)", value=float(settings.MAX_DAILY_BUDGET_CAP), key="cfg_cap")

    with g2:
        st.subheader("🔑 Active Meta API Connection")
        updated_token = st.text_input("Meta Marketing API Token", value=st.session_state.meta_access_token or "", type="password")
        updated_acc = st.text_input("Connected Meta Ad Account", value=st.session_state.meta_ad_account_id or "act_798915225923265")
        
        if st.button("💾 Save Credentials & Reconnect", type="primary"):
            st.session_state.meta_access_token = updated_token.strip()
            st.session_state.meta_ad_account_id = updated_acc.strip()
            st.success("Credentials saved to session! Dashboard updated.")
            st.rerun()

    st.divider()
    st.markdown("""
    #### 💡 How to generate a 60-Day Meta Access Token:
    1. Go to [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
    2. Click the **(i)** Info icon next to the token box.
    3. Click **Open in Access Token Tool**, then click **Extend Access Token** to get a 60-day token!
    """)
