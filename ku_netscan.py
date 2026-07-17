#!/usr/bin/python3
import os
import sys
import socket
import subprocess
import urllib.request
import json
import re
#!/usr/bin/python3
import os
import sys
import socket
import subprocess
import urllib.request
import json
import re
import phonenumbers
from phonenumbers import geocoder, carrier
# ألوان ورموز التنسيق الاحترافية
GREEN  = '\033[92m'
RED    = '\033[91m'
YELLOW = '\033[93m'
BLUE   = '\033[94m'
MAGENTA= '\033[95m'
CYAN   = '\033[96m'
WHITE  = '\033[97m'
BOLD   = '\033[1m'
RESET  = '\033[0m'

INFO  = f"{BOLD}{BLUE}[*]{RESET}"
SUCC  = f"{BOLD}{GREEN}[+]{RESET}"
ERR   = f"{BOLD}{RED}[-]{RESET}"
WARN  = f"{BOLD}{YELLOW}[!]{RESET}"

BANNER = f"""{BOLD}{GREEN}
  _  __              _ _     _              
 | |/ /_  _ _ __  __| (_)___| |_ __ _ _ __  
 | ' /| | | | '__|/ _` | / __| __/ _` | '_ \\ 
 | . \\| |_| | |  | (_| | \\__ \\ || (_| | | | |
 |_|\\_\\\\__,_|_|   \\__,_|_|___/\\__\\__,_|_| |_|
                                            
{RESET}{BOLD}{CYAN}  ⚡ Kurdistan Ultimate Framework v3.5 | By Mohamedgarde46-Maker ⚡
{RESET}"""

def check_root():
    if os.getuid() != 0:
        print(f"\n{ERR} {BOLD}{RED}تکایه ئامرازه که وه ک root کارپیبکه (sudo mytool){RESET}\n")
        sys.exit(1)

def print_header(title_en, title_ku):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN} >> {title_en} ({title_ku}) {RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def back_menu():
    input(f"\n{BOLD}{YELLOW} ↩ Press [ Enter ] بۆ گەڕانەوە...{RESET}")

# 1. Network Scanner
def network_scanner():
    print_header("Network Scanner", "پشکنینی تۆر")
    print(f"{SUCC} خەریکی پشکنینم، تکایە چاوەڕوان بە...\n")
    os.system("arp-scan --localnet 2>/dev/null || arp-scan -l")

# 2. Port Scanner
def port_scanner():
    print_header("Port Scanner", "پشکنینی پۆرتەکان")
    target = input(f" {INFO} Enter target IP or Domain: ").strip()
    if not target: return
    try: target_ip = socket.gethostbyname(target)
    except: print(f"{ERR} ناونیشانەکە هەڵەیە!"); return
    print(f"{SUCC} Target IP: {BOLD}{WHITE}{target_ip}{RESET}\n")
    common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Proxy"}
    print(f"{BOLD}{MAGENTA} ┌──────┬──────────┬─────────────┐")
    print(" │ Port │  Status  │   Service   │")
    print(" ├──────┼──────────┼─────────────┤")
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        if s.connect_ex((target_ip, port)) == 0:
            print(f" │ {port:<4} │   {GREEN}OPEN{RESET}   │ {service:<11} │")
        s.close()
    print(f" └──────┴──────────┴─────────────┘{RESET}")

# 3. DNS Lookup
def dns_lookup():
    print_header("DNS Lookup", "دۆزینەوەی ئایپی سایت")
    domain = input(f" {INFO} Enter Domain Name: ").strip()
    if not domain: return
    try: print(f"{SUCC} IP for {domain} is: {BOLD}{GREEN}{socket.gethostbyname(domain)}{RESET}")
    except: print(f"{ERR} نەتوانرا ئایپی بدۆزرێتەوە!")

# 4. Ping Tester
def ping_tester():
    print_header("Ping Tester", "پشکنینی بەستەر")
    host = input(f" {INFO} Enter Target: ").strip()
    if not host: return
    if os.system(f"ping -c 4 {host}") == 0: print(f"\n{SUCC} ئامێرەکە سەر هێڵە")
    else: print(f"\n{ERR} ئامێرەکە دەرەوەی هێڵە!")

# 5. Whois Lookup
def whois_lookup():
    print_header("Whois Lookup", "زانیاری دۆمەین")
    domain = input(f" {INFO} Enter Domain: ").strip()
    if not domain: return
    os.system(f"whois {domain} | grep -E 'Domain Name|Registrar|Creation Date|Expir'")

# 6. Device Scanner
def device_scanner():
    print_header("Device Scanner", "پشکنینی ئامێرەکان")
    target = input(f" {INFO} Enter Target IP: ").strip()
    if not target: return
    os.system(f"nmap -F {target}")

# 7. Network Count
def network_count():
    print_header("Network Count", "ژمارەی ئامێرەکان")
    output = subprocess.check_output("arp-scan --localnet 2>/dev/null || arp-scan -l", shell=True).decode()
    devices_count = sum(1 for line in output.split('\n') if any(char.isdigit() for char in line) and ":" in line and "Interface" not in line and "responded" not in line)
    print(f"{SUCC} ژمارەی ئامێرەکان لەسەر تۆڕەکە: [ {BOLD}{YELLOW}{devices_count}{RESET} ] ئامێر")

# 8. Subdomain Scanner
def subdomain_scanner():
    print_header("Subdomain Scanner", "پشکنینی دۆمەینی لاوەکی")
    domain = input(f" {INFO} Enter Domain: ").strip()
    if not domain: return
    subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'cpanel', 'test', 'dev']
    for sub in subdomains:
        sub_host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(sub_host)
            print(f" {SUCC} Found: {BOLD}{CYAN}{sub_host:<20}{RESET} -> {GREEN}{ip}{RESET}")
        except: pass

