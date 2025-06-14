#!/usr/bin/python3
#Simulation for native IPv4 (Dual Stack and CGNAT)
from utils import wan_type, route, ipr, addr
import ipaddress

class native(wan_type):
    # Validate arguments
    def __new__(cls, args):
        #Validation successful
        return super().__new__(cls)

    # Init
    def __init__(self,args):
        self.iface = args.interface
        self.debug = args.debug

    def setup(self):
        # Print the gateway
        if self.debug: print(f"Native GW is {self.gw}")
        # Add address to gateway
        self.laddr = addr(self.gw,self.iface)
        # Add iptables masquerade rule
        if self.masq:
            if self.debug: print("Native IPv4 needs Masquerade")
            # TODO iptables -t nat .... add masquerade

    # Teardown DS-Lite tunnel
    def __del__(self):
        # TODO iptables -t nat ... del masquerade
        if self.debug: print("Del Native")


# Dual Stack class
class dualstack(native):
    # Validate arguments
    def __new__(cls, args):
        # DS requires either a subnet larger than 32 or fargw set
        if args.fargw is None and ipaddress.ip_interface(args.legacy).network.prefixlen >= 32:
            print("Dual Stack requires sufficient (non-/32) subnet or Far Gateway")
            return None
        #Validation successful
        return super().__new__(cls,args)

    # Init
    def __init__(self,args):
        self.masq = False
        if args.nat: self.masq = True
        if args.legacy is None:
            self.net = ipaddress.ip_interface("203.0.113.5/24")
        else:
            self.net = ipaddress.ip_interface(args.legacy)
        if args.fargw is None:
            self.gw = ipaddress.ip_interface(f"{str(self.net.network.network_address+1)}/{self.net.netmask}")
        else:
            self.gw = ipaddress.ip_interface(f"{args.fargw}/32")
        if args.debug: print(f"DualStack Net={self.net} gw={self.gw}")
        super().__init__(args)


# CGNAT Class
class cgnat(native):
    # Validate arguments
    def __new__(cls, args):
        # CGNAT requires at least a /30
        if args.cgnat is None:
            # Use defaults
            args.cgnat = ipaddress.ip_interface("10.69.96.5/20")
        else:
            args.cgnat = ipaddress.ip_interface(args.cgnat)
            if args.cgnat.network.prefixlen > 30:
                print("CGNAT requires sufficient (/30 or larger) network")
                return None
        #Validation successful
        return super().__new__(cls,args)

    # Init
    def __init__(self,args):
        self.masq = True
        self.net = args.cgnat
        self.gw = ipaddress.ip_interface(f"{str(args.cgnat.network.network_address+1)}/{self.net.netmask}")
        if args.debug: print(f"CGNAT Net={self.net} gw={self.gw}")
        super().__init__(args)
