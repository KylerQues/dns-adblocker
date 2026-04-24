import socket
from dnslib import DNSRecord

server = ("127.0.0.1", 15353)

def send_query(domain):
    # Build DNS query using dnslib (cleaner than raw hex)
    query = DNSRecord.question(domain)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send request
    sock.sendto(query.pack(), server)

    # Receive response
    data, _ = sock.recvfrom(512)

    # Parse response
    response = DNSRecord.parse(data)

    print(f"\nQuery: {domain}")

    # Print answers
    if response.rr:
        for answer in response.rr:
            print("Answer:", answer.rdata)
    else:
        print("No answer received")

# Test domains
send_query("google.com")          # should be ALLOWED
send_query("ads.google.com")     # should be BLOCKED
send_query("test.doubleclick.net")  # should be BLOCKED