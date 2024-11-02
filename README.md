# DomainHound


This is an automated reconnaissance script for initial bug bounty or penetration testing. Subdomain Enumeration - Filtering Sensitive Subdomains - Content Discovery - Domains Screenshotting

## Features
- **Subdomain Enumeration**: Uses `subfinder` to find subdomains of a specified domain.
- **Sensitive Root Domain Identification**: Filters subdomains based on keywords (like `api`, `dev`, `prod`, etc.).
- **Domain Resolution**: Checks if domains are live with `httprobe`.
- **Content Discovery**: Uses `meg` to locate and retrieve various endpoints.
- **Screenshotting**: Captures screenshots of root domains using a specified command (like Aquatone or Eyewitness).

---

## Prerequisites

Make sure the following tools are installed:
- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [Meg](https://github.com/tomnomnom/meg)
- [Httprobe](https://github.com/tomnomnom/httprobe)
- Screenshotting tool (Aquatone, Eyewitness, or equivalent)

Use the following commands to install these tools:

```bash
# Install Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Meg
go install -v github.com/tomnomnom/meg@latest

# Install Httprobe
go install -v github.com/tomnomnom/httprobe@latest
```

## Usage

1. **Clone the Repository**

   ```bash
  git clone https://github.com/AzerSD/DomainHound.git
   cd DomainHound
   ```

2. **Run the Script**

   ```bash
   python3 DomainHound.py -d <domain> -a <screenshot_command> -w <endpoints_file>
   ```

   **Arguments**:
   - `-d, --domain`: Target domain for reconnaissance.
   - `-a, --aquatone`: Command to use for screenshotting (e.g., `aquatone` or `eyewitness`).
   - `-w, --paths`: Path to a list of endpoints to be checked during content discovery. (e.g from SecList: Discovery/Web-Content `/api/api-endpoints.txt, /common.txt, /config-files.txt, information-disclosure/php-info.txt`)

   **Example**:
   ```bash
   python3 DomainHound.py -d example.com -a "aquatone" -w endpoints.txt
   ```

## Output Structure

The script creates a `data/` directory for each target domain with the following structure:

```
data/
└── <domain>/
    ├── subdomains.txt       # All enumerated subdomains
    ├── hosts                # Sensitive root domains
    ├── hosts-resolved       # Resolved domains (live hosts)
    └── out/                 # Content discovered by meg
```

## Script Breakdown

### 1. `fetch_domains(domain)`
   - Runs `subfinder` to gather subdomains and stores them in `subdomains.txt`.

### 2. `get_roots(domain)`
   - Identifies sensitive subdomains (e.g., `api`, `prod`, `dev`) and saves them to `hosts`.

### 3. `resolve(domain)`
   - Uses `httprobe` to resolve domains from `hosts` and stores live domains in `hosts-resolved`.

### 4. `content_discovery(domain, paths)`
   - Uses `meg` to find available endpoints, based on the input `paths` list, and saves them in the `out/` directory.

### 5. `screenshot_domains(domain, command)`
   - Runs the screenshot command on the root domains for easy visualization.

## Example Workflow

1. **Find subdomains** for `example.com` and check for live ones.
2. **Filter out** sensitive root domains (e.g., dev, staging).
3. **Discover endpoints** for all live domains.
4. **Capture screenshots** of the domains.
