"""
Autonomous Market & Competitor Recon Agent
Takes any website URL or business name, crawls the entity, autonomously discovers top competitors,
analyzes live market trends and ads, and formulates an actionable 360-degree market dossier.
"""

import re
import logging
import requests
from typing import Dict, Any, Optional

from agents.base_agent import BaseAgent
from tools.web_research import search_market_intel

logger = logging.getLogger("MarketReconAgent")

class AutonomousMarketReconAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Chief Intelligence Officer & Senior Market Recon Strategist",
            goal="Conduct 360-degree autonomous market and competitor reconnaissance on any website or brand.",
            backstory="You have audited thousands of businesses and competitor campaigns. You immediately spot profit leaks, competitor weaknesses, and winning attack angles."
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _extract_website_content(self, target: str) -> Dict[str, Any]:
        """Crawls a website URL or handles raw brand name."""
        target = target.strip()
        if not target.startswith("http://") and not target.startswith("https://") and ("." in target and not " " in target):
            target = f"https://{target}"

        if target.startswith("http://") or target.startswith("https://"):
            try:
                resp = requests.get(target, headers=self.headers, timeout=12)
                html = resp.text

                # Extract title
                title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else ""

                # Extract meta description
                meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
                meta_desc = meta_match.group(1).strip() if meta_match else ""

                # Clean text
                clean = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
                clean = re.sub(r'<style[^>]*>.*?</style>', ' ', clean, flags=re.DOTALL | re.IGNORECASE)
                clean = re.sub(r'<[^>]+>', ' ', clean)
                text = ' '.join(clean.split())[:3500]

                return {
                    "is_url": True,
                    "url": target,
                    "title": title,
                    "meta_description": meta_desc,
                    "body_snippet": text,
                    "success": True
                }
            except Exception as e:
                logger.warning(f"Failed to crawl URL {target}: {e}. Treating as entity query.")
                return {
                    "is_url": True,
                    "url": target,
                    "title": target,
                    "meta_description": "",
                    "body_snippet": f"Could not crawl directly ({str(e)}). Running deep web search recon.",
                    "success": False
                }
        else:
            return {
                "is_url": False,
                "url": target,
                "title": target,
                "meta_description": "",
                "body_snippet": f"Target entity name: {target}",
                "success": True
            }

    def analyze_market_360(self, target_input: str, location_hint: str = "") -> Dict[str, Any]:
        """
        Main Autonomous Recon Pipeline:
        1. Crawls website / input entity
        2. Discovers real competitors in market
        3. Scrapes active marketing campaigns & trends
        4. Synthesizes 360-degree competitive intelligence via LLM
        """
        # Step 1: Extract site data
        site_info = self._extract_website_content(target_input)

        # Step 2: Live Search for Market & Competitors
        query_base = f"{site_info.get('title', target_input)} {location_hint}".strip()
        search_competitors = search_market_intel(f"{query_base} top competitors active marketing ads", max_results=4)
        search_trends = search_market_intel(f"{query_base} customer reviews complaints offers", max_results=4)

        comp_text = "\n".join([f"- {r.get('title')}: {r.get('snippet')} ({r.get('url')})" for r in search_competitors])
        trends_text = "\n".join([f"- {r.get('title')}: {r.get('snippet')}" for r in search_trends])

        prompt = f"""
You are the Chief Intelligence Officer & Senior Market Recon Strategist at WholeUp Agency.
A user has submitted the following target entity/website to conduct a 360-degree Autonomous Market & Competitor Recon.

### Target Entity Submitted:
- Input: {target_input}
- Title / Meta: {site_info.get('title', '')} | {site_info.get('meta_description', '')}
- Location Focus: {location_hint or 'Auto-Detect from context (Surat/Gujarat/India)'}
- Website Content Sample:
\"\"\"
{site_info.get('body_snippet', '')}
\"\"\"

### Live Market & Competitor Intel Found via Search:
- Competitor Data:
{comp_text}
- Customer Trends & Market Sentiment:
{trends_text}

---

### YOUR MISSION:
Generate an uncompromising, direct, high-value 360-Degree Market & Competitor Recon Dossier.
Do NOT give generic marketing fluff or textbook definitions. Give sharp, actionable business truth.

Format your response cleanly in GitHub Markdown using these exact 5 sections:

## 1. 🔍 Target Brand X-Ray (Current State)
- What this brand actually does and sells.
- Core Positioning & Price Perception.
- The 2-3 Glaring "Profit Leaks" (Where they are losing customers right now: bad hook, weak offer, missing trust signals, poor CTA).

## 2. 🌐 Live Market Landscape (Kya Chal Raha Hai Market Mein)
- Current market demand and customer mindset in this niche.
- Price benchmarks (What people are actually paying right now).
- What hot trends are driving sales in this industry.

## 3. 🕵️ Competitor Recon Matrix (Kaun-Kaun Kya Kar Raha Hai)
Detail at least 3 active competitors operating in this space:
- **Competitor Name & Angle**: What they claim.
- **Their Active Ad Strategy**: What hooks/offers they are using to get attention.
- **Their Fatal Weakness**: Where they fail (bad customer service, high prices, boring creatives, no risk-reversal).

## 4. ⚡ Exploitable Market Gaps (Kahan Mauka Hai)
- What every competitor is doing WRONG or ignoring.
- The exact customer pain point that nobody is solving properly.
- The Blue Ocean angle that will make this brand stand out immediately.

## 5. 🎯 WholeUp Winning Attack Playbook
- **1x No-Brainer Irresistible Offer**: The exact offer to launch that makes competitors look stupid.
- **3x Scroll-Stopping Meta Reel / Ad Hooks**: Specific 0-3 second hooks that will steal competitor attention.
- **WhatsApp Pitch Message (Client Closing Script)**: A punchy, respectful 4-line WhatsApp message that the agency founder can send directly to this business owner to close a ₹30,000 - ₹50,000 retainer!
"""

        dossier = self.call_llm(prompt)

        return {
            "target": target_input,
            "site_info": site_info,
            "competitor_sources": len(search_competitors),
            "trends_sources": len(search_trends),
            "dossier": dossier
        }
