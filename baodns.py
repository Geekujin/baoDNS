import requests
import json
import os

# Config file path
CONFIG_FILE = ".baocfg"


# Loads the config file
def load_config(file_path):
    config = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore empty lines and comments
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

# Get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

# Gets the current DNS record via Porkbun API
def get_dns_record(api_key, api_secret, domain, record_type, subdomain):
    url = f"https://api.porkbun.com/api/json/v3/dns/retrieveByNameType/{domain}/{record_type}/{subdomain}"
    payload = {
        "apikey": api_key,
        "secretapikey": api_secret
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["records"]
    except requests.RequestException as e:
        print(f"Error retrieving DNS records: {e}")
        # Error handling, providing further information
        if response.status_code == 403:
            print("Forbidden: Check API key or domain ownership")
        print(f"Response: {response.text}")
        return None

# Update the DNS record on the porkbun API
def update_dns_record(api_key, api_secret, domain, subdomain, record_type, ip):
    url = f"https://api.porkbun.com/api/json/v3/dns/editByNameType/{domain}/{record_type}/{subdomain}"
    payload = {
        "apikey": api_key,
        "secretapikey": api_secret,
        "type": record_type,
        "name": subdomain,
        "content": ip,
        "ttl": 300  # Time-to-live in seconds
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error updating DNS record: {e}")
    return None

def main():
    config = load_config(CONFIG_FILE)
    if not config:
        return

    # Pull info from config file and check if it is all present
    api_key = config.get("API_KEY")
    api_secret = config.get("API_SECRET")
    domain = config.get("DOMAIN")
    subdomain = config.get("SUBDOMAIN")
    record_type = config.get("RECORD_TYPE")

    if not all([api_key, api_secret, domain, record_type]):
        print("Missing required configuration values.")
        return

    # Get public IP address
    current_ip = get_public_ip()
    if not current_ip:
        return

    print(f"Your public IP address is: {current_ip}")
    print("")

    # Get the current DNS record
    records = get_dns_record(api_key, api_secret, domain, record_type, subdomain)
    if not records:
        print(f"No DNS record found for {subdomain}.{domain}!")
        print("Exiting...")
        return

    # Check if DNS is already set to the correct IP address
    record_to_update = None

    # Logic to determine if there is a subdomain
    if subdomain:
        full_record_name = f"{subdomain}.{domain}"
    else:
        full_record_name = domain

    for record in records:
        if record.get("content") == current_ip:
           print(f"{record_type} record for {full_record_name} already set to {record.get('content')}, no changes made.")
           print("Exiting...")
           return
        if record.get("name") == full_record_name:
           record_to_update = record


    # Update the record
    result = update_dns_record(api_key, api_secret, domain, subdomain, record_type, current_ip)
    if result and result.get("status") == "SUCCESS":
        print(f"{record_type} record for {full_record_name} successfully updated to {current_ip}.")
    else:
        print(f"Failed to update {record_type} record for {full_record_name}.")

if __name__ == "__main__":
    main()