# 9. Header Security
def header_checker():
    print_header("Header Security", "پشکنینی پاراستنی سایت")
    url = input(f" {INFO} Enter URL: ").strip()
    if not url.startswith("http"): url = "http://" + url
    try:
        headers = urllib.request.urlopen(url).info()
        for h in ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy']:
            if h in headers: print(f"  {GREEN}[SAFE]{RESET} {h}: {headers[h]}")
            else: print(f"  {RED}[VULN]{RESET} {h} is Missing!")
    except Exception as e: print(f"{ERR} Error: {e}")

# 10. Admin Finder
def admin_finder():
    print_header("Admin Finder", "دۆزینەوەی پانێڵی ئەدمین")
    url = input(f" {INFO} Enter URL: ").strip()
    if not url.startswith("http"): url = "http://" + url
    for p in ['/admin', '/login', '/wp-admin', '/administrator']:
        try:
            req = urllib.request.Request(url+p, headers={'User-Agent': 'Mozilla/5.0'})
            if urllib.request.urlopen(req).code == 200: print(f" {SUCC} Found: {BOLD}{GREEN}{url+p}{RESET}")
        except: pass

# 11. Subnet Calc
def subnet_calc():
    print_header("Subnet Calc", "حسابکردنی تۆر")
    ip = input(f" {INFO} Enter IP: ").strip()
    if not ip or len(ip.split('.')) != 4: return
    p = ip.split('.')
    print(f" {SUCC} Network: {p[0]}.{p[1]}.{p[2]}.0 | Gateway: {p[0]}.{p[1]}.{p[2]}.1")

# 12. MAC Lookup
def mac_lookup():
    print_header("MAC Lookup", "زانیاری ماک ئەدرەس")
    mac = input(f" {INFO} Enter MAC Address: ").strip()
    try:
        vendor = urllib.request.urlopen(f"https://api.macvendors.com/{mac}").read().decode()
        print(f"\n{SUCC} Vendor: {BOLD}{GREEN}{vendor}{RESET}")
    except: print(f"{ERR} MAC not found.")

# 13. Banner Grabbing
def banner_grabbing():
    print_header("Banner Grabbing", "دیاریکردنی جۆری سێرڤەر")
    target = input(f" {INFO} Enter IP/Domain: ").strip()
    port_in = input(f" {INFO} Enter Port (Default 80): ").strip()
    port = int(port_in) if port_in.isdigit() else 80
    try:
        s = socket.socket()
        s.settimeout(2.0)
        s.connect((socket.gethostbyname(target), port))
        if port in [80, 8080]: s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        print(f"\n{SUCC} Response:\n{CYAN}{s.recv(512).decode(errors='ignore').strip()}{RESET}")
    except Exception as e: print(f"{ERR} Failed: {e}")

# 14. Local Network Info
def local_info():
    print_header("Local Info", "کارتەکانی تۆر")
    print(f" {SUCC} Hostname: {socket.gethostname()}")
    os.system("ip -br address")

# 15. Cloudflare Bypass
def cloudflare_bypass():
    print_header("Cloudflare Bypass", "دۆزینەوەی ئایپی ڕاستەقینە")
    domain = input(f" {INFO} Enter Target Domain: ").strip()
    if not domain: return
    os.system(f"dig +short cname {domain} && dig +short mx {domain}")

# 16. Phone Info Lookup
def phone_lookup():
    print_header("Phone Lookup", "زانیاری ژمارەی تەلەفۆن")
    phone = input(f" {INFO} Enter Phone Number: ").strip()
    if not phone: return
    try:
        res = urllib.request.urlopen(f"https://html.nu/api/phone.php?number={phone}").read().decode()
        print(f"{SUCC} Data: {GREEN}{res}{RESET}")
    except: print(f"{ERR} Error fetching phone data.")

# 17. Shellshock Scanner
def shellshock_scan():
    print_header("Shellshock Scanner", "پشکنینی کلاود سێرڤەر")
    target = input(f" {INFO} Enter Target IP: ").strip()
    if not target: return
    os.system(f"nmap -sV --script http-shellshock {target}")

# 18. Directory Brute-Forcer
def dir_bruter():
    print_header("Directory Bruter", "پشکنینی بووشایی سایت")
    url = input(f" {INFO} Enter Target URL: ").strip()
    if not url.startswith("http"): url = "http://" + url
    dirs = ['/backup.sql', '/.git', '/config.php', '/robots.txt']
    for d in dirs:
        try:
            if urllib.request.urlopen(url+d).code == 200: print(f" {SUCC} Found: {url+d}")
        except: pass

