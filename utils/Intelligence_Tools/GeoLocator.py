import requests

def get_geolocation(ip: str) -> str:
    """
    Retrieves geolocation data for the given IP using ip-api.com.
    
    Args:
        ip (str): IP address to look up.
    
    Returns:
        str: Formatted geolocation info or error message.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,query,status,message")
        data = response.json()

        if data["status"] == "success":
            return (
                f"IP: {data['query']}\n"
                f"Country: {data['country']}\n"
                f"Region: {data['regionName']}\n"
                f"City: {data['city']}\n"
                f"ISP: {data['isp']}"
            )
        else:
            return f"Geolocation lookup failed: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Geolocation error: {e}"