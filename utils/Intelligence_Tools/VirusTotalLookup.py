import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("VT_API_KEY")

def query_virustotal(entity: str) -> str:
    headers = {
        "x-apikey": API_KEY
    }

    if entity.count(".") == 3 and all(part.isdigit() for part in entity.split(".")):
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{entity}"
    else:
        url = f"https://www.virustotal.com/api/v3/domains/{entity}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            total = sum(stats.values())
            return f"VirusTotal Detection:\n{stats['malicious']} malicious out of {total} engines."
        else:
            return f"VirusTotal Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"VirusTotal exception: {e}"