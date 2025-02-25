import requests
import os
import time
import re
import sys
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from shutil import get_terminal_size

console = Console()

# ✅ स्क्रीन साफ़ करने का फ़ंक्शन
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# ✅ डायनामिक ASCII बॉक्स (स्क्रीन साइज के अनुसार ऑटो-फिट)
def show_banner():
    width = get_terminal_size().columns
    title = "IP TRACKER"
    author = "Author  : @RealTheWarrior"
    version = "Version : 1.0.0"

    box_width = min(width - 4, 50)  # स्क्रीन के हिसाब से बॉक्स की चौड़ाई सेट करें
    content = f"\n{title.center(box_width)}\n{'-' * box_width}\n{author.center(box_width)}\n{version.center(box_width)}\n"
    centered_panel = Align.center(Panel(Align.center(content), style="green", width=box_width + 4))
    console.print(centered_panel)

# ✅ लोडिंग एनिमेशन (4 सेकंड तक चलेगा)
def loading_animation(text):
    animation = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    start_time = time.time()
    while time.time() - start_time < 4:
        for frame in animation:
            print(f"\r{text} {frame}", end="", flush=True)
            time.sleep(0.1)
    print("\r" + " " * (len(text) + 2), end="\r")

# ✅ Scam Score फ़ेच करना
def get_scam_score(ip):
    try:
        url = f"https://scamalytics.com/ip/{ip}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return "[yellow]⚠ Scam Score Not Available ⚠[/yellow]"

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        match = re.search(r"Fraud Score: (\d+)", text)

        if match:
            score = int(match.group(1))
            if score >= 70:
                return f"[red]{score}% (High Risk) 🚨[/red]"
            elif score >= 30:
                return f"[yellow]{score}% (Suspicious) ⚠️[/yellow]"
            else:
                return f"[green]{score}% (Safe) ✅[/green]"
        else:
            return "[yellow]⚠ Scam Score Not Found ⚠[/yellow]"
    except requests.exceptions.RequestException:
        return "[red]❌ Scam Score Fetching Failed![/red]"

# ✅ IP ट्रैकिंग फ़ंक्शन
def track_ip(ip):
    try:
        console.print(f"\n[bold cyan]🔍 Scanning IP: {ip}[/bold cyan]\n")
        loading_animation("[+] Connecting to IP Database...")

        ip_info_url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,mobile,hosting,query"
        ip_response = requests.get(ip_info_url).json()

        if ip_response.get('status') == 'fail':
            console.print("[red]❌ Invalid IP Address![/red]")
            return

        loading_animation("[+] Checking for Scam Score...")
        scam_score = get_scam_score(ip)
        loading_animation("[+] Processing Data...")

        # ✅ रिज़ल्ट टेबल
        table = Table(title="🌍 Warrior IP Tracker Results")
        table.add_column("Attribute", style="cyan")
        table.add_column("Details", style="green")

        table.add_row("IP Address", ip_response.get('query', 'N/A'))
        table.add_row("Country", ip_response.get('country', 'N/A'))
        table.add_row("Region", ip_response.get('regionName', 'N/A'))
        table.add_row("City", ip_response.get('city', 'N/A'))
        table.add_row("ZIP Code", ip_response.get('zip', 'N/A'))
        table.add_row("Latitude", str(ip_response.get('lat', 'N/A')))
        table.add_row("Longitude", str(ip_response.get('lon', 'N/A')))
        table.add_row("ISP", ip_response.get('isp', 'N/A'))
        table.add_row("Organization", ip_response.get('org', 'N/A'))
        table.add_row("ASN", ip_response.get('as', 'N/A'))
        table.add_row("Mobile Network?", "Yes" if ip_response.get('mobile', False) else "No")
        table.add_row("Hosting Provider?", "Yes" if ip_response.get('hosting', False) else "No")
        table.add_row("Scam Score", scam_score)

        console.print(table)

        # ✅ Exit Info (अब रिजल्ट के नीचे)
        console.print("\n[bold yellow][Ctrl + C] for Exit[/bold yellow]\n")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Network Error: {str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Unexpected Error: {str(e)}[/red]")

# ✅ मुख्य फ़ंक्शन (CLI + Interactive Mode)
def main():
    clear_screen()
    show_banner()

    if len(sys.argv) > 1:
        ip = sys.argv[1]
        track_ip(ip)
        return

    while True:
        try:
            console.print("\n[bold red][+] Enter IP Address to Track: [/bold red]", end="")
            ip = input()
            if ip.strip():
                track_ip(ip)
        except KeyboardInterrupt:
            console.print("\n[bold red]❌ Exiting...[/bold red]")
            break

if __name__ == "__main__":
    main()