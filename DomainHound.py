#!/usr/bin/python3
import os
import argparse
import time

# These are sensitive root domain patterns
arr = [
    "api", "corp", "dev", "uat", "test", "stag", "sandbox", "prod", "internal", 
    "admin", "portal", "secure", "support", "help", "auth", "account", 
    "qa", "staging", "beta", "prod", "preprod", "services", "payments", 
    "backend", "assets", "legacy", "archive", "upload", "download", "file", 
    "client", "customer", "partner", "static", "resources", "v1", "v2", 
    "edge", "mobile", "cdn", "config", "docker", "k8s", "kubernetes", "demo"
]

# Content Discovery using (meg)
def content_discovery(domain, paths):
    print(f"\n[>] Using Meg to find endpoints for {domain}...\n")
    os.system(f"meg -v -c 2 {paths} data/{domain}/hosts-resolved data/{domain}/out")
    os.chdir(f"data/{domain}")
    os.system(f"grep -Hrie '200 OK' | grep -v 'HTTP/1.1' | awk '{{print $2}}' >> data/{domain}/hosts-resolved")
    os.chdir("../../")

# Screenshot the root domains
def screenshot_domains(domain, command):
    print(f"\n[>] Screenshotting root domains for {domain}...\n")
    os.system(f"cat data/{domain}/hosts-resolved | {command}")

def fetch_domains(domain):
    os.system(f"subfinder -d {domain} -o data/{domain}/subdomains.txt --silent -t 100")
    print("\n")

def resolve(domain):
    os.system(f"cat data/{domain}/hosts | httprobe -c 80 | tee -a data/{domain}/hosts-resolved")

def get_roots(domain):
    doms = []
    print(f"---------------# Interesting Domains for {domain} #---------------------\n")
    with open(f"data/{domain}/subdomains.txt", 'r') as domainf:
        domains = domainf.readlines()
        for subdomain in domains:
            for pattern in arr:
                if pattern in subdomain:
                    print(f"[>] {subdomain.strip()}")
                    doms.append(subdomain)
    with open(f"data/{domain}/hosts", 'w') as s:
        s.writelines(doms)
    print(f"\n[+] Found {len(doms)} Domains for {domain}")
    print("------------------------------------------------------")
    time.sleep(2)
    print("\n[>] Resolving the domains\n")
    resolve(domain)

print("""

 /$$$$$$$                                    /$$          
| $$__  $$                                  |__/          
| $$  \\ $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$ /$$$$$$$ 
| $$  | $$ /$$__  $$| $$_  $$_  $$ |____  $$| $$| $$__  $$
| $$  | $$| $$  \\ $$| $$ \\ $$ \\ $$  /$$$$$$$| $$| $$  \\ $$
| $$  | $$| $$  | $$| $$ | $$ | $$ /$$__  $$| $$| $$  | $$
| $$$$$$$/|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$| $$  | $$
|_______/  \\______/ |__/ |__/ |__/ \\_______/|__/|__/  |__/
                                                          
                                                          
                                                          
 /$$   /$$                                     /$$        
| $$  | $$                                    | $$        
| $$  | $$  /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$$        
| $$$$$$$$ /$$__  $$| $$  | $$| $$__  $$ /$$__  $$        
| $$__  $$| $$  \\ $$| $$  | $$| $$  \\ $$| $$  | $$        
| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$        
| $$  | $$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$        
|__/  |__/ \\______/  \\______/ |__/  |__/ \\_______/        
                                                                                                                                                                
""")

# Parse arguments
argparser = argparse.ArgumentParser(description='Find root domains')
argparser.add_argument('-d', '--domain', help="A single domain")
argparser.add_argument('-f', '--file', help="File containing list of domains")
argparser.add_argument('-a', '--aquatone', help="The Aquatone command", required=True)
argparser.add_argument('-w', '--paths', help='The list of endpoints to discover', required=True)
args = argparser.parse_args()

if args.file:
    # Clean the domains file to ensure it only contains valid domains
    os.system(f"cat {args.file} | sed 's/^\\*\\.\\?//' | sed 's|https\\?://||' | sed 's|/.*||' | grep -v '^#' | grep -v '^$' | sort -u > cleaned_domains.txt")
    with open("cleaned_domains.txt", 'r') as file:
        domains = [line.strip() for line in file.readlines()]
elif args.domain:
    domains = [args.domain]
else:
    print("Please provide either a single domain or a file with domains.")
    exit(1)

# Run recon for each domain
for domain in domains:
    os.makedirs(f"data/{domain}", exist_ok=True)
    time.sleep(2)

    print(f"\n[>] Finding Root Domains for {domain}...\n")

    # Fetch the domains using subfinder
    fetch_domains(domain)

    # Get sensitive domains
    get_roots(domain)

    # Discover content
    content_discovery(domain, args.paths)

    # Screenshot the root domains
    screenshot_domains(domain, args.aquatone)

