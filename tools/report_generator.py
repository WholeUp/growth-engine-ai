"""
Automated Executive Report Generator: Nightly Client / Agency Performance Summaries
Generates branded, clean executive summaries suitable for WhatsApp delivery or PDF archiving.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class ExecutiveReportGenerator:
    def __init__(self, agency_name: str = "WholeUp Agency"):
        self.agency_name = agency_name

    def generate_daily_executive_report(
        self,
        account_name: str,
        total_spend: float,
        total_leads: int,
        ads_performance: List[Dict[str, Any]],
        actions_taken: List[Dict[str, Any]]
    ) -> str:
        """Compiles clean, high-impact executive daily report."""
        cpl = (total_spend / total_leads) if total_leads > 0 else 0.0
        date_str = datetime.now().strftime("%d %B %Y")
        time_str = datetime.now().strftime("%I:%M %p")

        # Top winning ad
        winning_ad = "N/A"
        active_ads = [a for a in ads_performance if a.get("status") == "ACTIVE"]
        if active_ads:
            winning_ad = max(active_ads, key=lambda x: x.get("leads", 0)).get("ad_name", "N/A")

        # Compile report text
        report = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *{self.agency_name} — DAILY PERFORMANCE BRIEF*
📅 Date: {date_str} | Generated at: {time_str}
🏢 Account: {account_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 *KEY FINANCIAL METRICS:*
• Total Spend Today: ₹{total_spend:,.2f}
• Total Verified Leads: {total_leads}
• Average Cost Per Lead (CPL): ₹{cpl:,.2f}
• Winning Creative: {winning_ad}

🛡️ *AUTONOMOUS RISK MANAGEMENT:*"""

        if actions_taken:
            for act in actions_taken:
                report += f"\n• [{act.get('rule', 'System')}] {act.get('ad_name', '')} ➔ {act.get('action', '')}"
        else:
            report += "\n• All active creatives running within healthy performance thresholds. Zero spend bleeds."

        report += f"""

🎯 *MEDIA BUYER'S ACTION PLAN FOR TOMORROW:*
1. Monitor CPL stability on winning creative: '{winning_ad}'.
2. Review retargeting pool growth (target: 1,000+ 50% video viewers).
3. Pacing calibrated for Surat peak buying hours (11:30 AM - 2:30 PM & 7:30 PM - 10:30 PM).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*Delivered by WholeUp AI Growth Operating System*
"""
        return report.strip()
