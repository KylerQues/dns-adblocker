import socket
import time
from dnslib import DNSRecord

# DNS server address (your local server)
server = ("127.0.0.1", 15353)

def send_query(domain):
    # Build a DNS query for the given domain
    query = DNSRecord.question(domain)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set timeout so it doesn't hang forever
    sock.settimeout(2)

    try:
        # Start timing
        start = time.time()

        # Send DNS request to your server
        sock.sendto(query.pack(), server)

        # Receive response from server
        data, _ = sock.recvfrom(512)

        # End timing
        end = time.time()

        # Parse DNS response
        response = DNSRecord.parse(data)

        # Print query info
        print(f"\nQuery: {domain}")

        # Print how long the request took (in milliseconds)
        print(f"Time: {(end - start) * 1000:.2f} ms")

        # Print answers from DNS response
        if response.rr:
            for answer in response.rr:
                print("Answer:", answer.rdata)
        else:
            print("No answer received")

    except socket.timeout:
        # Handle timeout case
        print(f"\nQuery: {domain}")
        print("Request timed out")

    finally:
        # Always close the socket
        sock.close()


# Run test queries immediately
send_query("google.com")             # should be ALLOWED
send_query("ads.google.com")         # should be BLOCKED
send_query("test.doubleclick.net")   # should be BLOCKED
send_query("notgoogleads.com")       # should be ALLOWED