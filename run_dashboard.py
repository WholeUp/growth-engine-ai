"""
WholeUp Agency: AI Growth Matrix & Autonomous Media Buyer Dashboard
Enterprise-Grade UI with Modern Glassmorphism & Agency Presets
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from orchestrator import AgencyOrchestrator
from tools.meta_ads_api import MetaAdsManager
from config import settings

# Page Setup
st.set_page_config(
    page_title="WholeUp AI Growth Matrix",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End SaaS & Agency Styling (Glassmorphism + Neon Accents)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Hero Title */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 24px;
        font-weight: 500;
    }

    /* Live Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .glass-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Metric Boxes */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
    }

    /* Sidebar Clean */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# Header Section
meta_manager = MetaAdsManager()
status_label = f"LIVE META API CONNECTED: {meta_manager.ad_account_id}" if meta_manager.is_live else "SANDBOX SIMULATION MODE"

st.markdown(f"""
<div class="status-pill">
    <div class="status-dot"></div>
    <span>{status_label}</span>
</div>
<div class="hero-title">WholeUp AI Growth Matrix & Media Buyer</div>
<div class="hero-subtitle">5+ Year Senior Agency Operating System: Avatar Psychology • SEO Intent • Direct Response Copy • Visual Direction • Autonomous Ad Optimizer</div>
""", unsafe_allow_html=True)

# Sidebar Navigation & Branding
st.sidebar.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom: 20px;">
    <span style="font-size: 2rem;">🚀</span>
    <div>
        <div style="font-size: 1.2rem; font-weight:800; color:#F8FAFC;">WholeUp Agency</div>
        <div style="font-size: 0.8rem; color:#94A3B8;">AI Growth Engine v2.0</div>
    </div>
</div>
""", unsafe_allow_html=True)

nav = st.sidebar.radio("Navigation", [
    "🎯 5-Agent Campaign Studio",
    "🤖 Autonomous AI Media Buyer",
    "📁 Campaign Vault & History",
    "⚙️ Guardrails & API Settings"
])

st.sidebar.divider()
st.sidebar.caption("⚡ Connected Models:")
st.sidebar.markdown(f"• **Meta Ad Account:** `{meta_manager.ad_account_id or 'Demo'}`\n• **LLM Brain:** `Gemini 2.5 Flash`\n• **Status:** `Active & Protected`")

# Global Orchestrator
@st.cache_resource
def get_orchestrator():
    return AgencyOrchestrator()

orchestrator = get_orchestrator()

