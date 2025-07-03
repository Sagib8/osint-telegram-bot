
import whois

def get_domain_whois(domain: str) -> str:
    """
    Fetches WHOIS information for a given domain name.

    Args:
        domain (str): The domain to look up.

    Returns:
        str: Raw WHOIS information or an error message.
    """
    try:
        result = whois.whois(domain)
        return str(result)
    except Exception as e:
        return f"WHOIS lookup failed: {e}"