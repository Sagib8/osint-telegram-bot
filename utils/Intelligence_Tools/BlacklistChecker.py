import requests
import os

def check_blacklist(ip: str) -> str:
    """
    Checks the IP address against AbuseIPDB blacklist.

    Args:
        ip (str): The IP address to check.

    Returns:
        str: Summary of the blacklist report or error message.
    """
    API_KEY = os.getenv("ABUSEIPDB_API_KEY")
    if not API_KEY:
        return "AbuseIPDB API key is missing in environment."

    url = "https://api.abuseipdb.com/api/v2/check"
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json().get("data", {})

        if "abuseConfidenceScore" in data:
            return (
                f"Abuse Confidence Score: {data['abuseConfidenceScore']}\n"
                f"Country: {data.get('countryCode', 'N/A')}\n"
                f"ISP: {data.get('isp', 'N/A')}\n"
                f"Domain: {data.get('domain', 'N/A')}\n"
                f"Usage Type: {data.get('usageType', 'N/A')}\n"
                f"Total Reports: {data.get('totalReports', 0)}"
            )
        else:
            return "No data found or invalid IP."
    except Exception as e:
        return f"Blacklist check failed: {e}"