# dns-adblocker

# DNS Ad Blocker (Python)

A simple DNS server built in Python that blocks specific domains and forwards allowed requests to a real DNS server.

## What it does

- Runs a basic DNS server using UDP
- Reads DNS requests from clients
- Extracts and normalizes the requested domain (case-insensitive, removes trailing dots)
- Checks if the domain is blocked
- Returns a blocked response or forwards allowed requests to an upstream DNS server (`8.8.8.8`)
- Measures request processing time (latency)

## Features

- DNS request parsing using `dnslib`
- Simple in-memory blocklist
- Logs all DNS requests (INFO, WARNING, ERROR levels)
- Blocks domains by returning `0.0.0.0`
- Includes a test client for verification
- Supports subdomain blocking (e.g. `*.doubleclick.net`)
- Forwards allowed requests to upstream DNS (8.8.8.8)
- Uses a separate socket for upstream requests (prevents response mix-ups)
- Handles DNS edge cases (e.g. domains with no A record or non-existent domains)

## Requirements

Install dependencies:

pip install dnslib

## How To Run

Start the server:
python server.py

Run the test client:
python test_dns.py

## Example Output

Query: google.com  
Time: ~20–50 ms  
Answer: real IP addresses  

Query: ads.google.com  
Time: ~1–5 ms  
Answer: 0.0.0.0  

