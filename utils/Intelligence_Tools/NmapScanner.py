import subprocess

def scan_common_ports(ip: str) -> str:
    """
    Scans 15 common TCP and UDP ports using Nmap for the given IP address.

    Args:
        ip (str): Target IP address.

    Returns:
        str: Raw output from Nmap or an error message.
    """
    # Top TCP ports
    tcp_ports = [
        21, 22, 23, 25, 53, 80, 110, 143,
        443, 445, 993, 995, 3306, 3389, 8080
    ]

    # Top UDP ports (subset of common services)
    udp_ports = [53, 67, 123, 161, 500, 1900, 69, 137, 138, 514]

    # Combine using T: and U: syntax
    port_str = f"T:{','.join(map(str, tcp_ports))},U:{','.join(map(str, udp_ports))}"

    try:
        result = subprocess.run(
            ["nmap", "-sSU", "-p", port_str, ip],
            capture_output=True,
            text=True,
            timeout=90
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Nmap error:\n{result.stderr}"
    except Exception as e:
        return f"Nmap execution failed: {e}"