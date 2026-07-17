import arabic_reshaper
from bidi.algorithm import get_display

def fix_kurdish_text(text):
    # إعادت تشكيل الحروف لكي تتصل ببعضها
    reshaped_text = arabic_reshaper.reshape(text)
    # تعديل اتجاه النص من اليمين إلى اليسار
    return get_display(reshaped_text)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ku_netscan.py
ئامرازی سکانکردنی شبکە بە زمانی کوردیی سۆرانی
Network Scanner Tool - Kurdish Sorani Interface (for Kali Linux)

بۆ بەکارهێنانی یاسایی و فێربوون بەکاردێت (Authorized/Educational use only).
پێویستە: Python 3، پاکێجی nmap لەسەر سیستەم دامەزرابێت، و pip packages: python-nmap, rich

دامەزراندن (Install requirements):
    sudo apt install nmap -y
    pip install python-nmap rich --break-system-packages
"""

import sys
import socket
import subprocess
import ipaddress
import platform
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.prompt import Prompt, IntPrompt
    from rich import box
except ImportError:
    print("[!] پاکێجی 'rich' نەدۆزرایەوە. ئەمە بنووسە:")
    print("    pip install rich --break-system-packages")
    sys.exit(1)

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

console = Console()

BANNER = r"""
[bold cyan]
 _  __ _   _   _ ______ _______   _____  _____          _   _ 
