"""
Interactive CLI for WholeUp Multi-Agent Digital Marketing & Media Buyer System
Run with: python run_cli.py
"""

import sys
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from orchestrator import AgencyOrchestrator
from tools.meta_ads_api import MetaAdsManager
from config import settings

console = Console()

def display_banner():
    console.print("""[bold cyan]
  ██████╗ ██████╗  ██████╗ ██╗    ██╗████████╗██╗  ██╗    █████╗ ██╗
 ██╔════╝ ██╔══██╗██╔═══██╗██║    ██║╚══██╔══╝██║  ██║   ██╔══██╗██║
 ██║  ███╗██████╔╝██║   ██║██║ █╗ ██║   ██║   ███████║   ███████║██║
 ██║   ██║██╔══██╗██║   ██║██║███╗██║   ██║   ██╔══██║   ██╔══██║██║
 ╚██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝   ██║   ██║  ██║██╗██║  ██║██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝    ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝
    [bold magenta]5+ YR SENIOR DIGITAL MARKETING & AUTONOMOUS MEDIA BUYER[/bold magenta]
    [/bold cyan]""")

def menu_campaign_generator(orchestrator: AgencyOrchestrator):
    console.rule("[bold cyan]CREATE NEW CAMPAIGN PACK[/bold cyan]")
    niche = Prompt.ask("[bold yellow]Client Niche / Industry[/bold yellow]", default="Surat Luxury Real Estate (3BHK & 4BHK)")
    location = Prompt.ask("[bold yellow]Target Location / City[/bold yellow]", default="Surat, Gujarat (Vesu, Pal, Adajan)")
    offer = Prompt.ask("[bold yellow]Core Offer / Hook[/bold yellow]", default="Exclusive pre-launch pricing with ₹0 EMI till possession & luxury club amenities")

    console.print("\n[cyan]Starting multi-agent execution...[/cyan]")
    bundle = orchestrator.run_full_campaign(niche, location, offer)
    console.print(f"[bold green]Campaign dossier successfully generated![/bold green] Saved at: [underline]{bundle['file_path']}[/underline]\n")

def menu_ad_optimizer(orchestrator: AgencyOrchestrator):
    console.rule("[bold red]AI MEDIA BUYER: AUTO-PILOT AD ACCOUNT OPTIMIZER[/bold red]")
    meta = MetaAdsManager()
    
    # Show current ads table
    ads = meta.get_ad_metrics()
    table = Table(title=f"Current Ads Status ({'Live Meta API' if meta.is_live else 'Sandbox / Simulation Mode'})")
    table.add_column("Ad ID", style="dim")
    table.add_column("Ad Name", style="bold")
    table.add_column("Status")
    table.add_column("Spend (₹)", justify="right")
    table.add_column("Leads", justify="right")
    table.add_column("CPC (₹)", justify="right")
    table.add_column("Freq", justify="right")
    table.add_column("ROAS", justify="right")

    for ad in ads:
        status_style = "green" if ad["status"] == "ACTIVE" else "red"
        table.add_row(
            ad["id"],
            ad["ad_name"],
            f"[{status_style}]{ad['status']}[/{status_style}]",
            f"₹{ad['spend']:.2f}",
            str(ad["leads"]),
            f"₹{ad['cpc']:.2f}",
            f"{ad['frequency']:.2f}",
            f"{ad['roas']:.1f}x"
        )
    console.print(table)

    is_dry_run = Confirm.ask("\nRun in [bold]Dry Run / Simulation Mode[/bold] first (no changes made)?", default=True)
    results = orchestrator.run_ad_autopilot(dry_run=is_dry_run)
    
    console.print(f"\n[bold green]Scan Complete:[/bold green] {results['actions_count']} rule triggers processed.")

def main():
    orchestrator = AgencyOrchestrator()
    while True:
        display_banner()
        console.print("[1] [bold cyan]Launch 5-Agent Campaign Generator[/bold cyan] (Research + SEO + Copy + Visuals + CMO Audit)")
        console.print("[2] [bold red]Run Autonomous AI Media Buyer[/bold red] (Kill Bleeders + Scale Winners + Alerts)")
        console.print("[3] [bold yellow]Inspect Live / Simulated Ad Account Metrics[/bold yellow]")
        console.print("[4] [bold white]Exit[/bold white]")

        choice = Prompt.ask("\n[bold]Select an action[/bold]", choices=["1", "2", "3", "4"], default="1")
        if choice == "1":
            menu_campaign_generator(orchestrator)
        elif choice == "2":
            menu_ad_optimizer(orchestrator)
        elif choice == "3":
            menu_ad_optimizer(orchestrator)
        elif choice == "4":
            console.print("[yellow]Exiting Growth Matrix AI. Happy scaling![/yellow]")
            sys.exit(0)

        Prompt.ask("\nPress [bold]Enter[/bold] to return to main menu...")

if __name__ == "__main__":
    main()
