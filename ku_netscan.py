#!/usr/bin/python3
import os
import sys
import socket
import arabic_reshaper
from bidi.algorithm import get_display
from rich.console import Console
from rich.table import Table

# تهيئة شاشة التنسيق
console = Console()

# دالة لتصحيح عرض اللغة الكردية السورانية في الترمينال
def fix_text(text):
    return get_display(arabic_reshaper.reshape(text))

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

# 2. فحص صلاحيات الـ Root
def check_root():
    if os.getuid() != 0:
        console.print(f"[bold red] [-] {fix_text('تکایە ئامرازەکە وەک root کارپێبکە (sudo mytool)')}[/bold red]")
        sys.exit(1)

# 3. الأداة الأولى: فحص البورتات المصححة والمضمونة
def port_scanner():
    console.print(f"\n[bold yellow]» {fix_text('پشکنینی پۆرتەکان (Port Scanner)')}[/bold yellow]")
    target = input("Enter target IP or Domain (e.g. google.com): ").strip()
    
    if not target:
        print("Invalid target!")
        return

    try:
        target_ip = socket.gethostbyname(target)
        console.print(f"[green][+] Target IP:[/green] {target_ip}")
    except socket.gaierror:
        console.print(f"[bold red][-] {fix_text('ناونیشانەکە هەڵەیە!')}[/bold red]")
        return

    # قائمة البورتات الشهيرة
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
        3306: "MySQL", 8080: "HTTP-Proxy"
    }

    # إنشاء جدول منسق لعرض النتائج
    table = Table(title=fix_text("ئەنجامی پشکنینی پۆرتەکان"), title_style="bold cyan")
    table.add_column("Port", style="magenta", justify="center")
    table.add_column("Status", style="bold green", justify="center")
    table.add_column("Service", style="blue", justify="center")

    console.print(f"[yellow]{fix_text('خەریکی پشکنینم، تکایە چاوەڕوان بە...')}[/yellow]")
    
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            table.add_row(str(port), "OPEN", service)
        s.close()

    print("\n")
    console.print(table)

# 4. الأداة الثانية: فحص الشبكة (Network Scanner) - ضع كود الفحص القديم هنا إذا أردت
def network_scanner():
    console.print(f"\n[bold yellow]» {fix_text('پشکنینی تۆڕ (Network Scanner)')}[/bold yellow]")
    console.print(f"[cyan][+] {fix_text('ئەم بەشە بەم زووانە چالاک دەبێت یان لێرە کۆدی کۆنت دابنێ')}[/cyan]")
    input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))

# 5. القائمة الرئيسية التي تجمع كل الأدوات وتتحكم بالتشغيل
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print_banner()
        
        console.print(f"\n[bold cyan] {fix_text('تکایە ئامرازێک هەڵبژێرە:')}[/bold cyan]")
        print("---------------------------------------")
        print(f" 1. Network Scanner ({fix_text('پشکنینی تۆڕ')})")
        print(f" 2. Port Scanner    ({fix_text('پشکنینی پۆرت')})")
        print(f" 3. Exit            ({fix_text('دەرچوون')})")
        print("---------------------------------------")
        
        choice = input(" [?] Choose -> ").strip()
        
        if choice == '1':
            network_scanner()
        elif choice == '2':
            port_scanner()
            input(fix_text("\nبۆ گەڕانەوە ئینتەر داگرە..."))
        elif choice == '3':
            console.print(f"[bold green]\n[+] {fix_text('ماڵاوا! سوپاس بۆ بەکارهێنانی ئامرازەکە')}[/bold green]")
            sys.exit(0)
        else:
            console.print(f"[bold red][!] {fix_text('هەڵبژاردنەکە هەڵەیە!')}[/bold red]")
            os.system('sleep 1.5')

if __name__ == "__main__":
    main_menu()