# 19. Email Harvester
def email_harvester():
    print_header("Email Harvester", "کۆکەرەوەی ئیمێڵ")
    domain = input(f" {INFO} Enter Target Domain: ").strip()
    if not domain: return
    os.system(f"curl -s 'https://crt.sh/?q=%25.{domain}' | grep -E -o '[A-Za-z0-9._%+-]+@{domain}' | sort -u")

# 20. Firewall Detector
def firewall_detector():
    print_header("Firewall Detector", "پشکنینی دیواری ئاگرین")
    target = input(f" {INFO} Enter Target IP: ").strip()
    if not target: return
    os.system(f"nmap -sV --script http-waf-detect {target}")

# القائمة الرئيسية المحدثة بالكردية السورانية والإنجليزية معاً
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print(BANNER)
        print(f" {BOLD}{CYAN}┌────────────────────────────────────────────────────────┐")
        print(f" │            تکایە ئامرازێکی گونجاو هەڵبژێرە:            │")
        print(f" └────────────────────────────────────────────────────────┘{RESET}")
        
        print(f"  {BOLD}{BLUE}[01]{RESET} Network Scanner     (پشکنینی تۆر)         {BOLD}{BLUE}[11]{RESET} Subnet Calculator  (حسابکردنی تۆر)")
        print(f"  {BOLD}{BLUE}[02]{RESET} Port Scanner        (پشکنینی پۆرت)        {BOLD}{BLUE}[12]{RESET} MAC Address Lookup (زانیاری ماک)")
        print(f"  {BOLD}{BLUE}[03]{RESET} DNS Lookup          (ئایپی سایت)          {BOLD}{BLUE}[13]{RESET} Port Banner Grab   (جۆری سێرڤەر)")
        print(f"  {BOLD}{BLUE}[04]{RESET} Ping Tester         (پشکنینی بەستەر)      {BOLD}{BLUE}[14]{RESET} Local Network Info (کارتەکانی تۆر)")
        print(f"  {BOLD}{BLUE}[05]{RESET} Whois Lookup        (زانیاری دۆمەین)      {BOLD}{BLUE}[15]{RESET} Cloudflare Bypass  (ئایپی ڕاستەقینە)")
        print(f"  {BOLD}{BLUE}[06]{RESET} Device Scanner      (پشکنینی ئامێرەکان)   {BOLD}{BLUE}[16]{RESET} Phone Info Lookup  (ژمارەی تەلەفۆن)")
        print(f"  {BOLD}{BLUE}[07]{RESET} Network Count       (ژمارەی ئامێرەکان)    {BOLD}{BLUE}[17]{RESET} Shellshock Scanner (کلاود سێرڤەر)")
        print(f"  {BOLD}{BLUE}[08]{RESET} Subdomain Scanner   (دۆمەینی لاوەکی)      {BOLD}{BLUE}[18]{RESET} Directory Bruter   (بووشایی سایت)")
        print(f"  {BOLD}{BLUE}[09]{RESET} Header Security     (پاراستنی سایت)       {BOLD}{BLUE}[19]{RESET} Email Harvester    (کۆکەرەوەی ئیمێڵ)")
        print(f"  {BOLD}{BLUE}[10]{RESET} Admin Panel Finder  (پانێڵی ئەدمین)       {BOLD}{BLUE}[20]{RESET} Firewall Detector  (دیواری ئاگرین)")
        print(f"  ─────────────────────────────────────────────────────────────────────────────────────────")
        print(f"  {BOLD}{RED}[21] Exit (دەرچوون){RESET}")
        print(f"  ─────────────────────────────────────────────────────────────────────────────────────────")
        
        choice = input(f"\n{BOLD}{CYAN} ┌─[ Kurdistan-Framework ]\n └─╼ # {RESET}").strip()
        
        funcs = {
            '1': network_scanner, '01': network_scanner, '2': port_scanner, '02': port_scanner,
            '3': dns_lookup, '03': dns_lookup, '4': ping_tester, '04': ping_tester,
            '5': whois_lookup, '05': whois_lookup, '6': device_scanner, '06': device_scanner,
            '7': network_count, '07': network_count, '8': subdomain_scanner, '08': subdomain_scanner,
            '9': header_checker, '09': header_checker, '10': admin_finder, '11': subnet_calc,
            '12': mac_lookup, '13': banner_grabbing, '14': local_info, '15': cloudflare_bypass,
            '16': phone_lookup, '17': shellshock_scan, '18': dir_bruter, '19': email_harvester,
            '20': firewall_detector
        }
        
        if choice in funcs:
            funcs[choice]()
            back_menu()
        elif choice == '21':
            print(f"{BOLD}{GREEN}\n[+] ماڵاوا! سوپاس بۆ بەکارهێنانی Kurdistan Framework {RESET}\n")
            sys.exit(0)
        else:
            print(f"{WARN} {RED}هەڵبژاردنەکە هەڵەیە!{RESET}")
            os.system('sleep 1')

if __name__ == "__main__":
    main_menu()
