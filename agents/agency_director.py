"""
Agent 5: Agency Director & Chief Marketing Officer (CMO)
The final gatekeeper. Audits tone, deletes remaining AI fluff, ensures Meta ad policy compliance,
and rates the entire campaign on conversion readiness.
"""

from agents.base_agent import BaseAgent
from config.marketing_dna import ANTI_FLUFF_RULES

class AgencyDirectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Agency Director & Chief Marketing Officer (CMO)",
            goal="Ensure ruthless quality control, zero fluff, Meta policy compliance, and high conversion probability.",
            backstory=(
                "You have scaled marketing agencies to 8 figures. You have fired copywriters for writing "
                "generic corporate garbage. You review every asset before a single rupee or dollar of client ad spend is deployed. "
                "If an ad won't make money on Day 1, you send it back or rewrite the hook yourself."
            )
        )

    def review_and_finalize(self, niche: str, target_location: str, campaign_bundle: dict) -> str:
        prompt = f"""
Perform a ruthless Senior CMO Audit on this complete campaign package:
Niche: {niche}
Location: {target_location}

Campaign Package Draft:
---
[RESEARCH DOSSIER]
{campaign_bundle.get('research', '')}

[SEO & SEARCH STRATEGY]
{campaign_bundle.get('seo', '')}

[COPYWRITING (ADS & REELS)]
{campaign_bundle.get('copy', '')}

[VISUAL & PRODUCTION BLUEPRINT]
{campaign_bundle.get('visuals', '')}
---

Your Review Protocol:
1. Fluff & Cliche Audit: Identify any weak, generic AI phrases and give their punchy replacement.
2. Meta Ad Policy Compliance Check: Ensure no prohibited claims (guaranteed returns, misleading claims, personal attribute violations).
3. Hook Strength Rating (1-10) for each of the 3 Meta Ads and 5 Reels.
4. Executive Sign-Off & Launch Checklist: 3 critical action items for the media buyer before turning campaigns live.

Deliver your review with authority, high-conviction advice, and senior agency polish.
"""
        return self.call_llm(prompt)
