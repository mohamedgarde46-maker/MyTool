#!/usr/bin/python3
import os
import sys
import socket
import subprocess

# ألوان ANSI الكلاسيكية - مضمونة وتعمل على أي ترمينال بدون تشويه الخطوط
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

BANNER = f"""{GREEN}
  _  __       _   _      _                      
 | |/ /_  _  | \\ | | ___| |_ ___  ___ __ _ _ __  
 | ' /| | | ||  \\| |/ _ \\ __/ __|/ __/ _` | '_ \\ 
 | . \\| |_| || |\\  |  __/ |_\\__ \\ (_| (_| | | | |
 |_|\\_\\\\__,_||_| \\_|\\___|\\__|___/\\___\\__,_|_| |_|
{CYAN} [+] Multi-Tool Framework | Created by Mohamedgarde46-Maker {RESET}
"""

def check_root():
    if os.getuid() != 0:
        print(f"{RED}[-] تکایه ئامرازه که وه ک root کارپیبکه (sudo mytool){RESET}")
        sys.exit(1)

# 1. فحص الشبكة المحلية العادي
def network_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی تۆر (Network Scanner){RESET}")
    ip_range = input("Enter IP Range (e.g., 192.168.1.1/24): ").strip()
    if not ip_range: return
    print(f"{GREEN}[+] خەریکی پشکنینم، تکایە چاوەڕوان بە...{RESET}")
    os.system(f"arp-scan --interface=eth0 {ip_range} 2>/dev/null || arp-scan -l")

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

# 6. الأداة الجديدة: فحص الأجهزة (Device Scanner)
def device_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی ئامێرەکان (Device Scanner){RESET}")
    target = input("Enter Target IP (e.g., 192.168.1.5): ").strip()
    if not target: return
    print(f"{GREEN}[+] خەریکی پشکنینی قووڵی ئامێرەکەم...{RESET}")
    # فحص نظام التشغيل التخميني للأجهزة عبر Ping TTL والمنفذ المفتوح
    os.system(f"nmap -O -F {target} 2>/dev/null || nmap -F {target}")

# 7. الأداة الجديدة: كم واحد على الشبكة (Network Users Count)
def network_count():
    print(f"\n{YELLOW}>> پشکنینی ژمارەی ئامێرەکان لەسەر تۆڕ (Network Count){RESET}")
    print(f"{GREEN}[+] خەریکی پشکنینی سەرجەم تۆڕەکەم بۆ دۆزینەوەی هەموو ئامێرەکان...{RESET}")
    
    # الحصول على الآي بي الافتراضي للشبكة
    try:
        cmd = "ip route | grep default | awk '{print $3}'"
        gateway = subprocess.check_output(cmd, shell=True).decode().strip()
        network_prefix = ".".join(gateway.split(".")[:3]) + ".0/24"
    except:
        network_prefix = "192.168.1.0/24" # افتراضي في حال فشل التلقائي
        
    print(f"{CYAN}[*] Scanning Target Network: {network_prefix}{RESET}\n")
    
    # فحص صارم وعد الأجهزة المتصلة
    output = subprocess.check_output(f"arp-scan --interface=eth0 {network_prefix} 2>/dev/null || arp-scan -l", shell=True).decode()
    print(output)
    
    # حساب عدد الأجهزة المكتشفة في المخرجات
    devices_count = 0
    for line in output.split('\n'):
        if "responded" in line or "packets received" in line:
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
