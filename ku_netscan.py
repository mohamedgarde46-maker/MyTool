#!/usr/bin/python3
import os
import sys
import socket
import subprocess
import arabic_reshaper
from bidi.algorithm import get_display
from rich.console import Console
from rich.table import Table

# تهيئة شاشة التنسيق والألوان
console = Console()

# دالة مطورة ومضمونة لتصحيح عرض اللغة الكردية السورانية بدون خبط الحروف
def fix_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# 1. تصميم البانر الاحترافي للأداة
BANNER = """
[bold green]
  _  __       _   _      _                      
 | |/ /_  _  | \ | | ___| |_ ___  ___ __ _ _ __  
 | ' /| | | ||  \| |/ _ \ __/ __|/ __/ _` | '_ \ 
 | . \| |_| || |\  |  __/ |_\__ \ (_| (_| | | | |
 |_|\_\\__,_||_| \_|\___|\__|___/\___\__,_|_| |_|
[/bold green]
 [bold blue]Multi-Tool Framework | Created by Mohamedgarde46-Maker[/bold blue]
"""

def print_banner():
    console.print(BANNER)

# فحص صلاحيات الـ Root
def check_root():
    if os.getuid() != 0:
        console.print(f"[bold red] [-] {fix_text('تکایە ئامرازەکە وەک root کارپێبکە (sudo mytool)')}[/bold red]")
        sys.exit(1)

# ─── الأداة الأولى: فحص الشبكة المحلية ──────────────────────────────────────────
def network_scanner():
    console.print(f"\n[bold yellow]» {fix_text('ئامرازی پشکنینی تۆڕ (Network Scanner)')}[/bold yellow]")
    ip_range = input("Enter IP Range (e.g., 192.168.1.1/24): ").strip()
    if not ip_range:
        print("Invalid range!")
        return
    
    console.print(f"[yellow]{fix_text('خەریکی پشکنینی تۆڕەکەم، تکایە چاوەڕوان بە...')}[/yellow]")
    
    # استخدام أمر arp-scan المدمج في كالي ليعطي نتائج حقيقية وسريعة للأجهزة المتصلة
    try:
        output = subprocess.check_output(f"arp-scan --interface=eth0 {ip_range} 2>/dev/null", shell=True).decode()
        print(output)
    except Exception:
        # حل بديل في حال لم تكن الواجهة eth0
        try:
            output = subprocess.check_output(f"arp-scan -l 2>/dev/null", shell=True).decode()
            print(output)
        except Exception:
            console.print(f"[red][-] {fix_text('تکایە دڵنیا بەرەوە کە arp-scan دابەزیوە لەسەر سیستمەکەت')}[/red]")

# ─── الأداة الثانية: فحص البورتات ──────────────────────────────────────────────
def port_scanner():
    console.print(f"\n[bold yellow]» {fix_text('ئامرازی پشکنینی پۆرتەکان (Port Scanner)')}[/bold yellow]")
    target = input("Enter target IP or Domain (e.g., google.com): ").strip()
    if not target: return

    try:
        target_ip = socket.gethostbyname(target)
        console.print(f"[green][+] Target IP:[/green] {target_ip}")
    except socket.gaierror:
        console.print(f"[bold red][-] {fix_text('ناونیشانەکە هەڵەیە!')}[/bold red]")
        return

    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
        3306: "MySQL", 8080: "HTTP-Proxy"
    }

    table = Table(title=fix_text("ئەنجامی پۆرتەکان"), title_style="bold cyan")
    table.add_column("Port", style="magenta", justify="center")
    table.add_column("Status", style="bold green", justify="center")
    table.add_column("Service", style="blue", justify="center")

    console.print(f"[yellow]{fix_text('خەریکی پشکنینم...')}[/yellow]")
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            table.add_row(str(port), "OPEN", service)
        s.close()
    console.print(table)

# ─── الأداة الثالثة: استخراج الآي بي والمعلومات ─────────────────────────────────
def dns_lookup():
    console.print(f"\n[bold yellow]» {fix_text('دۆزینەوەی ناونیشانی ئایپی (DNS Lookup)')}[/bold yellow]")
    domain = input("Enter Domain Name (e.g., domain.com): ").strip()
    if not domain: return
    
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[bold green][+] IP Address for {domain} is: {ip}[/bold green]")
    except socket.gaierror:
        console.print(f"[bold red][-] {fix_text('نەتوانرا ئایپی بدۆزرێتەوە!')}[/bold red]")

# ─── الأداة الرابعة: فحص الاتصال ───────────────────────────────────────────────
def ping_tester():
    console.print(f"\n[bold yellow]» {fix_text('پشکنینی بەستەر (Ping Tester)')}[/bold yellow]")
    host = input("Enter Target IP/Domain to Ping: ").strip()
    if not host: return
    
    console.print(f"[yellow]{fix_text('خەریکی ناردنی پاکێتم...')}[/yellow]")
    response = os.system(f"ping -c 4 {host}")
    if response == 0:
        console.print(f"[bold green][+] {fix_text('ئامێرەکە سەر هێڵە ومەبەست بەردەستە')}[/bold green]")
    else:
        console.print(f"[bold red][-] {fix_text('ئامێرەکە دەرەوەی هێڵە!')}[/bold red]")

# ─── القائمة الرئيسية ─────────────────────────────────────────────────────────
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print_banner()
        
        console.print(f"\n[bold cyan] {fix_text('تکایە ئامرازێک هەڵبژێرە:')}[/bold cyan]")
        print("------------------------------------------------")
        print(f" 1. Network Scanner       ({fix_text('پشکنینی تۆڕ')})")
        print(f" 2. Port Scanner          ({fix_text('پشکنینی پۆرت')})")
        print(f" 3. DNS Lookup / IP Find  ({fix_text('دۆزینەوەی ئایپی')})")
        print(f" 4. Ping Tester           ({fix_text('پشکنینی بەستەر')})")
        print(f" 5. Exit                  ({fix_text('دەرچوون')})")
        print("------------------------------------------------")
        
        choice = input(" [?] Choose -> ").strip()
        
        if choice == '1':
            network_scanner()
            input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))
        elif choice == '2':
            port_scanner()
            input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))
        elif choice == '3':
            dns_lookup()
            input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))
        elif choice == '4':
            ping_tester()
            input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))
        elif choice == '5':
            console.print(f"[bold green]\n[+] {fix_text('ماڵاوا! سوپاس بۆ بەکارهێنانی ئامرازەکە')}[/bold green]")
            sys.exit(0)
        else:
            console.print(f"[bold red][!] {fix_text('هەڵبژاردنەکە هەڵەیە!')}[/bold red]")
            os.system('sleep 1.2')

if __name__ == "__main__":
    main_menu()
