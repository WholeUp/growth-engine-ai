"""
Meta Marketing API Tool: Live & High-Fidelity Simulation Engine
Handles live status toggling (PAUSED/ACTIVE), budget scaling, and real-time metric extraction.
"""

import time
import logging
from typing import Dict, List, Any, Optional

from config import settings

logger = logging.getLogger("MetaAdsAPI")

# Realistic Mock Data for Immediate Testing / Simulation
DEFAULT_MOCK_ADS = [
    {
        "id": "ad_101_vesu_realty",
        "adset_id": "adset_vesu_3bhk",
        "campaign_name": "Surat Luxury Real Estate - Vesu",
        "ad_name": "Ad #1 - Video Hook (EMI vs Rent)",
        "status": "ACTIVE",
        "spend": 1850.0,
        "leads": 22,
        "clicks": 340,
        "cpc": 5.44,
        "ctr": 2.85,
        "frequency": 1.45,
        "cpl": 84.09,
        "roas": 4.2
    },
    {
        "id": "ad_102_bleeder_ad",
        "adset_id": "adset_vesu_3bhk",
        "campaign_name": "Surat Luxury Real Estate - Vesu",
        "ad_name": "Ad #2 - Static Poster (Cluttered Text)",
        "status": "ACTIVE",
        "spend": 820.0,
        "leads": 0,
        "clicks": 45,
        "cpc": 18.22,
        "ctr": 0.65,
        "frequency": 1.20,
        "cpl": 0.0,  # 0 leads, spent 820 -> Bleeder!
        "roas": 0.0
    },
    {
        "id": "ad_103_fatigued_winner",
        "adset_id": "adset_pal_villas",
        "campaign_name": "Pal Bhatha Commercial Showrooms",
        "ad_name": "Ad #3 - Founder Story Hook",
        "status": "ACTIVE",
        "spend": 4500.0,
        "leads": 35,
        "clicks": 620,
        "cpc": 7.25,
        "ctr": 1.15,
        "frequency": 3.85,  # High frequency -> Creative Fatigue!
        "cpl": 128.57,
        "roas": 2.1
    }
]

# Shared In-memory storage for mock simulation
_SHARED_MOCK_ADS = [dict(a) for a in DEFAULT_MOCK_ADS]

