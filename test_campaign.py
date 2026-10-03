import sys
sys.stdout.reconfigure(encoding='utf-8')

from orchestrator import AgencyOrchestrator

def test_campaign_flow():
    print("Testing 5-Agent Campaign Pipeline...")
    orchestrator = AgencyOrchestrator()
    bundle = orchestrator.run_full_campaign(
        niche="Surat Luxury Real Estate (3BHK & 4BHK)",
        location="Surat, Gujarat (Vesu, Pal, Adajan)",
        offer="₹0 EMI till possession + Free 3-year luxury club membership"
    )
    print("\n✅ Campaign Pipeline Completed!")
    print(f"Master file saved at: {bundle['file_path']}")

if __name__ == "__main__":
    test_campaign_flow()