| |/ /| | | | | |  ____|__   __| / ____|/ ____|   /\   | \ | |
| ' / | | | | | | |__     | |   | (___ | |       /  \  |  \| |
|  <  | | | | | |  __|    | |    \___ \| |      / /\ \ | . ` |
| . \ | |_| |_| | |____   | |    ____) | |____ / ____ \| |\  |
|_|\_\ \___/ \___/|______| |_|   |_____/ \_____/_/    \_\_| \_|
[/bold cyan]
[bold yellow]  ئامرازی سکانکردنی شبکە | Network Scan Tool[/bold yellow]
[dim]  تەنها بۆ شبکەی خۆت یان بە مۆڵەت بەکاربهێنە | Authorized use only[/dim]
"""


def print_banner():
    console.print(BANNER)


def check_root():
    """ئاگادارکردنەوە ئەگەر بەکارهێنەر root نەبێت"""
    import os
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        console.print(
            "[yellow]⚠ ئاگاداری:[/yellow] هەندێک تایبەتمەندی پێویستیان بە دەسەڵاتی [bold]root[/bold] هەیە. "
            "باشترە بە [bold]sudo[/bold] پڕۆگرامەکە ڕابکەیت.\n"
        )


def get_local_info():
    """پیشاندانی زانیاری سیستەم و ئینتەرنێت لۆکاڵی"""
    table = Table(title="زانیاری سیستەم | System Info", box=box.ROUNDED, title_style="bold green")
    table.add_column("خانە", style="cyan", no_wrap=True)
    table.add_column("بەها", style="white")

    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "نەزانراو"

    table.add_row("ناوی سیستەم (Hostname)", hostname)
    table.add_row("IP لۆکاڵی (Local IP)", local_ip)
    table.add_row("سیستەمی کارپێکردن (OS)", f"{platform.system()} {platform.release()}")
    table.add_row("کاتژمێر (Time)", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        result = subprocess.run(["ip", "-4", "addr"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = [l.strip() for l in result.stdout.splitlines() if "inet " in l]
            ifaces = "\n".join(lines) if lines else "نەدۆزرایەوە"
        else:
            ifaces = "نەتوانرا وەربگیرێت"
    except Exception:
        ifaces = "کۆمانی 'ip' بەردەست نییە"

    table.add_row("ئینتەرفەیسەکان (Interfaces)", ifaces)
    console.print(table)


def host_discovery(subnet: str):
    """دۆزینەوەی ئامێرە چالاکەکان لە شبکەیەکدا (ping sweep)"""
    if not NMAP_AVAILABLE:
        console.print("[red]✗ python-nmap دانەمەزراوە.[/red] بنووسە: pip install python-nmap --break-system-packages")
        return

    try:
        ipaddress.ip_network(subnet, strict=False)
    except ValueError:
        console.print(f"[red]✗ فۆرماتی subnet هەڵەیە:[/red] {subnet}\nنموونە: 192.168.1.0/24")
        return

    scanner = nmap.PortScanner()
    console.print(f"\n[cyan]در حال دۆزینەوەی ئامێرەکان لە[/cyan] [bold]{subnet}[/bold] ...\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("سکانکردن (Ping Sweep)...", total=None)
        try:
            scanner.scan(hosts=subnet, arguments="-sn")
        except Exception as e:
            progress.stop()
            console.print(f"[red]✗ هەڵە ڕوویدا:[/red] {e}")
            return
        progress.update(task, completed=True)

    hosts_list = [(x, scanner[x].get('status', {}).get('state', '')) for x in scanner.all_hosts()]

    if not hosts_list:
        console.print("[yellow]هیچ ئامێرێکی چالاک نەدۆزرایەوە.[/yellow]")
        return

    table = Table(title=f"ئامێرە چالاکەکان لە {subnet}", box=box.ROUNDED, title_style="bold green")
    table.add_column("IP Address", style="cyan")
    table.add_column("دۆخ (Status)", style="white")
    table.add_column("ناو (Hostname)", style="white")

    for ip, state in hosts_list:
        try:
            hn = socket.gethostbyaddr(ip)[0]
        except Exception:
            hn = "-"
        table.add_row(ip, state, hn)

    console.print(table)
    console.print(f"\n[bold green]کۆی گشتی:[/bold green] {len(hosts_list)} ئامێر دۆزرایەوە.\n")


def port_scan(target: str, port_range: str):
    """سکانکردنی پۆرتەکانی ئامێرێکی دیاریکراو"""
    if not NMAP_AVAILABLE:
        console.print("[red]✗ python-nmap دانەمەزراوە.[/red] بنووسە: pip install python-nmap --break-system-packages")
        return

    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        console.print(f"[red]✗ ناتوانرێت ئامانج بدۆزرێتەوە:[/red] {target}")
        return

    scanner = nmap.PortScanner()
    console.print(f"\n[cyan]در حال سکانکردنی پۆرتەکانی[/cyan] [bold]{target}[/bold] بۆ ماوەی [bold]{port_range}[/bold] ...\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("سکانکردنی پۆرتەکان...", total=None)
        try:
            scanner.scan(hosts=target, ports=port_range, arguments="-sV -T4")
        except Exception as e:
            progress.stop()
            console.print(f"[red]✗ هەڵە ڕوویدا:[/red] {e}")
            return
        progress.update(task, completed=True)

    if target not in scanner.all_hosts():
        console.print("[yellow]ئامانجەکە وەڵامی نەدایەوە یان بەردەست نییە.[/yellow]")
        return

    table = Table(title=f"پۆرتە کراوەکانی {target}", box=box.ROUNDED, title_style="bold green")
    table.add_column("پۆرت (Port)", style="cyan")
    table.add_column("پرۆتۆکۆل", style="white")
    table.add_column("دۆخ (State)", style="white")
    table.add_column("خزمەتگوزاری (Service)", style="white")
    table.add_column("وەشان (Version)", style="white")

    found_any = False
    for proto in scanner[target].all_protocols():
        ports = sorted(scanner[target][proto].keys())
        for port in ports:
            info = scanner[target][proto][port]
            state_color = "green" if info['state'] == 'open' else "red"
            table.add_row(
                str(port),
                proto,
                f"[{state_color}]{info['state']}[/{state_color}]",
                info.get('name', '-'),
                f"{info.get('product', '')} {info.get('version', '')}".strip() or "-",
            )
            found_any = True

    if not found_any:
        console.print("[yellow]هیچ پۆرتێکی کراوە نەدۆزرایەوە.[/yellow]")
    else:
        console.print(table)


def os_detection(target: str):
    """دۆزیندنەوەی سیستەمی کارپێکردنی ئامانج (OS Fingerprinting)"""
    if not NMAP_AVAILABLE:
        console.print("[red]✗ python-nmap دانەمەزراوە.[/red] بنووسە: pip install python-nmap --break-system-packages")
        return

    import os as _os
    if hasattr(_os, "geteuid") and _os.geteuid() != 0:
        console.print(
            "[yellow]⚠ ئاگاداری:[/yellow] دۆزینەوەی OS پێویستی بە دەسەڵاتی [bold]root[/bold] هەیە. "
            "بە [bold]sudo[/bold] دووبارە هەوڵ بدەرەوە.\n"
        )
        return

    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        console.print(f"[red]✗ ناتوانرێت ئامانج بدۆزرێتەوە:[/red] {target}")
        return

    scanner = nmap.PortScanner()
    console.print(f"\n[cyan]در حال دۆزینەوەی سیستەمی کارپێکردنی[/cyan] [bold]{target}[/bold] ...\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("دۆزینەوەی OS (Fingerprinting)...", total=None)
        try:
            scanner.scan(hosts=target, arguments="-O --osscan-guess")
        except Exception as e:
            progress.stop()
            console.print(f"[red]✗ هەڵە ڕوویدا:[/red] {e}")
            return
        progress.update(task, completed=True)

    if target not in scanner.all_hosts():
        console.print("[yellow]ئامانجەکە وەڵامی نەدایەوە یان بەردەست نییە.[/yellow]")
        return

    osmatches = scanner[target].get('osmatch', [])

    if not osmatches:
        console.print(
            "[yellow]نەتوانرا سیستەمی کارپێکردن بە دڵنیایی دەستنیشان بکرێت.[/yellow]\n"
            "[dim]ئەمە ڕوودەدات کاتێک فایەرۆڵ (firewall) ئامانج پاکێتەکان دەگرێت.[/dim]"
        )
        return

    table2 = Table(title=f"سیستەمی کارپێکردنی {target}", box=box.ROUNDED, title_style="bold green")
    table2.add_column("ناوی سیستەم (OS)", style="white")
    table2.add_column("ڕێژەی دڵنیایی (Accuracy)", style="cyan")
    for match in osmatches[:5]:
        acc = int(match.get('accuracy', '0'))
        acc_color = "green" if acc >= 85 else ("yellow" if acc >= 60 else "red")
        table2.add_row(match.get('name', '-'), f"[{acc_color}]{acc}%[/{acc_color}]")

    console.print(table2)


def full_scan(target: str):
    """ئامرازی گشتگیر: دۆزینەوە + پۆرت + زانیاری"""
    console.print(Panel(f"[bold]سکانی گشتگیر بۆ:[/bold] {target}", style="cyan"))
    port_scan(target, "1-1024")
    os_detection(target)


def main_menu():
    while True:
        console.print(Panel.fit(
            "[bold]١.[/bold] دۆزینەوەی ئامێرەکانی چالاک لە شبکەکە (Host Discovery)\n"
            "[bold]٢.[/bold] سکانکردنی پۆرتەکان (Port Scan)\n"
            "[bold]٣.[/bold] دۆزینەوەی سیستەمی کارپێکردن (OS Detection)\n"
            "[bold]٤.[/bold] سکانی گشتگیر (Full Scan)\n"
            "[bold]٥.[/bold] زانیاری سیستەم (System Info)\n"
            "[bold]٦.[/bold] دەرچوون (Exit)",
            title="مینیۆی سەرەکی | Main Menu",
            border_style="cyan",
        ))

        choice = Prompt.ask("[bold cyan]هەڵبژاردەیەک دیاری بکە[/bold cyan]", choices=["1", "2", "3", "4", "5", "6"], default="6")

        if choice == "1":
            subnet = Prompt.ask("[cyan]subnet بنووسە (نموونە: 192.168.1.0/24)[/cyan]")
            host_discovery(subnet)
        elif choice == "2":
            target = Prompt.ask("[cyan]IP یان ناوی ئامانج بنووسە[/cyan]")
            prange = Prompt.ask("[cyan]مەودای پۆرت بنووسە (نموونە: 1-1000)[/cyan]", default="1-1024")
            port_scan(target, prange)
        elif choice == "3":
            target = Prompt.ask("[cyan]IP یان ناوی ئامانج بنووسە[/cyan]")
            os_detection(target)
        elif choice == "4":
            target = Prompt.ask("[cyan]IP یان ناوی ئامانج بنووسە[/cyan]")
            full_scan(target)
        elif choice == "5":
            get_local_info()
        elif choice == "6":
            console.print("[bold green]خوداحافیز! 👋[/bold green]")
            break

        console.print()  # empty line


def main():
    console.clear()
    print_banner()
    check_root()

    if not NMAP_AVAILABLE:
        console.print(
            "[yellow]⚠ ئاگاداری:[/yellow] پاکێجی 'python-nmap' دانەمەزراوە.\n"
            "بۆ کارکردنی تەواوی ئامرازەکە ئەمە بنووسە:\n"
            "  [bold]sudo apt install nmap -y[/bold]\n"
            "  [bold]pip install python-nmap --break-system-packages[/bold]\n"
        )

    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]ڕاگیرا لەلایەن بەکارهێنەرەوە.[/bold red]")
        sys.exit(0)


if __name__ == "__main__":
    main()
import sys
# استدعاء الفانكشن التي قمنا بعملها سابقاً للغة الكردية
import arabic_reshaper
from bidi.algorithm import get_display

def fix_text(text):
    return get_display(arabic_reshaper.reshape(text))

# --- هنا نضع الأدوات الفرعية ---

def network_scanner():
    print(fix_text("خەریکی پشکنینی تۆڕەکەم..."))
    # ضع هنا كود فحص الشبكة القديم الخاص بك

def port_scanner():
    print(fix_text("خەریکی پشکنینی پۆرتەکانم..."))
    # هنا ستكتب كود أداة فحص البورتات الجديدة (سنشرحها بالأسفل)

def ip_finder():
    print(fix_text("دۆزینەوەی ناونیشانی IP..."))
    # هنا ستكتب كود أداة معرفة الآي بي

# --- القائمة الرئيسية ---
def main_menu():
    while True:
        print("\n==============================")
        print(fix_text(" تکایە ئامرازێک هەڵبژێرە:"))
        print("1. Network Scanner (پشکنینی تۆڕ)")
        print("2. Port Scanner (پشکنینی پۆرت)")
        print("3. IP Finder (دۆزینەوەی ئایپی)")
        print("4. Exit (دەرچوون)")
        print("==============================")
        
        choice = input(" -> ")
        
        if choice == '1':
            network_scanner()
        elif choice == '2':
            port_scanner()
        elif choice == '3':
            ip_finder()
        elif choice == '4':
            print(fix_text("ماڵاوا!"))
            sys.exit()
        else:
            print(fix_text("هەڵبژاردنەکە هەڵەیە، دووبارە هەوڵ بدەرەوە."))

if __name__ == "__main__":
    main_menu()