class MetaAdsManager:
    def __init__(self, access_token: Optional[str] = None, ad_account_id: Optional[str] = None):
        self.access_token = access_token or settings.META_ACCESS_TOKEN
        self.ad_account_id = ad_account_id or settings.META_AD_ACCOUNT_ID
        self.is_live = bool(self.access_token and self.ad_account_id and not self.access_token.startswith("your_"))
        
        self.mock_ads = _SHARED_MOCK_ADS

        if self.is_live:
            try:
                from facebook_business.api import FacebookAdsApi
                FacebookAdsApi.init(access_token=self.access_token)
                logger.info(f"Connected to LIVE Meta Marketing API (Ad Account: {self.ad_account_id})")
            except Exception as e:
                logger.error(f"Failed to initialize FacebookAdsApi: {e}. Falling back to simulation.")
                self.is_live = False
        else:
            logger.info("Operating in SIMULATION / SANDBOX mode (Mock Meta Ad Account)")

    def get_ad_metrics(self) -> List[Dict[str, Any]]:
        """Fetch real-time metrics for all active ads in account."""
        if not self.is_live:
            return self.mock_ads

        # Live Meta API Query
        try:
            from facebook_business.adobjects.adaccount import AdAccount
            account = AdAccount(f"act_{self.ad_account_id.replace('act_', '')}")
            fields = ['id', 'name', 'status', 'adset_id', 'campaign_id']
            ads = account.get_ads(fields=fields)
            
            results = []
            for ad in ads:
                insights = ad.get_insights(fields=[
                    'spend', 'impressions', 'clicks', 'cpc', 'ctr', 'frequency', 'actions'
                ], params={'date_preset': 'today'})
                
                spend = 0.0
                clicks = 0
                cpc = 0.0
                ctr = 0.0
                frequency = 1.0
                leads = 0
                
                if insights:
                    row = insights[0]
                    spend = float(row.get('spend', 0.0))
                    clicks = int(row.get('clicks', 0))
                    cpc = float(row.get('cpc', 0.0))
                    ctr = float(row.get('ctr', 0.0))
                    frequency = float(row.get('frequency', 1.0))
                    
                    # Extract leads from actions
                    for action in row.get('actions', []):
                        if action.get('action_type') in ['lead', 'contact', 'offsite_conversion.fb_pixel_lead']:
                            leads += int(action.get('value', 0))
                
                cpl = (spend / leads) if leads > 0 else 0.0

                results.append({
                    "id": ad.get('id'),
                    "ad_name": ad.get('name'),
                    "status": ad.get('status'),
                    "adset_id": ad.get('adset_id'),
                    "spend": spend,
                    "leads": leads,
                    "clicks": clicks,
                    "cpc": cpc,
                    "ctr": ctr,
                    "frequency": frequency,
                    "cpl": cpl,
                    "roas": 0.0  # Calculate if purchase value is available
                })
            return results
        except Exception as e:
            logger.error(f"Live Meta API error fetching ads: {e}. Returning simulation data.")
            return self.mock_ads

    def pause_ad(self, ad_id: str) -> Dict[str, Any]:
        """Pauses a bleeding or fatigued ad."""
        if not self.is_live:
            for ad in self.mock_ads:
                if ad["id"] == ad_id:
                    ad["status"] = "PAUSED"
                    return {"success": True, "mode": "simulation", "ad_id": ad_id, "status": "PAUSED"}
            return {"success": False, "error": f"Ad {ad_id} not found"}

        try:
            from facebook_business.adobjects.ad import Ad
            ad = Ad(ad_id)
            ad.api_update(params={'status': 'PAUSED'})
            return {"success": True, "mode": "live", "ad_id": ad_id, "status": "PAUSED"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def activate_ad(self, ad_id: str) -> Dict[str, Any]:
        """Activates a paused ad."""
        if not self.is_live:
            for ad in self.mock_ads:
                if ad["id"] == ad_id:
                    ad["status"] = "ACTIVE"
                    return {"success": True, "mode": "simulation", "ad_id": ad_id, "status": "ACTIVE"}
            return {"success": False, "error": f"Ad {ad_id} not found"}

        try:
            from facebook_business.adobjects.ad import Ad
            ad = Ad(ad_id)
            ad.api_update(params={'status': 'ACTIVE'})
            return {"success": True, "mode": "live", "ad_id": ad_id, "status": "ACTIVE"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def scale_budget(self, adset_id: str, percentage: float = 20.0) -> Dict[str, Any]:
        """Scales daily budget of winning adset incrementally (e.g. +20%)."""
        if not self.is_live:
            return {
                "success": True,
                "mode": "simulation",
                "adset_id": adset_id,
                "action": f"Budget increased by {percentage}%"
            }

        try:
            from facebook_business.adobjects.adset import AdSet
            adset = AdSet(adset_id)
            current_info = adset.api_get(fields=['daily_budget'])
            current_budget = float(current_info.get('daily_budget', 0))
            
            # Note: Meta uses cents/paise for currency (e.g. 50000 = ₹500)
            new_budget = current_budget * (1 + (percentage / 100.0))
            
            # Guardrail check against MAX_DAILY_BUDGET_CAP
            if (new_budget / 100.0) > settings.MAX_DAILY_BUDGET_CAP:
                return {
                    "success": False,
                    "error": f"Blocked: New budget ₹{new_budget/100:.2f} exceeds hard cap of ₹{settings.MAX_DAILY_BUDGET_CAP}"
                }

            adset.api_update(params={'daily_budget': int(new_budget)})
            return {
                "success": True,
                "mode": "live",
                "adset_id": adset_id,
                "old_budget": current_budget,
                "new_budget": new_budget
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
