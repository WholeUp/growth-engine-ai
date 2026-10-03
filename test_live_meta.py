import sys
sys.stdout.reconfigure(encoding='utf-8')

from tools.meta_ads_api import MetaAdsManager

def test_live():
    print("Connecting to Meta Marketing API...")
    meta = MetaAdsManager()
    print("Is Live Mode:", meta.is_live)
    print("Ad Account ID:", meta.ad_account_id)

    ads = meta.get_ad_metrics()
    print(f"\nTotal Ads in Account: {len(ads)}")
    for a in ads:
        print(f"  • [{a['status']}] {a['ad_name']} (ID: {a['id']})")
        print(f"    Spend: ₹{a['spend']:.2f} | Clicks: {a['clicks']} | CPC: ₹{a['cpc']:.2f} | Leads: {a['leads']}")

if __name__ == "__main__":
    test_live()