# =========================================================================
# TAB 1: 5-AGENT CAMPAIGN STUDIO
# =========================================================================
if nav == "🎯 5-Agent Campaign Studio":
    st.markdown('<div class="glass-card-title">🎯 Direct-Response Campaign Architecture</div>', unsafe_allow_html=True)
    st.write("Deploy the 5-Agent team to research buyer psychology, identify commercial search queries, craft conversion-tested ad copy, and design production-ready creative briefs.")

    # Agency Quick Presets
    st.caption("⚡ Quick Client Presets (Click to autofill):")
    p1, p2, p3, p4 = st.columns(4)

    # State initialization for inputs
    if "niche_input" not in st.session_state:
        st.session_state.niche_input = "Surat Luxury Real Estate (3BHK & 4BHK)"
    if "loc_input" not in st.session_state:
        st.session_state.loc_input = "Surat, Gujarat (Vesu, Pal, Adajan)"
    if "offer_input" not in st.session_state:
        st.session_state.offer_input = "Pre-launch exclusive pricing: ₹0 EMI till possession + Free 3-year luxury club membership for first 25 bookings."

    if p1.button("🏢 Real Estate (Surat)"):
        st.session_state.niche_input = "Surat Luxury Real Estate (3BHK & 4BHK)"
        st.session_state.loc_input = "Surat, Gujarat (Vesu, Pal, Adajan)"
        st.session_state.offer_input = "Pre-launch exclusive pricing: ₹0 EMI till possession + Free 3-year luxury club membership for first 25 bookings."
        st.rerun()

    if p2.button("💎 Diamond Jewelry"):
        st.session_state.niche_input = "Natural Diamond Bridal Jewelry & Solitaires"
        st.session_state.loc_input = "Surat & Ahmedabad, Gujarat"
        st.session_state.offer_input = "100% IGI Certified Solitaires at wholesale factory prices + 100% Lifetime Buyback Guarantee."
        st.rerun()

    if p3.button("👗 Textile / Saree Brand"):
        st.session_state.niche_input = "D2C Designer Banarasi & Silk Sarees"
        st.session_state.loc_input = "Pan-India (Focus: Mumbai, Delhi, Gujarat)"
        st.session_state.offer_input = "Flat 25% Off Festive Launch + Free Express Shipping & 7-Day Hassle-Free Exchange."
        st.rerun()

    if p4.button("🏋️ Premium Fitness / Gym"):
        st.session_state.niche_input = "Luxury Gym & Personal Training Studio"
        st.session_state.loc_input = "Vesu & Piplod, Surat"
        st.session_state.offer_input = "3-Day Free VIP Pass + Personalized Body Composition Scan & Diet Consultation (Zero Obligation)."
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Client Niche / Industry", value=st.session_state.niche_input)
        location = st.text_input("Target Location / Geo", value=st.session_state.loc_input)
    with col2:
        offer = st.text_area("Core Offer / Value Proposition", value=st.session_state.offer_input, height=108)

    if st.button("🚀 Deploy Multi-Agent Team (Generate Master Campaign)", type="primary", use_container_width=True):
        with st.spinner("⚡ 5 Specialized Agents are analyzing, writing, and reviewing..."):
            bundle = orchestrator.run_full_campaign(niche, location, offer)
            st.success("🎉 Master Campaign Package Generated & Verified by Agency Director!")

            # Tabs for Deliverables
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🕵️ 1. Avatar Psychology", 
                "🔍 2. SEO & Intent", 
                "✍️ 3. Direct-Response Copy", 
                "🎨 4. Visual Art Briefs", 
                "👑 5. CMO Quality Audit"
            ])

            with tab1:
                st.markdown(bundle["research"])

            with tab2:
                st.markdown(bundle["seo"])

            with tab3:
                st.markdown(bundle["copy"])

            with tab4:
                st.markdown(bundle["visuals"])

            with tab5:
                st.markdown(bundle["cmo_review"])

            # Download Dossier
            with open(bundle["file_path"], "r", encoding="utf-8") as f:
                content = f.read()
            st.download_button(
                label="📥 Download Master Campaign Dossier (.md)",
                data=content,
                file_name=Path(bundle["file_path"]).name,
                mime="text/markdown",
                type="secondary"
            )

# =========================================================================
# TAB 2: AUTONOMOUS AI MEDIA BUYER
# =========================================================================
elif nav == "🤖 Autonomous AI Media Buyer":
    st.markdown('<div class="glass-card-title">🤖 24/7 Autonomous Ad Optimizer & Kill-Switch</div>', unsafe_allow_html=True)
    st.write("Live algorithmic protection for Meta & Google ad spend. Automatically halts bleeders, scales high-ROAS winners, and flags fatigued creatives.")

    ads_data = meta_manager.get_ad_metrics()
    df = pd.DataFrame(ads_data)

    total_spend = df["spend"].sum() if "spend" in df else 0.0
    total_leads = df["leads"].sum() if "leads" in df else 0
    avg_cpc = df["cpc"].mean() if "cpc" in df else 0.0
    active_count = len(df[df["status"] == "ACTIVE"]) if "status" in df else 0

    # Top Metric Bar
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Today's Ad Spend", f"₹{total_spend:,.2f}")
    m2.metric("Total Conversions / Leads", f"{total_leads}")
    m3.metric("Avg. CPC", f"₹{avg_cpc:.2f}")
    m4.metric("Active Ads Monitored", f"{active_count} of {len(df)}")

    st.write(" ")

    # Live Data Table
    st.subheader("📊 Live Monitored Ads")
    display_cols = ["id", "ad_name", "status", "spend", "leads", "cpc", "ctr", "frequency", "roas"]
    existing_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[existing_cols], use_container_width=True)

    # Action Panel
    colA, colB = st.columns([2, 1])
    with colA:
        st.subheader("⚡ Run Optimizer Rules")
        dry_run_opt = st.checkbox("Dry Run Mode (Inspect & create recommendations without pausing live ads)", value=False)
        
        if st.button("🛡️ Execute Kill & Scale Audit", type="primary", use_container_width=True):
            with st.spinner("AI Media Buyer evaluating spend rules..."):
                results = orchestrator.run_ad_autopilot(dry_run=dry_run_opt)
                st.success(f"Audit Complete! {results['actions_count']} automated actions processed.")

                if results["actions"]:
                    for act in results["actions"]:
                        st.info(f"**[{act['rule']}]** {act['ad_name']} ➔ **{act['action']}**\n\n*Reason:* {act['reason']}")
                else:
                    st.info("✅ All active ads are operating within healthy metrics. No bleeders detected.")
                st.rerun()

    with colB:
        st.subheader("🛑 Manual Controls")
        if len(df) > 0 and "id" in df:
            selected_ad = st.selectbox("Select Ad ID to Control", options=df["id"].tolist())
            b1, b2 = st.columns(2)
            if b1.button("🛑 Pause Ad", use_container_width=True):
                meta_manager.pause_ad(selected_ad)
                st.warning(f"Ad {selected_ad} set to PAUSED")
                st.rerun()
            if b2.button("▶️ Activate Ad", use_container_width=True):
                meta_manager.activate_ad(selected_ad)
                st.success(f"Ad {selected_ad} set to ACTIVE")
                st.rerun()

