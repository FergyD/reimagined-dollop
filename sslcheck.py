import ssl
import socket
from datetime import datetime
import requests

def get_ssl_expiry_date(url):
    try:
        # Extract the domain from the URL
        hostname = url.split("//")[-1].split("/")[0]

        # Establish an SSL context and get the certificate
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Extract expiration date and calculate remaining days
        expiry_date = cert['notAfter']
        expiry_date = datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y GMT')
        remaining_days = (expiry_date - datetime.utcnow()).days

        return remaining_days
    except Exception as e:
        return str(e)

def check_urls(url_list):
    results = {}
    for url in url_list:
        remaining_days = get_ssl_expiry_date(url)
        results[url] = remaining_days

    return results

def main(req):
    url_list = ["https://example.com", "https://anotherexample.com"]
    result = check_urls(url_list)
    
    return {
        "status": 200,
        "body": result
    }
