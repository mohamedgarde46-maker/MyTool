#!/usr/bin/python3
import os
import sys
import socket
import subprocess
import urllib.request
import json

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

# علامات بصرية لتجميل المخرجات
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
{RESET}{BOLD}{CYAN}  ⚡ Kurdistan Multi-Tool Framework v2.5 | By Mohamedgarde46-Maker ⚡
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
    ip_range = input(f" {INFO} Enter IP Range (e.g., 192.168.1.1/24): ").strip()
    if not ip_range: return
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
    print_header("DNS Lookup", "دۆزینەوەی ناونیشانی ئایپی")
    domain = input(f" {INFO} Enter Domain Name (e.g., google.com): ").strip()
    if not domain: return
    try: print(f"{SUCC} IP for {domain} is: {BOLD}{GREEN}{socket.gethostbyname(domain)}{RESET}")
    except: print(f"{ERR} نەتوانرا ئایپی بدۆزرێتەوە!")

# 4. Ping Tester
def ping_tester():
    print_header("Ping Tester", "پشکنینی بەستەر")
    host = input(f" {INFO} Enter Target IP/Domain: ").strip()
    if not host: return
    print(f"{INFO} Sending packets...")
    if os.system(f"ping -c 4 {host}") == 0: print(f"\n{SUCC} ئامێرەکە سەر هێڵە ومەبەست بەردەستە")
    else: print(f"\n{ERR} ئامێرەکە دەرەوەی هێڵە!")

# 5. Whois Lookup
def whois_lookup():
    print_header("Whois Lookup", "زانیاری دەربارەی دۆمەین")
    domain = input(f" {INFO} Enter Domain Name: ").strip()
    if not domain: return
    print(f"{SUCC} Fetching domain details:\n")
    os.system(f"whois {domain} | grep -E 'Domain Name|Registrar|Creation Date|Expir'")

# 6. Device Scanner
def device_scanner():
    print_header("Device Scanner", "پشکنینی ئامێرەکان")
    target = input(f" {INFO} Enter Target IP: ").strip()
    if not target: return
    print(f"{SUCC} خەریکی پشکنینی قووڵی ئامێرەکەم...\n")
    os.system(f"nmap -F {target}")

# 7. Network Count
def network_count():
    print_header("Network Count", "ژمارەی ئامێرەکان لەسەر تۆڕ")
    print(f"{INFO} Scanning network devices...\n")
    output = subprocess.check_output("arp-scan --localnet 2>/dev/null || arp-scan -l", shell=True).decode()
    print(output)
    devices_count = sum(1 for line in output.split('\n') if any(char.isdigit() for char in line) and ":" in line and "Interface" not in line and "responded" not in line)
    print(f"{BLUE}="*40)
    print(f"{SUCC} ژمارەی ئامێرەکان لەسەر تۆڕەکە: [ {BOLD}{YELLOW}{devices_count}{RESET} ] ئامێر")
    print(f"{BLUE}="*40)

# 8. Subdomain Scanner
def subdomain_scanner():
    print_header("Subdomain Scanner", "پشکنینی دۆمەینی لاوەکی")
    domain = input(f" {INFO} Enter Domain: ").strip()
    if not domain: return
    subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'cpanel', 'test', 'dev']
    print(f"{INFO} Scanning subdomains for {domain}...\n")
    for sub in subdomains:
        sub_host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(sub_host)
            print(f" {SUCC} Found: {BOLD}{CYAN}{sub_host:<20}{RESET} -> {GREEN}{ip}{RESET}")
        except: pass

# 9. Header Security Checker
def header_checker():
    print_header("Header Security", "پاراستنی سایت")
    url = input(f" {INFO} Enter URL (e.g., http://example.com): ").strip()
    if not url.startswith("http"): url = "http://" + url
    try:
        req = urllib.request.urlopen(url)
        headers = req.info()
        print(f"\n{SUCC} Security Headers Check for {url}:")
        for h in ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']:
            if h in headers: print(f"  {GREEN}[SAFE]{RESET} {h}: {headers[h]}")
            else: print(f"  {RED}[VULN]{RESET} {h} is Missing!")
    except Exception as e: print(f"{ERR} Error: {e}")

