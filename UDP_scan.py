import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "192.168.56.2"
src_port = RandShort()
dst_port = 53
dst_timeout = 10
def udp_scan(dst_ip, dst_port, dst_timeout):
    udp_scan_resp = sr1(IP(dst=dst_ip) / UDP(dport=dst_port), timeout=dst_timeout)
    if (str(type(udp_scan_resp)) == "<type 'NoneType'>"):
        print("Open|Filtered")
    elif (udp_scan_resp.haslayer(UDP)):
        print("Open")
    elif (udp_scan_resp.haslayer(ICMP)):
        if (int(udp_scan_resp.getlayer(ICMP).type) == 3 and int(udp_scan_resp.getlayer(ICMP).code) == 3):
            print("Closed")


udp_scan(dst_ip, dst_port, dst_timeout)
