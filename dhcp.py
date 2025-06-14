# DHCP Server Code
from scapy.all import *
import socket

class dhcp_srv:
    # Validate arguments
    def __new__(cls, args):
        print("New DHCPv6 server",args)
        #Validate arguments, return None on error
        #Validation successful
        return super().__new__(cls)
    
    def __init__(self,args):
        self.interface = args.interface

    def send_ra(self):
        # Send periodic Router Advertisements
        pass

    def setup(self,gwan:array):
        # Bind to IPv4 broadcast and IPv6 DHCPv6 multicast

        print("[+] Sniff started")
        sniff(store=0, prn=self.printer, iface=self.interface)

    def printer(self,packet):
        print("Packet Received:",packet)

    def __del__(self):
        pass