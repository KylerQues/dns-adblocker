import socket
from dnslib import DNSRecord, RR, A


port = 53
ip = '0.0.0.0'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # First argument is saying we are using IPV4, and second argumenmt is for choosing UDP and not TCP
sock.bind((ip,port)) # Only takes one parameter so an extra set of brackets is needed to make these variablews a tuple

blocked_domains = ["ads.google.com", "doubleclick.net"]

while True:
    data, addr = sock.recvfrom(512) # Returns a tuple of the data then the address
    request = DNSRecord.parse(data)
    qname = str(request.q.qname).strip('.')

    print("Request:", qname)

    reply = request.reply()

    if qname in blocked_domains:
        print("BLOCKED")
        reply.add_answer(RR(qname, rdata=A("0.0.0.0")))
    else:
        print("ALLOWED")
        reply.add_answer(RR(qname, rdata=A("8.8.8.8")))

    sock.sendto(reply.pack(), addr)

