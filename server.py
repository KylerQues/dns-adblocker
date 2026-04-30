import socket
import logging
import time
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

# Cache: (qname, qtype) -> {response, expires_at}
cache = {}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

logging.info(f"DNS server running on {ip}:{port}")

while True:
    data, addr = sock.recvfrom(512)

    try:
        request = DNSRecord.parse(data)

        qname = str(request.q.qname).strip('.').lower()
        qtype = request.q.qtype

        cache_key = (qname, qtype)

        logging.info(f"Request from {addr[0]}: {qname} (type={qtype})")

        # ---- CACHE CHECK ----
        if cache_key in cache:
            entry = cache[cache_key]

            if time.time() < entry["expires_at"]:
                logging.info(f"Cache hit: {qname}")
                sock.sendto(entry["response"], addr)
                continue
            else:
                logging.info(f"Cache expired: {qname}")
                del cache[cache_key]

        # ---- BLOCK CHECK ----
        is_blocked = any(
            qname == blocked or qname.endswith("." + blocked)
            for blocked in blocked_domains
        )

        if is_blocked:
            logging.warning(f"Blocked: {qname}")

            reply = request.reply()

            reply.add_answer(
                RR(
                    rname=qname,
                    rtype=1,
                    rclass=1,
                    ttl=60,
                    rdata=A("0.0.0.0")
                )
            )

            packed_reply = reply.pack()

            # Cache blocked response
            cache[cache_key] = {
                "response": packed_reply,
                "expires_at": time.time() + 60
            }

            sock.sendto(packed_reply, addr)

        else:
            logging.info(f"Allowed: {qname}")

            upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            upstream_sock.settimeout(2)

            try:
                upstream_sock.sendto(data, upstream_dns)
                response_data, _ = upstream_sock.recvfrom(512)

                dns_response = DNSRecord.parse(response_data)

                # Extract TTL safely
                if dns_response.rr:
                    ttl = min([r.ttl for r in dns_response.rr])
                else:
                    ttl = 60  # fallback

                # Cache response
                cache[cache_key] = {
                    "response": response_data,
                    "expires_at": time.time() + ttl
                }

                sock.sendto(response_data, addr)

            except socket.timeout:
                logging.error("Upstream DNS timeout")

            finally:
                upstream_sock.close()

    except Exception as e:
        logging.error(f"Error: {e}")