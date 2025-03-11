import ssl
import socket
from datetime import datetime
import urllib.parse

def get_ssl_expiry_date(url):
    """
    Checks the SSL certificate expiry date of a URL.

    Args:
        url (str): The URL to check.

    Returns:
        datetime or str: The expiry date as a datetime object, or an error message as a string.
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme != 'https':
            return f"Error: URL scheme is not HTTPS - {url}"
        hostname = parsed_url.netloc
        port = 443  # Default HTTPS port

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock: #added timeout.
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expiry_timestamp = ssl.cert_time_to_seconds(cert['notAfter'])
        expiry_date = datetime.fromtimestamp(expiry_timestamp)
        return expiry_date

    except socket.gaierror:
        return f"Error: Could not resolve hostname - {url}"
    except ConnectionRefusedError:
        return f"Error: Connection refused - {url}"
    except ssl.SSLError as e:
        if "self signed certificate" in str(e):
            return f"SSL Error: Self-signed certificate - {url}"
        return f"SSL Error: {e} - {url}"
    except Exception as e:
        return f"An unexpected error occurred: {e} - {url}"

while True:
    url_to_check = input("Enter the URL to check (e.g., https://www.google.com) or type 'exit' to quit: ")

    if url_to_check.lower() == 'exit':
        break  # Exit the loop if the user enters 'exit'

    expiry_result = get_ssl_expiry_date(url_to_check)

    if isinstance(expiry_result, datetime):
        print(f"URL: {url_to_check} - SSL Expiry: {expiry_result.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"URL: {url_to_check} - {expiry_result}")
    print("-" * 20) #add a seperator.
