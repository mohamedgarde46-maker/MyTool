#!/usr/bin/python3
import os
import sys
import socket
import subprocess

# ألوان ANSI الكلاسيكية
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# تغيير الاسم والبانر إلى Kurdistan
BANNER = f"""{GREEN}
  _  __              _ _     _              
 | |/ /_  _ _ __  __| (_)___| |_ __ _ _ __  
 | ' /| | | | '__|/ _` | / __| __/ _` | '_ \\ 
 | . \| |_| | |  | (_| | \__ \\ || (_| | | | |
 |_|\_\\\\__,_|_|   \__,_|_|___/\__\__,_|_| |_|
                                            
{CYAN} [+] Kurdistan Multi-Tool Framework | Created by Mohamedgarde46-Maker {RESET}
"""

def check_root():
    if os.getuid() != 0:
        print(f"{RED}[-] تکایه ئامرازه که وه ک root کارپیبکه (sudo mytool){RESET}")
        sys.exit(1)

# 1. فحص الشبكة المحلية المطور (يفحص كل الأجهزة بدقة)
def network_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی تۆر (Network Scanner){RESET}")
    print(f"{GREEN}[+] خەریکی پشکنینم، تکایە چاوەڕوان بە...{RESET}")
    # الفحص بدون تحديد واجهة إجبارية ليجلب كل شيء متصل بالواي فاي والكيبل
    os.system("arp-scan --localnet 2>/dev/null || arp-scan -l")

# 2. فحص البورتات
def port_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی پۆرتەکان (Port Scanner){RESET}")
    target = input("Enter target IP or Domain (e.g., google.com): ").strip()
    if not target: return
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{GREEN}[+] Target IP: {target_ip}{RESET}")
    except socket.gaierror:
        print(f"{RED}[-] ناونیشانەکە هەڵەیە!{RESET}")
        return

    common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Proxy"}
    print("\nPort\tStatus\tService")
    print("------------------------")
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"{GREEN}{port}\tOPEN\t{service}{RESET}")
        s.close()

# 3. معرفة الآي بي
def dns_lookup():
    print(f"\n{YELLOW}>> دۆزینەوەی ناونیشانی ئایپی (DNS Lookup){RESET}")
    domain = input("Enter Domain Name (e.g., domain.com): ").strip()
    if not domain: return
    try:
        ip = socket.gethostbyname(domain)
        print(f"{GREEN}[+] IP Address for {domain} is: {ip}{RESET}")
    except socket.gaierror:
        print(f"{RED}[-] نەتوانرا ئایپی بدۆزرێتەوە!{RESET}")

# 4. فحص اتصال السيرفر
def ping_tester():
    print(f"\n{YELLOW}>> پشکنینی بەستەر (Ping Tester){RESET}")
    host = input("Enter Target IP/Domain: ").strip()
    if not host: return
    response = os.system(f"ping -c 4 {host}")
    if response == 0:
        print(f"{GREEN}[+] ئامێرەکە سەر هێڵە ومەبەست بەردەستە{RESET}")
    else:
        print(f"{RED}[-] ئامێرەکە دەرەوەی هێڵە!{RESET}")

# 5. معلومات الدومين والموقع
def whois_lookup():
    print(f"\n{YELLOW}>> زانیاری دەربارەی دۆمەین (Whois Lookup){RESET}")
    domain = input("Enter Domain Name (e.g., google.com): ").strip()
    if not domain: return
    print(f"{GREEN}[+] خەریکی هێنانی زانیاریم...{RESET}")
    os.system(f"whois {domain} | grep -E 'Domain Name|Registrar|Creation Date|Expir'")

# 6. فحص الأجهزة قووڵ
def device_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی ئامێرەکان (Device Scanner){RESET}")
    target = input("Enter Target IP (e.g., 192.168.1.5): ").strip()
    if not target: return
    print(f"{GREEN}[+] خەریکی پشکنینی قووڵی ئامێرەکەم...{RESET}")
    os.system(f"nmap -F {target}")

# 7. حل مشكلة العدد الناقص وفحص الشبكة بالكامل
def network_count():
    print(f"\n{YELLOW}>> پشکنینی ژمارەی ئامێرەکان لەسەر تۆڕ (Network Count){RESET}")
    print(f"{GREEN}[+] خەریکی پشکنینی گشتی و دۆزینەوەی هەموو ئامێرەکانم...{RESET}\n")
    
    # الفحص الشامل عبر الإعدادات المحلية التلقائية لضمان التقاط الـ 5 أجهزة كاملة
    output = subprocess.check_output("arp-scan --localnet 2>/dev/null || arp-scan -l", shell=True).decode()
    print(output)
    
    # حساب عدد الأجهزة بدقة من المخرجات المكتوبة
    devices_count = 0
    for line in output.split('\n'):
        if "responded" in line or "packets received" in line or "Interface" in line:
            continue
        if any(char.isdigit() for char in line) and ":" in line:
            devices_count += 1
            
    print("------------------------------------------------")
    print(f"{GREEN}[+] سەرکەوتوو بوو! ژمارەی ئامێرەکان لەسەر تۆڕەکە: [ {devices_count} ] ئامێر{RESET}")
    print("------------------------------------------------")

# القائمة الرئيسية
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print(BANNER)
        print(f"{CYAN} تکایە ئامرازێک هەڵبژێرە:{RESET}")
        print("------------------------------------------------")
        print(" 1. Network Scanner       (پشکنینی تۆر)")
        print(" 2. Port Scanner          (پشکنینی پۆرت)")
        print(" 3. DNS Lookup / IP Find  (دۆزینەوەی ئایپی)")
        print(" 4. Ping Tester           (پشکنینی بەستەر)")
        print(" 5. Whois Lookup          (زانیاری دۆمەین)")
        print(" 6. Device Scanner        (پشکنینی ئامێرەکان)")
        print(" 7. Network Count         (ژمارەی ئامێرەکان)")
        print(" 8. Exit                  (دەرچوون)")
        print("------------------------------------------------")
        
        choice = input(" [?] Choose -> ").strip()
        
        if choice == '1':
            network_scanner()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '2':
            port_scanner()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '3':
            dns_lookup()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '4':
            ping_tester()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '5':
            whois_lookup()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '6':
            device_scanner()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '7':
            network_count()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '8':
            print(f"{GREEN}\n[+] ماڵاوا! سوپاس بۆ بەکارهێنانی ئامرازەکە{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] هەڵبژاردنەکە هەڵەیە!{RESET}")
            os.system('sleep 1')

if __name__ == "__main__":
    main_menu()
