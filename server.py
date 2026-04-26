import socket
import logging
from dnslib import DNSRecord, RR, A

port = 15353
ip = '0.0.0.0'

# Upstream DNS server
upstream_dns = ('8.8.8.8', 53)

# Create UDP socket (IPv4)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

# Domains to block
blocked_domains = ["ads.google.com", "doubleclick.net"]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

logging.info(f"DNS server running on {ip}:{port}")

while True:
    # Get DNS request
    data, addr = sock.recvfrom(512)

    try:
        # Parse DNS request
        request = DNSRecord.parse(data)

        # Normalize domain
        qname = str(request.q.qname).strip('.').lower()

        logging.info(f"Request from {addr[0]}: {qname}")

        # Improved block matching
        is_blocked = any(
            qname == blocked or qname.endswith("." + blocked)
            for blocked in blocked_domains
        )

        if is_blocked:
            logging.warning(f"Blocked: {qname}")

            reply = request.reply()

            # Improved response record
            reply.add_answer(
                RR(
                    rname=qname,
                    rtype=1,
                    rclass=1,
                    ttl=60,
                    rdata=A("0.0.0.0")
                )
            )

            sock.sendto(reply.pack(), addr)

        else:
            logging.info(f"Allowed: {qname}")

            # Separate socket for upstream 
            upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            upstream_sock.settimeout(2)

            try:
                upstream_sock.sendto(data, upstream_dns)
                response_data, _ = upstream_sock.recvfrom(512)

                sock.sendto(response_data, addr)

            except socket.timeout:
                logging.error("Upstream DNS timeout")

            finally:
                upstream_sock.close()

    except Exception as e:
        logging.error(f"Error: {e}")