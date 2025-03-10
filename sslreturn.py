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
        hostname = parsed_url.netloc
        port = 443  # Default HTTPS port

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expiry_timestamp = ssl.cert_time_to_seconds(cert['notAfter'])
        expiry_date = datetime.fromtimestamp(expiry_timestamp)
        return expiry_date

  #  except urllib.parse.ParseError:
   #     return f"Error: Invalid URL format - {url}"
    except socket.gaierror:
        return f"Error: Could not resolve hostname - {url}"
    except ConnectionRefusedError:
        return f"Error: Connection refused - {url}"
    except ssl.SSLError as e:
        return f"SSL Error: {e} - {url}"
    except Exception as e:
        return f"An unexpected error occurred: {e} - {url}"
    #except Exception as e:
     #   return f"an error has occured: {e} - {url}"

def check_urls_ssl_expiry(urls):
    """
    Checks the SSL expiry dates for a list of URLs.

    Args:
        urls (list): A list of URLs to check.
    Returns:
        dict: A dictionary of urls and their expiry dates or error messages.

    """
    results = {}
    for url in urls:
        results[url] = get_ssl_expiry_date(url)
    return results

# Example Usage:
urls_to_check = [
    "https://www.google.com",
    "https://www.example.com",
    "https://expired.badssl.com", #example of an expired certificate
    "invalid_url",
    "https://doesnotexist.example.com",
    "https://self-signed.badssl.com" #example of a self signed certificate.
]

expiry_results = check_urls_ssl_expiry(urls_to_check)

for url, result in expiry_results.items():
    if isinstance(result, datetime):
        print(f"URL: {url} - SSL Expiry: {result.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"URL: {url} - {result}")
        #print(f"URL: {url} - Error")