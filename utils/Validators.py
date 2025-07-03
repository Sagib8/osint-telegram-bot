import re


ipv4_pattern = re.compile(
    r"^((25[0-5]|(2[0-4]|1\d|0?\d)?\d)\.){3}"
    r"(25[0-5]|(2[0-4]|1\d|0?\d)?\d)$"
)

ipv6_pattern = re.compile(
    r'''^(
        ([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|
        ([0-9a-fA-F]{1,4}:){1,7}:|
        ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|
        ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|
        ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|
        ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|
        ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|
        [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|
        :((:[0-9a-fA-F]{1,4}){1,7}|:)|
        fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|
        ::(ffff(:0{1,4}){0,1}:){0,1}
        ((25[0-5]|(2[0-4]|1\d|0?\d)?\d)\.){3,3}
        (25[0-5]|(2[0-4]|1\d|0?\d)?\d)|
        ([0-9a-fA-F]{1,4}:){1,4}:
        ((25[0-5]|(2[0-4]|1\d|0?\d)?\d)\.){3,3}
        (25[0-5]|(2[0-4]|1\d|0?\d)?\d)
    )$''', re.VERBOSE | re.IGNORECASE
)

def is_ipv4(text: str) -> bool:
    return bool(ipv4_pattern.fullmatch(text))

def is_ipv6(text: str) -> bool:
    return bool(ipv6_pattern.fullmatch(text))

def is_valid_ip(text: str) -> bool:
    return is_ipv4(text) or is_ipv6(text)

DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!\-)([a-zA-Z0-9]{1,63}(-[a-zA-Z0-9]{1,63})?\.)+[a-zA-Z]{2,63}$"
)

def is_valid_domain(domain: str) -> bool:
    domain = domain.strip().lower()
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = domain.split("://", 1)[1].split("/")[0]
    return bool(DOMAIN_REGEX.fullmatch(domain))

def sanitize_entity(entity: str) -> str:
    """
    Cleans user input by removing URL schemes (http://, https://) and trailing slashes.
    Returns a clean domain or IP string.
    """
    return re.sub(r"^https?://", "", entity.strip().rstrip("/"))