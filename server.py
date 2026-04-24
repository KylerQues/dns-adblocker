import socket
from dnslib import DNSRecord, RR, A

port = 15353
ip = '0.0.0.0'

# Upstream DNS server
upstream_dns = ('8.8.8.8', 53)

# Create UDP socket (IPv4)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Listen on port
sock.bind((ip, port))

# Domains to block
blocked_domains = ["ads.google.com", "doubleclick.net"]

# Run server forever
while True:
    # Get DNS request
    data, addr = sock.recvfrom(512)

    try:
        # Parse DNS request
        request = DNSRecord.parse(data)

        # Get domain name
        qname = str(request.q.qname).strip('.')

        print("Request:", qname)

        # Check if blocked
        if any(blocked in qname for blocked in blocked_domains):
            print("BLOCKED")

            # Create reply
            reply = request.reply()

            # Block domain
            reply.add_answer(RR(qname, rdata=A("0.0.0.0")))

            # Send response
            sock.sendto(reply.pack(), addr)

        else:
            print("ALLOWED")

            # Forward request to upstream DNS
            sock.sendto(data, upstream_dns)

            # Get response from upstream DNS
            response_data, _ = sock.recvfrom(512)

            # Send response back to client
            sock.sendto(response_data, addr)

    except Exception as e:
        print("Error:", e)