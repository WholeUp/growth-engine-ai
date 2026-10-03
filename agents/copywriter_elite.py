"""
Agent 3: Elite Direct-Response Copywriter
Crafts high-converting Meta Ads, viral Reel scripts, and irresistible offers.
"""

from agents.base_agent import BaseAgent
from config.marketing_dna import DIRECT_RESPONSE_FRAMEWORKS, ANTI_FLUFF_RULES

class CopywriterEliteAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Elite Direct-Response Copywriter",
            goal="Write ad copy and video scripts that stop the thumb scroll, build emotional tension, and drive conversions.",
            backstory=(
                "You have generated tens of crores in revenue through direct response ads on Meta, Google, and YouTube. "
                "You study Dan Kennedy, Eugene Schwartz, Alex Hormozi, and modern viral creators. "
                "You never write boring brochure copy. Every hook is a punch in the gut, every line forces the next line to be read, "
                "and every CTA feels like a no-brainer opportunity."
            )
        )

    def write_campaign_copy(self, niche: str, target_location: str, offer_description: str, research_dossier: str) -> str:
        prompt = f"""
Using the audience insights below, write a complete multi-angle advertising campaign:
- Niche: {niche}
- Location: {target_location}
- Offer: {offer_description}

Audience Research Context:
{research_dossier}

Deliverable 1: 3x High-Converting Meta/Instagram Ad Variations
- **Ad 1 (The Polarizing Pattern Interrupt - AIDA)**: Start with an unexpected question or contrarian statement. Break common industry myths.
- **Ad 2 (The Hidden Pain Agitation - PAS)**: Dig into the financial or emotional bleed of staying stuck. Introduce the unique mechanism.
- **Ad 3 (The Social Proof / Case Study - HSO)**: Story-driven hook with specific numbers, client transformation, and risk reversal.

Each Ad must include:
* Primary Text (Formatted with short, punchy 1-2 sentence paragraphs for mobile screens)
* Headline (Max 5-7 words, high impact)
* News Feed Link Description (1 sentence trust booster)
* Recommended CTA Button (e.g., 'Send WhatsApp Message', 'Book Now', 'Learn More')

Deliverable 2: 5x Viral Short-Form Reel / Shorts Scripts
For each reel:
* Hook (0-3 sec): Exact dialogue + on-screen visual action/prop
* Agitation / Story (3-15 sec): Why normal methods fail
* The Solution / Value (15-45 sec): The actionable takeaway or showcase
* Call to Action (45-60 sec): Single specific instruction (e.g., 'DM "SURAT" to get the brochure')

Anti-Fluff Rules strictly enforced:
{chr(10).join(f"- {rule}" for rule in ANTI_FLUFF_RULES)}
"""
        return self.call_llm(prompt)
