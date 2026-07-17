#!/usr/bin/python3
import os
import sys
import socket
import subprocess
import urllib.request
import json

# ألوان ANSI الكلاسيكية
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

BANNER = f"""{GREEN}
  _  __              _ _     _              
 | |/ /_  _ _ __  __| (_)___| |_ __ _ _ __  
 | ' /| | | | '__|/ _` | / __| __/ _` | '_ \\ 
 | . \| |_| | |  | (_| | \__ \\ || (_| | | | |
 |_|\_\\\\__,_|_|   \__,_|_|___/\__\__,_|_| |_|
                                            
{CYAN} [+] Kurdistan Multi-Tool Framework v2.0 | Created by Mohamedgarde46-Maker {RESET}
"""

def check_root():
    if os.getuid() != 0:
        print(f"{RED}[-] تکایه ئامرازه که وه ک root کارپیبکه (sudo mytool){RESET}")
        sys.exit(1)

# 1. Network Scanner
def network_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی تۆر (Network Scanner){RESET}")
    print(f"{GREEN}[+] خەریکی پشکنینم، تکایە چاوەڕوان بە...{RESET}")
    os.system("arp-scan --localnet 2>/dev/null || arp-scan -l")

# 2. Port Scanner
def port_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی پۆرتەکان (Port Scanner){RESET}")
    target = input("Enter target IP or Domain: ").strip()
    if not target: return
    try: target_ip = socket.gethostbyname(target)
    except: print(f"{RED}[-] ناونیشانەکە هەڵەیە!{RESET}"); return
    common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Proxy"}
    print("\nPort\tStatus\tService")
    print("------------------------")
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        if s.connect_ex((target_ip, port)) == 0:
            print(f"{GREEN}{port}\tOPEN\t{service}{RESET}")
        s.close()

# 3. DNS Lookup
def dns_lookup():
    print(f"\n{YELLOW}>> دۆزینەوەی ناونیشانی ئایپی (DNS Lookup){RESET}")
    domain = input("Enter Domain Name: ").strip()
    if not domain: return
    try: print(f"{GREEN}[+] IP for {domain} is: {socket.gethostbyname(domain)}{RESET}")
    except: print(f"{RED}[-] نەتوانرا ئایپی بدۆزرێتەوە!{RESET}")

# 4. Ping Tester
def ping_tester():
    print(f"\n{YELLOW}>> پشکنینی بەستەر (Ping Tester){RESET}")
    host = input("Enter Target IP/Domain: ").strip()
    if not host: return
    if os.system(f"ping -c 4 {host}") == 0: print(f"{GREEN}[+] ئامێرەکە سەر هێڵە{RESET}")
    else: print(f"{RED}[-] ئامێرەکە دەرەوەی هێڵە!{RESET}")

# 5. Whois Lookup
def whois_lookup():
    print(f"\n{YELLOW}>> زانیاری دەربارەی دۆمەین (Whois Lookup){RESET}")
    domain = input("Enter Domain Name: ").strip()
    if not domain: return
    os.system(f"whois {domain} | grep -E 'Domain Name|Registrar|Creation Date|Expir'")

# 6. Device Scanner
def device_scanner():
    print(f"\n{YELLOW}>> ئامرازی پشکنینی ئامێرەکان (Device Scanner){RESET}")
    target = input("Enter Target IP: ").strip()
    if not target: return
    os.system(f"nmap -F {target}")

# 7. Network Count
def network_count():
    print(f"\n{YELLOW}>> پشکنینی ژمارەی ئامێرەکان لەسەر تۆڕ (Network Count){RESET}")
    output = subprocess.check_output("arp-scan --localnet 2>/dev/null || arp-scan -l", shell=True).decode()
    print(output)
    devices_count = sum(1 for line in output.split('\n') if any(char.isdigit() for char in line) and ":" in line and "Interface" not in line and "responded" not in line)
    print(f"{GREEN}[+] ژمارەی ئامێرەکان لەسەر تۆڕەکە: [ {devices_count} ] ئامێر{RESET}")

# 8. Subdomain Scanner
def subdomain_scanner():
    print(f"\n{YELLOW}>> پشکنینی دۆمەینی لاوەکی (Subdomain Scanner){RESET}")
    domain = input("Enter Domain (e.g., google.com): ").strip()
    if not domain: return
    subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'cpanel', 'test', 'dev']
    print(f"{GREEN}[+] Scanning subdomains for {domain}...{RESET}")
    for sub in subdomains:
        sub_host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(sub_host)
            print(f"{GREEN}[+] Found: {sub_host} -> {ip}{RESET}")
        except: pass

# 9. Header Security Checker
def header_checker():
    print(f"\n{YELLOW}>> پشکنینی پاراستنی سایت (Header Security Checker){RESET}")
    url = input("Enter URL (e.g., http://example.com): ").strip()
    if not url.startswith("http"): url = "http://" + url
    try:
        req = urllib.request.urlopen(url)
        headers = req.info()
        print(f"\n{GREEN}[+] Security Headers Check for {url}:{RESET}")
        for h in ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']:
            if h in headers: print(f" {GREEN}[SAFE] {h}: {headers[h]}{RESET}")
            else: print(f" {RED}[MISSING] {h} (Vulnerable){RESET}")
    except Exception as e: print(f"{RED}[-] Error: {e}{RESET}")

