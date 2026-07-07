#!/usr/bin/env python3
from scapy.all import IP, TCP, send

src_ip = "127.0.0.1"
dst_ip = "127.0.0.1"
dport = 12345
message = "Dear Steel Cat! This is no attack, it's my humster Pinkie you should track"

pkt = IP(src=src_ip, dst=dst_ip) / TCP(sport=12345, dport=dport, flags="PA") / message
send(pkt, iface="Npcap Loopback Adapter")
print("Сообщение отправлено.")