# 10. Admin Panel Finder
def admin_finder():
    print_header("Admin Finder", "پانێڵی ئەدمین")
    url = input(f" {INFO} Enter Target URL: ").strip()
    if not url.startswith("http"): url = "http://" + url
    panels = ['/admin', '/login', '/admin.php', '/wp-admin', '/admin/', '/administrator']
    print(f"{INFO} Checking admin pages...\n")
    for p in panels:
        try:
            req = urllib.request.Request(url+p, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            if res.code == 200: print(f" {SUCC} Admin Page Found: {BOLD}{GREEN}{url+p}{RESET}")
        except: pass

# 11. Subnet Calculator
def subnet_calc():
    print_header("Subnet Calc", "حسابکردنی تۆر")
    ip = input(f" {INFO} Enter IP (e.g., 192.168.1.50): ").strip()
    if not ip: return
    parts = ip.split('.')
    if len(parts) == 4:
        print(f"\n {SUCC} Network IP:   {BOLD}{WHITE}{parts[0]}.{parts[1]}.{parts[2]}.0{RESET}")
        print(f" {SUCC} Gateway IP:   {BOLD}{WHITE}{parts[0]}.{parts[1]}.{parts[2]}.1{RESET}")
        print(f" {SUCC} Broadcast IP: {BOLD}{WHITE}{parts[0]}.{parts[1]}.{parts[2]}.255{RESET}")
        print(f" {SUCC} Subnet Mask:  {BOLD}{WHITE}255.255.255.0{RESET}")

# 12. MAC Address Lookup
def mac_lookup():
    print_header("MAC Lookup", "ماک ئەدرەس")
    mac = input(f" {INFO} Enter MAC Address: ").strip()
    if not mac: return
    try:
        url = f"https://api.macvendors.com/{mac}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        vendor = urllib.request.urlopen(req).read().decode()
        print(f"\n{SUCC} Manufacturer Vendor: {BOLD}{GREEN}{vendor}{RESET}")
    except: print(f"{ERR} MAC not found or API Limit reached.")

## 13. Port Banner Grabbing (مصححة ومضمونة ضد الضغط بالخطأ)
def banner_grabbing():
    print_header("Banner Grabbing", "جۆری سێرڤەر")
    target = input(f" {INFO} Enter IP/Domain: ").strip()
    if not target: return
    
    port_input = input(f" {INFO} Enter Port (Default is 80): ").strip()
    
    # ⚠️ إذا ضغطت Enter بدون كتابة شيء، سيختار تلقائياً بورت 80 ولن ينهار البرنامج
    if not port_input:
        port = 80
    else:
        try:
            port = int(port_input)
        except ValueError:
            print(f"{ERR} {RED}Error: البورت يجب أن يكون رقماً فقط!{RESET}")
            return

    try:
        s = socket.socket()
        s.settimeout(2.0)
        s.connect((socket.gethostbyname(target), port))
        if port == 80 or port == 8080:
            s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        print(f"\n{SUCC} Server Response:\n{CYAN}{banner}{RESET}")
    except Exception as e: 
        print(f"{ERR} Could not grab banner: {e}")

# 14. Local Network Info
def local_info():
    print_header("Local Info", "کارتەکانی تۆر")
    hostname = socket.gethostname()
    print(f" {SUCC} Hostname:     {BOLD}{WHITE}{hostname}{RESET}")
    print(f" {SUCC} Internal IP:  {BOLD}{WHITE}{socket.gethostbyname(hostname)}{RESET}")
    try:
        ext_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
        print(f" {SUCC} External IP:  {BOLD}{GREEN}{ext_ip}{RESET}")
    except: pass
    print(f"\n{BOLD}{MAGENTA}[*] Active Network Interfaces:{RESET}")
    os.system("ip -br address")

# القائمة الرئيسية المنسقة بشكل خلاب
def main_menu():
    check_root()
    while True:
        os.system('clear')
        print(BANNER)
        print(f" {BOLD}{CYAN}┌────────────────────────────────────────┐{RESET}")
        print(f" {BOLD}{CYAN}│       تکایە ئامرازێک هەڵبژێرە:         │{RESET}")
        print(f" {BOLD}{CYAN}└────────────────────────────────────────┘{RESET}")
        
        # طباعة الخيارات على شكل جدول منظم ثنائي الأعمدة
        print(f"  {BOLD}{BLUE}[01]{RESET} Network Scanner      {BOLD}{BLUE}[08]{RESET} Subdomain Scanner")
        print(f"  {BOLD}{BLUE}[02]{RESET} Port Scanner         {BOLD}{BLUE}[09]{RESET} Header Security")
        print(f"  {BOLD}{BLUE}[03]{RESET} DNS Lookup          {BOLD}{BLUE}[10]{RESET} Admin Finder")
        print(f"  {BOLD}{BLUE}[04]{RESET} Ping Tester          {BOLD}{BLUE}[11]{RESET} Subnet Calc")
        print(f"  {BOLD}{BLUE}[05]{RESET} Whois Lookup         {BOLD}{BLUE}[12]{RESET} MAC Lookup")
        print(f"  {BOLD}{BLUE}[06]{RESET} Device Scanner       {BOLD}{BLUE}[13]{RESET} Banner Grabbing")
        print(f"  {BOLD}{BLUE}[07]{RESET} Network Count        {BOLD}{BLUE}[14]{RESET} Local Network Info")
        print(f"  ────────────────────────────────────────────────────────")
        print(f"  {BOLD}{RED}[15] Exit (دەرچوون){RESET}")
        print(f"  ────────────────────────────────────────────────────────")
        
        choice = input(f"\n{BOLD}{CYAN} ┌─[ Kurdistan-Framework ]\n └─╼ # {RESET}").strip()
        
        funcs = {
            '1': network_scanner, '01': network_scanner,
            '2': port_scanner, '02': port_scanner,
            '3': dns_lookup, '03': dns_lookup,
            '4': ping_tester, '04': ping_tester,
            '5': whois_lookup, '05': whois_lookup,
            '6': device_scanner, '06': device_scanner,
            '7': network_count, '07': network_count,
            '8': subdomain_scanner, '08': subdomain_scanner,
            '9': header_checker, '09': header_checker,
            '10': admin_finder,
            '11': subnet_calc,
            '12': mac_lookup,
            '13': banner_grabbing,
            '14': local_info
        }
        
        if choice in funcs:
            funcs[choice]()
            back_menu()
        elif choice == '15':
            print(f"{BOLD}{GREEN}\n[+] ماڵاوا! سوپاس بۆ بەکارهێنانی ئامرازەکە {RESET}\n")
            sys.exit(0)
        else:
            print(f"{WARN} {RED}هەڵبژاردنەکە هەڵەیە!{RESET}")
            os.system('sleep 1')

if __name__ == "__main__":
    main_menu()