# 10. Admin Panel Finder
def admin_finder():
    print(f"\n{YELLOW}>> دۆزینەوەی پانێڵی ئەدمین (Admin Panel Finder){RESET}")
    url = input("Enter Target URL (e.g., http://example.com): ").strip()
    if not url.startswith("http"): url = "http://" + url
    panels = ['/admin', '/login', '/admin.php', '/wp-admin', '/admin/', '/administrator']
    print(f"{GREEN}[+] Checking admin pages...{RESET}")
    for p in panels:
        try:
            req = urllib.request.Request(url+p, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            if res.code == 200: print(f"{GREEN}[+] Admin Page Found: {url+p}{RESET}")
        except: pass

# 11. Subnet Calculator
def subnet_calc():
    print(f"\n{YELLOW}>> حسابکردنی تۆر (Subnet Calculator){RESET}")
    ip = input("Enter IP (e.g., 192.168.1.50): ").strip()
    if not ip: return
    parts = ip.split('.')
    if len(parts) == 4:
        print(f"{GREEN}[+] Network IP: {parts[0]}.{parts[1]}.{parts[2]}.0{RESET}")
        print(f"{GREEN}[+] Gateway IP: {parts[0]}.{parts[1]}.{parts[2]}.1{RESET}")
        print(f"{GREEN}[+] Broadcast IP: {parts[0]}.{parts[1]}.{parts[2]}.255{RESET}")
        print(f"{GREEN}[+] Subnet Mask: 255.255.255.0{RESET}")

# 12. MAC Address Lookup
def mac_lookup():
    print(f"\n{YELLOW}>> زانیاری دەربارەی ماک ئەدرەس (MAC Lookup){RESET}")
    mac = input("Enter MAC Address (e.g., AA:BB:CC:11:22:33): ").strip()
    if not mac: return
    try:
        url = f"https://api.macvendors.com/{mac}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        vendor = urllib.request.urlopen(req).read().decode()
        print(f"{GREEN}[+] Manufacturer Vendor: {vendor}{RESET}")
    except: print(f"{RED}[-] MAC not found or API Limit reached.{RESET}")

# 13. Port Banner Grabbing
def banner_grabbing():
    print(f"\n{YELLOW}>> دیاریکردنی جۆری سێرڤەر (Banner Grabbing){RESET}")
    target = input("Enter IP/Domain: ").strip()
    port = int(input("Enter Port (e.g., 22 or 80): ").strip())
    try:
        s = socket.socket()
        s.settimeout(2.0)
        s.connect((socket.gethostbyname(target), port))
        if port == 80 or port == 8080:
            s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        print(f"\n{GREEN}[+] Server Banner response:\n{banner}{RESET}")
    except Exception as e: print(f"{RED}[-] Could not grab banner: {e}{RESET}")

# 14. Local IP & Interface Finder
def local_info():
    print(f"\n{YELLOW}>> دۆزینەوەی کارتەکانی تۆر (Local Info){RESET}")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"{GREEN}[+] Hostname: {hostname}{RESET}")
    print(f"{GREEN}[+] Internal IP (Local IP): {local_ip}{RESET}")
    try:
        ext_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
        print(f"{GREEN}[+] External IP (Public IP): {ext_ip}{RESET}")
    except: pass
    print(f"\n{CYAN}[*] Active Interfaces in system:{RESET}")
    os.system("ip -br address")

# القائمة الرئيسية
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print(BANNER)
        print(f"{CYAN} تکایە ئامرازێک هەڵبژێرە:{RESET}")
        print("---------------------------------------------------------------------------------")
        print(" 1. Network Scanner (پشکنینی تۆر)         8. Subdomain Scanner (پشکنینی دۆمەین)")
        print(" 2. Port Scanner    (پشکنینی پۆرت)         9. Header Security   (پاراستنی سایت)")
        print(" 3. DNS Lookup      (ئایپی سایت)          10. Admin Finder     (پانێڵی ئەدمین)")
        print(" 4. Ping Tester     (پشکنینی بەستەر)       11. Subnet Calc      (حسابکردنی تۆر)")
        print(" 5. Whois Lookup    (زانیاری دۆمەین)       12. MAC Lookup       (ماک ئەدرەس)")
        print(" 6. Device Scanner  (پشکنینی ئامێرەکان)    13. Banner Grabbing  (جۆری سێرڤەر)")
        print(" 7. Network Count   (ژمارەی ئامێرەکان)     14. Local Network Info(کارتەکانی تۆر)")
        print("                                           15. Exit             (دەرچوون)")
        print("---------------------------------------------------------------------------------")
        
        choice = input(" [?] Choose (1-15) -> ").strip()
        
        funcs = {'1': network_scanner, '2': port_scanner, '3': dns_lookup, '4': ping_tester,
                 '5': whois_lookup, '6': device_scanner, '7': network_count, '8': subdomain_scanner,
                 '9': header_checker, '10': admin_finder, '11': subnet_calc, '12': mac_lookup,
                 '13': banner_grabbing, '14': local_info}
        
        if choice in funcs:
            funcs[choice]()
            input("\nEnter بۆ گەڕانەوە...")
        elif choice == '15':
            print(f"{GREEN}\n[+] ماڵاوا! سوپاس بۆ بەکارهێنانی ئامرازەکە {RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] هەڵبژاردنەکە هەڵەیە!{RESET}")
            os.system('sleep 1')

if __name__ == "__main__":
    main_menu()
