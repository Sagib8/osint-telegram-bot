from utils.Intelligence_Tools.NmapScanner import scan_common_ports
from utils.Validators import is_valid_ip, is_valid_domain
from utils.Intelligence_Tools.GeoLocator import get_geolocation
from utils.Intelligence_Tools.WhoisLookup import get_domain_whois
from utils.Intelligence_Tools.BlacklistChecker import check_blacklist
from utils.Intelligence_Tools.VirusTotalLookup import query_virustotal

def analyze_entity(entity: str, resolved_ip: str = None) -> dict:
    results = {}

    # If input is a domain – collect domain-related intelligence
    if is_valid_domain(entity):
        print(f"[Intelligence] WHOIS for {entity}")
        results["WHOIS"] = get_domain_whois(entity)

        print(f"[Intelligence] Blacklist check for domain {entity}")
        results["Blacklist Status"] = {
            # Check domain reputation on VirusTotal and AbuseIPDB
            "VirusTotal": query_virustotal(entity),
            "AbuseIPDB": check_blacklist(entity)
        }

    # If we have a valid IP (resolved from domain or given directly)
    if resolved_ip and is_valid_ip(resolved_ip):
        print(f"[Intelligence] Nmap on {resolved_ip}")
        results["Open Ports"] = scan_common_ports(resolved_ip)

        print(f"[Intelligence] Geo for {resolved_ip}")
        results["Geolocation"] = get_geolocation(resolved_ip)

        print(f"[Intelligence] Blacklist check for IP {resolved_ip}")
        # Merge IP blacklist results into existing section or create it
        results.setdefault("Blacklist Status", {})["VirusTotal"] = query_virustotal(resolved_ip)
        results["Blacklist Status"]["AbuseIPDB"] = check_blacklist(resolved_ip)

    return results