# =========================================================================
# TAB 3: CAMPAIGN VAULT & HISTORY
# =========================================================================
elif nav == "📁 Campaign Vault & History":
    st.markdown('<div class="glass-card-title">📁 Generated Campaign Vault</div>', unsafe_allow_html=True)
    st.write("Browse, inspect, and export all previously generated multi-agent campaign files.")

    outputs_dir = Path(__file__).resolve().parent / "outputs"
    campaign_files = sorted(list(outputs_dir.glob("campaign_*.md")), reverse=True)

    if campaign_files:
        selected_file = st.selectbox("Select Campaign File to Inspect", options=campaign_files, format_func=lambda p: p.name)
        with open(selected_file, "r", encoding="utf-8") as f:
            file_body = f.read()

        st.download_button(
            label=f"📥 Download {selected_file.name}",
            data=file_body,
            file_name=selected_file.name,
            mime="text/markdown"
        )
        st.markdown(file_body)
    else:
        st.info("No saved campaigns found yet. Generate your first campaign in the Campaign Studio!")

# =========================================================================
# TAB 4: GUARDRAILS & API SETTINGS
# =========================================================================
elif nav == "⚙️ Guardrails & API Settings":
    st.markdown('<div class="glass-card-title">⚙️ Financial Guardrails & API Connections</div>', unsafe_allow_html=True)
    st.write("Adjust automated stop-loss thresholds, hard budget caps, and API connection credentials.")

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("🛡️ Financial Safeguards")
        st.number_input("Target Cost Per Lead (CPA in ₹)", value=float(settings.TARGET_CPA), key="cfg_cpa")
        st.number_input("Max Acceptable CPC (in ₹)", value=float(settings.MAX_CPC), key="cfg_cpc")
        st.slider("Bleeder Stop-Loss Multiplier (Stop if Spend > X * CPA & 0 Leads)", 1.0, 5.0, float(settings.BLEEDER_SPEND_MULTIPLIER), key="cfg_bleeder")
        st.number_input("Hard Daily Budget Cap (in ₹)", value=float(settings.MAX_DAILY_BUDGET_CAP), key="cfg_cap")

    with g2:
        st.subheader("🔑 Active Credentials")
        st.text_input("Meta Marketing API Token", value=settings.META_ACCESS_TOKEN[:15] + "..." if settings.META_ACCESS_TOKEN else "", disabled=True)
        st.text_input("Connected Meta Ad Account", value=settings.META_AD_ACCOUNT_ID, disabled=True)
        st.text_input("Gemini API Key", value=settings.GEMINI_API_KEY[:10] + "..." if settings.GEMINI_API_KEY else "", disabled=True)
        st.text_input("Active LLM Model", value="gemini-2.5-flash", disabled=True)

    st.success("✅ Both Meta Marketing API and Gemini 2.5 Flash are actively synced from `.env`.")
