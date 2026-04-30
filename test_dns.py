import socket
from dnslib import DNSRecord
import time

server = ("127.0.0.1", 15353)

def query(domain):
    q = DNSRecord.question(domain)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(q.pack(), server)
    response, _ = sock.recvfrom(512)
    sock.close()
    return response

domain = "google.com"

print("First request (should MISS cache)")
query(domain)

time.sleep(1)

print("Second request (should HIT cache)")
query(domain)

print("Waiting for TTL to expire...")
time.sleep(65)

print("Third request (should MISS again)")
query(domain)