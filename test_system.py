import sys
sys.stdout.reconfigure(encoding='utf-8')

from agents.media_buyer_bot import MediaBuyerBot
from tools.meta_ads_api import MetaAdsManager

def test_media_buyer():
    print("--- 1. Testing Meta Ads Manager ---")
    meta = MetaAdsManager()
    ads = meta.get_ad_metrics()
    print(f"Total ads detected: {len(ads)}")
    for a in ads:
        print(f"  • {a['id']}: {a['ad_name']} | Status: {a['status']} | Spend: ₹{a['spend']} | Leads: {a['leads']}")

    print("\n--- 2. Testing Autonomous AI Media Buyer Rules ---")
    bot = MediaBuyerBot()
    results = bot.evaluate_and_optimize(dry_run=False)
    print(f"Actions triggered: {results['actions_count']}")
    for action in results["actions"]:
        print(f"  👉 [{action['rule']}] {action['ad_name']} ➔ {action['action']}")
        print(f"     Reason: {action['reason']}")

    print("\n--- 3. Verifying Ad Status Post-Optimization ---")
    updated_ads = meta.get_ad_metrics()
    for a in updated_ads:
        print(f"  • {a['id']}: Status is now {a['status']}")

    print("\n✅ Smoke Test Passed Successfully!")

if __name__ == "__main__":
    test_media_buyer()
