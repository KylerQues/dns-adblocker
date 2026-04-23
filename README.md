# dns-adblocker

# DNS Ad Blocker (Python)

A simple DNS server built in Python that blocks specific domains using a blocklist.

## What it does

- Runs a basic DNS server using UDP
- Reads DNS requests from clients
- Extracts the requested domain
- Checks if the domain is blocked
- Returns a blocked response or allows it (basic response)

## Features

- DNS request parsing using `dnslib`
- Simple in-memory blocklist
- Logs all DNS requests
- Blocks domains by returning `0.0.0.0`

## Requirements

Install dependencies:

pip install dnslib

## How To Run

python server.py
