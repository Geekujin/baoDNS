# baoDNS
Update IP address of domain name via [Porkbun API](https://porkbun.com/api/json/v3/documentation).


A python script that checks your current IPv4 address, and updates your domain and/or subdomain registered with Porkbun.com via their API. I have no idea if anyone other than me will find this useful, but I needed an easy way to update the DNS records of my domain name as it's used as a dynamic DNS address for my home server. 

This is my first foray into Python, and this script was almost a solution looking for a problem 😀

## Usage

Add your [API keys](https://porkbun.com/account/api), domain name, record type and optionally subdomain to the **.baocfg** file. As this file will contain your API keys ensure that the file is secured to prevent unauthorised access.

Once configured, ensure that the **.baocfg** file is in the same folder as the baodns.py script, or edit line 6 `CONFIG_FILE = .baocfg` to point to your preferred config file.

File can then be run using `python3 baodns.py`

## Possible future enhancements
- Get the public IP via Porkbun API instead of using a 3rd party tool.
- Separate API Key and DNS records into separate files.
- Allow specifying different config files at the command line.
- Ability to add or delete DNS records via command line or config files.


(cute Baobun image via [Vecteezy.com](https://vecteezy.com)
