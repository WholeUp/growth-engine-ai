"""
Agent 1: Psychological Avatar & Market Intelligence Researcher
Uncovers customer pain points, secret desires, skepticism, and competitor gaps.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.web_research import search_market_intel
from config.marketing_dna import ANTI_FLUFF_RULES

class AvatarResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Psychological Avatar & Market Intelligence Researcher",
            goal="Dissect the exact target customer persona, secret fears, objections, and competitor gaps.",
            backstory=(
                "You have spent 7+ years researching buyer psychology for 7-figure digital marketing campaigns. "
                "You reject generic demographics ('30-50 yr old males'). Instead, you find the emotional trigger "
                "that keeps the prospect awake at 2:00 AM, the exact objections they will throw at sales reps, "
                "and how competitors are failing to address them."
            )
        )

    def analyze_market(self, niche: str, target_location: str, offer_description: str) -> str:
        # Step 1: Live web search for competitor signals
        search_query = f"{niche} {target_location} reviews complaints competitor marketing"
        intel_results = search_market_intel(search_query, max_results=3)
        
        intel_context = "\n".join([f"- {r['title']}: {r['snippet']}" for r in intel_results])

        prompt = f"""
Analyze the target audience and market landscape for:
- Niche / Industry: {niche}
- Target Location / Geo: {target_location}
- Offer / Core Service: {offer_description}

Web Intelligence Signals:
{intel_context}

Framework Instructions:
1. Identify the 'Nightmare at 2:00 AM' (The deepest unspoken fear or frustration).
2. Cost of Inaction (What happens in 6 months if they do nothing?).
3. Top 3 Brutal Objections (Why they will be skeptical of this offer).
4. Competitor Weakness / Angle of Attack (Where existing ads are lazy, dishonest, or boring).
5. Dream Outcome (The status elevation or financial relief they secretly crave).

Anti-Fluff Rules:
{chr(10).join(f"- {rule}" for rule in ANTI_FLUFF_RULES)}

Provide a sharp, bulleted executive research dossier.
"""
        return self.call_llm(prompt)
