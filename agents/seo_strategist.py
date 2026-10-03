"""
Agent 2: Senior SEO & Search Intent Architect
Finds high-converting transactional keywords, local SEO ranking pillars, and negative keywords.
"""

from agents.base_agent import BaseAgent
from config.marketing_dna import ANTI_FLUFF_RULES

class SEOStrategistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Senior SEO & Search Intent Architect",
            goal="Identify high-intent, money-making search queries, local SEO dominators, and negative keywords.",
            backstory=(
                "You have ranked 100+ local and global businesses at the top of Google. "
                "You care zero about vanity search volume and 100% about buyer intent. "
                "You know how to eliminate wasted budget by building rigorous negative keyword lists "
                "and how to capture local map pack rankings."
            )
        )

    def formulate_strategy(self, niche: str, target_location: str, offer_description: str, research_dossier: str) -> str:
        prompt = f"""
Using the audience research below, build the SEO & Paid Search Intent Strategy:
- Niche: {niche}
- Location: {target_location}
- Offer: {offer_description}

Audience Research Context:
{research_dossier}

Generate the following:
1. High-Intent Commercial Keywords (Top 8 queries people type when they have their credit card or checkbook ready).
2. Local SEO Long-Tail Queries (Location-specific queries with area names, nearby landmarks, and intent modifiers).
3. Negative Keywords List (Queries to exclude immediately to avoid wasting ad budget on freebie-seekers, DIY learners, or students).
4. Local Map Pack / GBP Optimization Trigger (What specific categories, service mentions, and geo-tagged reviews are needed to rank #1).

Output format: Clean, structured markdown with tables or bulleted lists.
"""
        return self.call_llm(prompt)
