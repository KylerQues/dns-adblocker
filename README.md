# dns-adblocker

# DNS Ad Blocker (Python)

A simple DNS server built in Python that blocks specific domains and forwards allowed requests to a real DNS server.

## What it does

- Runs a basic DNS server using UDP
- Reads DNS requests from clients
- Extracts the requested domain
- Checks if the domain is blocked
- Returns a blocked response or forwards allowed requests to an upstream DNS server

## Features

- DNS request parsing using `dnslib`
- Simple in-memory blocklist
- Logs all DNS requests
- Blocks domains by returning `0.0.0.0`
- Includes a test client for verification
- Supports subdomain blocking
- Forwards allowed requests to upstream DNS (8.8.8.8)

## Requirements

Install dependencies:

pip install dnslib

## How To Run

Start the server:
python server.py

Run the test client:
python test_client.py