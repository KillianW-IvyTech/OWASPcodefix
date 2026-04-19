# url = input("Enter URL: ")
# response = requests.get(url)
# print(response.text)
import requests
from urllib.parse import urlparse
ALLOWED_HOSTS = {"example.com", "api.example.com"}
MAX_RESPONSE_LENGTH = 1000
def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are permitted")
    if not parsed.hostname:
        raise ValueError("URL must include a valid hostname")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host '{parsed.hostname}' is not permitted")
    return url
def fetch_url(url):
    try:
        validated = validate_url(url)
        response = requests.get(validated, timeout=(5, 10))
        response.raise_for_status()
        print(response.text[:MAX_RESPONSE_LENGTH])
    except ValueError as e:
        print(f"Invalid URL: {e}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {type(e).__name__}")
url = input("Enter URL: ")
fetch_url(url)