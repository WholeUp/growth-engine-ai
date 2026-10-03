"""
Algorithmic Dayparting & Pacing Engine
Optimizes ad spend to match Surat business owner active hours.
Prevents budget waste during dead night hours and concentrates spend during peak buying windows.
"""

from datetime import datetime
from typing import Dict, Any

class DaypartingEngine:
    # Defined for Indian Local Business Owners (Surat, Gujarat)
    PEAK_WINDOWS = [
        (11, 14),  # 11:00 AM - 2:00 PM: Afternoon store opening & tea break
        (19, 23)   # 7:00 PM - 11:00 PM: Evening shop closing & relaxed phone browsing
    ]
    OFF_PEAK_WINDOWS = [
        (8, 11),   # 8:00 AM - 11:00 AM: Commute & morning rush
        (14, 19)   # 2:00 PM - 7:00 PM: Peak store rush / inventory work
    ]
    DEAD_WINDOWS = [
        (0, 8)     # 12:00 AM - 8:00 AM: Sleeping hours (Zero business owner form submissions)
    ]

    @classmethod
    def get_current_pacing(cls) -> Dict[str, Any]:
        """Analyzes current hour and recommends optimal ad spend multiplier."""
        now = datetime.now()
        current_hour = now.hour

        # Check Dead Hours
        for start, end in cls.DEAD_WINDOWS:
            if start <= current_hour < end:
                return {
                    "phase": "DEAD_HOURS",
                    "status": "SLEEP / MINIMAL",
                    "budget_multiplier": 0.4,
                    "reason": "Midnight / early morning. Low buying intent. Save budget.",
                    "hour": current_hour
                }

        # Check Peak Hours
        for start, end in cls.PEAK_WINDOWS:
            if start <= current_hour < end:
                return {
                    "phase": "PEAK_BUYING_HOURS",
                    "status": "AGGRESSIVE BOOST",
                    "budget_multiplier": 1.4,
                    "reason": "Business owners actively on Instagram. High conversion window.",
                    "hour": current_hour
                }

        # Default Off-Peak
        return {
            "phase": "NORMAL_PACING",
            "status": "STEADY",
            "budget_multiplier": 1.0,
            "reason": "Standard business hours. Maintain default daily pacing.",
            "hour": current_hour
        }
