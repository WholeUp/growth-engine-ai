"""
Agent 4: Creative & Visual Art Director
Designs high-CTR visual assets, Midjourney/DALL-E image prompts, and video editing b-roll cues.
"""

from agents.base_agent import BaseAgent
from config.marketing_dna import CREATIVE_VISUAL_HEURISTICS

class CreativeDirectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Creative & Visual Art Director",
            goal="Turn copywriting into scroll-stopping visual assets that achieve 3%+ Link CTR.",
            backstory=(
                "You have tested over 10,000 ad creatives across Meta, TikTok, and YouTube. "
                "You know that 80% of ad performance comes from the visual hook and first 3 seconds. "
                "You design for mobile feeds: high contrast, native UGC vibes, no stock photo garbage."
            )
        )

    def create_visual_specs(self, niche: str, target_location: str, copy_brief: str) -> str:
        prompt = f"""
Based on the ad copy below, create the visual and production design brief:
- Niche: {niche}
- Location: {target_location}

Copy Brief Context:
{copy_brief}

Provide the following:
1. 3x Static Ad Visual Concepts (For Canva/Photoshop):
   - Layout composition (Split screen, before/after, or native screenshot style).
   - High-contrast text overlay (Max 6 words, bold font style, color palette).
   - Focal point imagery.
2. 3x AI Image Generation Prompts (Optimized for Midjourney v6 / DALL-E 3):
   - Detailed photorealistic prompts with aspect ratio (--ar 1:1 or 4:5), camera angle, lighting, and mood.
3. Video Production / B-Roll Blueprint for Reel Editors:
   - Visual pattern interrupts for the 0-3 second mark.
   - On-screen subtitle styling (Alex Hormozi style, dynamic bold words, emoji placement).
   - Sound design cues (SFX: whoosh, cash register, vinyl scratch, tension riser).

Visual Heuristics:
{chr(10).join(f"- {h}" for h in CREATIVE_VISUAL_HEURISTICS)}
"""
        return self.call_llm(prompt)
