"""
Meta Marketing API Tool: Real-Time Live Ad Account Engine
Direct Meta Graph API integration for status toggling (PAUSED/ACTIVE), budget scaling,
and live metric extraction. Zero simulated/fake data.
"""

import time
import logging
import requests
from typing import Dict, List, Any, Optional

from config import settings

logger = logging.getLogger("MetaAdsAPI")

class MetaAdsManager:
    def __init__(self, access_token: Optional[str] = None, ad_account_id: Optional[str] = None):
        self.access_token = (access_token or settings.META_ACCESS_TOKEN or "").strip()
        raw_account = (ad_account_id or settings.META_AD_ACCOUNT_ID or "").strip()
        if raw_account and not raw_account.startswith("act_"):
            self.ad_account_id = f"act_{raw_account}"
        else:
            self.ad_account_id = raw_account
            
        self.is_live = bool(self.access_token and self.ad_account_id and not self.access_token.startswith("your_"))
        self.last_error: Optional[str] = None
        self.api_version = "v20.0"

    def get_ad_metrics(self, date_preset: str = "last_30d") -> List[Dict[str, Any]]:
        """
        Fetch real-time metrics for all ads in the connected Meta Ad Account.
        Returns empty list [] if no ads or if token is expired/invalid. Zero fake data.
        """
        self.last_error = None
        if not self.is_live:
            self.last_error = "Meta API not configured. Please set META_ACCESS_TOKEN and META_AD_ACCOUNT_ID in settings."
            return []

        try:
            url = f"https://graph.facebook.com/{self.api_version}/{self.ad_account_id}/ads"
            params = {
                "fields": "id,name,status,adset_id,campaign_id,effective_status",
                "limit": 50,
                "access_token": self.access_token
            }
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()

            if "error" in data:
                err_msg = data["error"].get("message", "Unknown Meta API error")
                self.last_error = f"Meta API: {err_msg}"
                logger.error(self.last_error)
                return []

            ads = data.get("data", [])
            results = []

            for ad in ads:
                ad_id = ad.get("id")
                # Query insights for this ad
                insights_url = f"https://graph.facebook.com/{self.api_version}/{ad_id}/insights"
                ins_params = {
                    "fields": "spend,impressions,clicks,cpc,ctr,frequency,actions",
                    "date_preset": date_preset,
                    "access_token": self.access_token
                }
                
                spend = 0.0
                clicks = 0
                cpc = 0.0
                ctr = 0.0
                frequency = 1.0
                leads = 0

                try:
                    ins_resp = requests.get(insights_url, params=ins_params, timeout=10)
                    ins_data = ins_resp.json()
                    if "data" in ins_data and ins_data["data"]:
                        row = ins_data["data"][0]
                        spend = float(row.get("spend", 0.0))
                        clicks = int(row.get("clicks", 0))
                        cpc = float(row.get("cpc", 0.0))
                        ctr = float(row.get("ctr", 0.0))
                        frequency = float(row.get("frequency", 1.0))

                        for action in row.get("actions", []):
                            if action.get("action_type") in [
                                "lead", "contact", "offsite_conversion.fb_pixel_lead", "onsite_conversion.lead_grouped"
                            ]:
                                leads += int(action.get("value", 0))
                except Exception as ie:
                    logger.warning(f"Could not fetch insights for ad {ad_id}: {ie}")

                cpl = (spend / leads) if leads > 0 else 0.0

                results.append({
                    "id": ad.get("id"),
                    "ad_name": ad.get("name"),
                    "status": ad.get("status"),
                    "effective_status": ad.get("effective_status"),
                    "adset_id": ad.get("adset_id"),
                    "campaign_id": ad.get("campaign_id"),
                    "spend": spend,
                    "leads": leads,
                    "clicks": clicks,
                    "cpc": cpc,
                    "ctr": ctr,
                    "frequency": frequency,
                    "cpl": cpl,
                    "roas": 0.0
                })

            return results

        except Exception as e:
            self.last_error = f"Connection error: {str(e)}"
            logger.error(self.last_error)
            return []

    def pause_ad(self, ad_id: str) -> Dict[str, Any]:
        """Pauses a bleeding or fatigued ad via live Meta API."""
        if not self.is_live:
            return {"success": False, "error": "Meta API not configured."}

        url = f"https://graph.facebook.com/{self.api_version}/{ad_id}"
        payload = {"status": "PAUSED", "access_token": self.access_token}
        try:
            resp = requests.post(url, data=payload, timeout=15)
            data = resp.json()
            if "success" in data and data["success"]:
                return {"success": True, "mode": "live", "ad_id": ad_id, "status": "PAUSED"}
            elif "error" in data:
                return {"success": False, "error": data["error"].get("message", "Failed to pause ad")}
            return {"success": True, "mode": "live", "ad_id": ad_id, "status": "PAUSED"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def activate_ad(self, ad_id: str) -> Dict[str, Any]:
        """Activates a paused ad via live Meta API."""
        if not self.is_live:
            return {"success": False, "error": "Meta API not configured."}

        url = f"https://graph.facebook.com/{self.api_version}/{ad_id}"
        payload = {"status": "ACTIVE", "access_token": self.access_token}
        try:
            resp = requests.post(url, data=payload, timeout=15)
            data = resp.json()
            if "success" in data and data["success"]:
                return {"success": True, "mode": "live", "ad_id": ad_id, "status": "ACTIVE"}
            elif "error" in data:
                return {"success": False, "error": data["error"].get("message", "Failed to activate ad")}
            return {"success": True, "mode": "live", "ad_id": ad_id, "status": "ACTIVE"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def scale_budget(self, adset_id: str, percentage: float = 20.0) -> Dict[str, Any]:
        """Scales daily budget of winning adset incrementally (e.g. +20%)."""
        if not self.is_live:
            return {"success": False, "error": "Meta API not configured."}

        try:
            get_url = f"https://graph.facebook.com/{self.api_version}/{adset_id}"
            params = {"fields": "daily_budget,name", "access_token": self.access_token}
            r = requests.get(get_url, params=params, timeout=15).json()
            if "error" in r:
                return {"success": False, "error": r["error"].get("message")}

            current_budget = float(r.get("daily_budget", 0))
            if current_budget <= 0:
                return {"success": False, "error": "AdSet does not use daily_budget or budget is 0"}

            new_budget = current_budget * (1 + (percentage / 100.0))
            if (new_budget / 100.0) > settings.MAX_DAILY_BUDGET_CAP:
                return {
                    "success": False,
                    "error": f"Blocked by guardrail: New budget ₹{new_budget/100:.2f} exceeds cap ₹{settings.MAX_DAILY_BUDGET_CAP}"
                }

            post_url = f"https://graph.facebook.com/{self.api_version}/{adset_id}"
            update_payload = {"daily_budget": int(new_budget), "access_token": self.access_token}
            up_resp = requests.post(post_url, data=update_payload, timeout=15).json()
            if "error" in up_resp:
                return {"success": False, "error": up_resp["error"].get("message")}

            return {
                "success": True,
                "mode": "live",
                "adset_id": adset_id,
                "old_budget": current_budget,
                "new_budget": new_budget
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
