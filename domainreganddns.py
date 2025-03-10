import whois
import csv
import dns.resolver
import datetime

def get_domain_registrar(domain):
    """
    Retrieves the domain registrar for a given domain.

    Args:
        domain (str): The domain name (e.g., "google.com").

    Returns:
        str or None: The registrar name or None if not found or an error occurs.
    """
    try:
        w = whois.whois(domain)
        if w.registrar:
            if isinstance(w.registrar, list): #whois returns a list sometimes.
                return w.registrar[0]
            else:
                return w.registrar
        else:
            return None #registrar not found.

    except whois.parser.PywhoisError as e:
        return f"Error: Whois parsing error - {e}"
    except whois.exceptions.UnknownTld as e:
        return f"Error: Unknown TLD - {e}"
    except whois.exceptions.FailedParsingWhoisOutput as e:
        return f"Error: Failed to parse whois output - {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_public_dns(domain):
    """
    Retrieves the public DNS servers for a given domain.

    Args:
        domain (str): The domain name (e.g., "google.com").

    Returns:
        list or str: A list of DNS servers or an error message.
    """
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, 'NS')
        dns_servers = [str(rdata.target) for rdata in answers]
        return dns_servers
    except dns.resolver.NXDOMAIN:
        return "Error: Domain does not exist."
    except dns.resolver.NoAnswer:
        return "Error: No DNS records found."
    except dns.resolver.Timeout:
        return "Error: DNS query timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    domains = [
        "google.com",
        "example.org",
        "invalidtldexample.xyz",
        "thisdomaindoesnotexistatall.fake",
        "bbc.co.uk"
    ]

    results = []

    for domain in domains:
        registrar = get_domain_registrar(domain)
        dns_servers = get_public_dns(domain)

        if isinstance(dns_servers, list):
            dns_str = ", ".join(dns_servers) #convert to a string.
        else:
            dns_str = dns_servers #if it is an error, keep the error.

        if registrar:
            results.append([domain, registrar, dns_str])
        else:
            results.append([domain, "Registrar information not found.", dns_str])

    # Export to CSV
    csv_filename = "domain_registrars_dns.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Domain", "Registrar", "DNS Servers"])  # Updated header row
        writer.writerows(results)

    print(f"Domain registrar and DNS information exported to {csv_filename}")

if __name__ == "__main__":
    main()