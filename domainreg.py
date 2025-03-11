import whois
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

def main():
    domains = [
        "starlight.co.uk",
        "coxautoinc.eu",
        "dealer-bay.co.uk",
        "thisdomaindoesnotexistatall.fake",
        "carsandmotor.co.uk",
        "carvaluation.com"
    ]

    for domain in domains:
        registrar = get_domain_registrar(domain)
        if registrar:
            if not registrar.startswith("Error"):
                print(f"Domain: {domain} - Registrar: {registrar}")
            else:
                print(f"Domain: {domain} - {registrar}")
        else:
            print(f"Domain: {domain} - Registrar information not found.")

if __name__ == "__main__":
    main()