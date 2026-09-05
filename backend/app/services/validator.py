from urllib.parse import urlparse
import socket
import ipaddress
from flask import request
from ..config import SUPPORTED_PRODUCT_DOMAINS


def get_json_payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def parse_number(value, name, *, positive=False, non_negative=False):
    if value is None or isinstance(value, bool):
        raise ValueError(f"{name} must be a valid number")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a valid number")
    if positive and number <= 0:
        raise ValueError(f"{name} must be positive")
    if non_negative and number < 0:
        raise ValueError(f"{name} cannot be negative")
    return number


def next_id(records):
    return max((record.get("id", 0) for record in records), default=0) + 1


def validate_external_url(url):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("A valid product URL is required")

    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only HTTP or HTTPS product URLs are supported")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not supported")

    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("Local or private network URLs are not allowed")
    if not any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in SUPPORTED_PRODUCT_DOMAINS
    ):
        raise ValueError("Only Amazon India, Flipkart and Myntra product URLs are supported")

    try:
        addresses = socket.getaddrinfo(hostname, parsed.port or 443, type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise ValueError("Product URL host could not be resolved")

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise ValueError("Local or private network URLs are not allowed")
    return url
