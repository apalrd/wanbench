# DHCP Server Code
from scapy.all import *
import socket
from scapy.layers.inet6 import IPv6,ICMPv6ND_RS,ICMPv6MLReport2,ICMPv6ND_NS
from utils import route, addr
import time

class dhcp_srv:
    # Validate arguments
    def __new__(cls, args):
        print("New DHCPv6 server",args)
        #Validate arguments, return None on error
        #Validation successful
        return super().__new__(cls)
    
    def __init__(self,args):
        self.iface = args.interface
        self.debug = args.debug

    def send_ra(self,dest):
        # Send periodic Router Advertisements
        print("Need to send an RA to",dest)

    def parse_rs(self,pkt):
        # Got a packet which is an RS
        # Send an RA in reponse
        self.send_ra(pkt[IPv6].src)

    def parse_dhcp4(self,pkt):
        pass

    def parse_dhcp6(self,pkt):
        pass

    def parse_pkt(self,pkt):
        if pkt.haslayer(ICMPv6ND_RS): self.parse_rs(pkt)
        #Ignore MLD reports
        elif pkt.haslayer(ICMPv6MLReport2): pass
        #Ignore NS (kernel will deal with these)
        elif pkt.haslayer(ICMPv6ND_NS): pass
        elif self.debug: print("Packet Received:",pkt)


    def setup(self,gwan:array):
        print("[+] Sniff started")
        self.sniffer = AsyncSniffer(store=0, prn=self.parse_pkt, iface=self.iface)
        self.sniffer.start()
        # Do other things, check for periodic send stuff
        time.sleep(50)

    def __del__(self):
        self.sniffer.stop()
        pass