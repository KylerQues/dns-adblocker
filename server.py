import socket
from dnslib import DNSRecord, RR, A

port = 53
ip = '0.0.0.0'

# Create UDP socket (IPv4)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Listen on port 53
sock.bind((ip, port))

# Domains to block
blocked_domains = ["ads.google.com", "doubleclick.net"]

# Run server forever
while True:
    # Get DNS request
    data, addr = sock.recvfrom(512)

    # Parse DNS request
    request = DNSRecord.parse(data)

    # Get domain name
    qname = str(request.q.qname).strip('.')

    print("Request:", qname)

    # Create reply
    reply = request.reply()

    # Check if blocked
    if qname in blocked_domains:
        print("BLOCKED")

        # Block domain
        reply.add_answer(RR(qname, rdata=A("0.0.0.0")))
    else:
        print("ALLOWED")

        # Allow (placeholder response)
        reply.add_answer(RR(qname, rdata=A("8.8.8.8")))

    # Send response
    sock.sendto(reply.pack(), addr)