"""
Agent 6: Autonomous AI Media Buyer & Ad Optimizer
Monitors Meta/Google ads 24/7. Executes Kill/Scale rules, pauses bleeding ads,
scales profitable winners, and dispatches real-time alerts.
"""

import logging
from typing import Dict, List, Any
from tools.meta_ads_api import MetaAdsManager
from tools.notification_hub import NotificationHub
from config import settings

logger = logging.getLogger("MediaBuyerBot")

class MediaBuyerBot:
    def __init__(self, target_cpa: float = None, max_cpc: float = None):
        self.meta_ads = MetaAdsManager()
        self.notifier = NotificationHub()
        self.target_cpa = target_cpa or settings.TARGET_CPA
        self.max_cpc = max_cpc or settings.MAX_CPC
        self.bleeder_threshold = self.target_cpa * settings.BLEEDER_SPEND_MULTIPLIER

    def evaluate_and_optimize(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Scans all ads in the account, evaluates rules, and takes automated action.
        If dry_run=True, it detects issues and creates recommendations without executing changes.
        """
        ads = self.meta_ads.get_ad_metrics()
        actions_taken = []
        
        logger.info(f"Scanning {len(ads)} ads against Senior Media Buyer rules...")

        for ad in ads:
            ad_id = ad.get("id")
            ad_name = ad.get("ad_name", "Unknown Ad")
            status = ad.get("status")
            spend = float(ad.get("spend", 0.0))
            leads = int(ad.get("leads", 0))
            cpc = float(ad.get("cpc", 0.0))
            frequency = float(ad.get("frequency", 1.0))
            roas = float(ad.get("roas", 0.0))
            adset_id = ad.get("adset_id", "")

            # Skip already paused ads unless reviving
            if status != "ACTIVE":
                continue

            # ---------------------------------------------------------
            # RULE 1: KILL BLEEDER (0 Leads, High Spend)
            # ---------------------------------------------------------
            if leads == 0 and spend >= self.bleeder_threshold:
                reason = f"Bleeder Alert: Spent ₹{spend:.2f} (>{self.bleeder_threshold:.2f}) with 0 leads."
                action_desc = "PAUSE AD"
                if not dry_run:
                    result = self.meta_ads.pause_ad(ad_id)
                    status_applied = result.get("status", "PAUSED")
                else:
                    status_applied = "RECOMMEND PAUSE (DRY RUN)"

                self.notifier.send_alert(
                    title=f"🛑 PAUSED BLEEDER AD: {ad_name}",
                    message=f"Killed ad {ad_id} to prevent ad spend burn.\n{reason}",
                    level="danger",
                    details={"Spend": f"₹{spend}", "Leads": leads, "Action": status_applied}
                )
                actions_taken.append({
                    "ad_id": ad_id,
                    "ad_name": ad_name,
                    "rule": "Kill Bleeder",
                    "action": status_applied,
                    "reason": reason
                })
                continue

            # ---------------------------------------------------------
            # RULE 2: HIGH CPC CUTOFF (Spiking click cost)
            # ---------------------------------------------------------
            if cpc > (self.max_cpc * 1.5) and spend >= self.target_cpa:
                reason = f"High CPC Spike: CPC at ₹{cpc:.2f} exceeds max threshold ₹{self.max_cpc:.2f}."
                if not dry_run:
                    self.meta_ads.pause_ad(ad_id)
                    status_applied = "PAUSED"
                else:
                    status_applied = "RECOMMEND PAUSE (DRY RUN)"

                self.notifier.send_alert(
                    title=f"⚠️ PAUSED HIGH CPC AD: {ad_name}",
                    message=f"Ad stopped due to expensive traffic.\n{reason}",
                    level="warning",
                    details={"CPC": f"₹{cpc}", "Spend": f"₹{spend}", "Action": status_applied}
                )
                actions_taken.append({
                    "ad_id": ad_id,
                    "ad_name": ad_name,
                    "rule": "High CPC Cutoff",
                    "action": status_applied,
                    "reason": reason
                })
                continue

            # ---------------------------------------------------------
            # RULE 3: CREATIVE FATIGUE DETECTION
            # ---------------------------------------------------------
            if frequency >= settings.FATIGUE_FREQUENCY:
                reason = f"Audience Saturation: Frequency reached {frequency:.2f} (Threshold: {settings.FATIGUE_FREQUENCY})."
                self.notifier.send_alert(
                    title=f"🔄 CREATIVE FATIGUE DETECTED: {ad_name}",
                    message=f"Same audience is seeing this ad repeatedly. Recommended action: Rotate new creative hook.\n{reason}",
                    level="warning",
                    details={"Frequency": frequency, "Spend": f"₹{spend}"}
                )
                actions_taken.append({
                    "ad_id": ad_id,
                    "ad_name": ad_name,
                    "rule": "Creative Fatigue",
                    "action": "FLAGGED FOR ROTATION",
                    "reason": reason
                })

            # ---------------------------------------------------------
            # RULE 4: SCALE WINNING ADS (+20% Budget)
            # ---------------------------------------------------------
            is_winning_roas = roas >= settings.WINNER_ROAS
            is_cheap_cpl = (leads >= 5 and (spend / leads) <= (self.target_cpa * 0.75))
            
            if (is_winning_roas or is_cheap_cpl) and frequency < 2.0:
                reason = f"Elite Performance: ROAS {roas:.2f} / CPL ₹{(spend/leads):.2f}. Frequency is healthy ({frequency:.2f})."
                if not dry_run and adset_id:
                    scale_result = self.meta_ads.scale_budget(adset_id, percentage=20.0)
                    action_applied = f"BUDGET SCALED +20% ({scale_result.get('mode', '')})"
                else:
                    action_applied = "RECOMMEND SCALE +20% (DRY RUN)"

                self.notifier.send_alert(
                    title=f"🚀 SCALED WINNER: {ad_name}",
                    message=f"Automated budget scaling triggered.\n{reason}",
                    level="success",
                    details={"ROAS": roas, "Leads": leads, "Action": action_applied}
                )
                actions_taken.append({
                    "ad_id": ad_id,
                    "ad_name": ad_name,
                    "rule": "Scale Winner",
                    "action": action_applied,
                    "reason": reason
                })

        return {
            "total_ads_scanned": len(ads),
            "actions_count": len(actions_taken),
            "actions": actions_taken,
            "mode": "Live Meta API" if self.meta_ads.is_live else "Meta Account Not Connected"
        }
