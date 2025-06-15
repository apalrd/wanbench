#!/usr/bin/python3
#Simulation for 464xlat
from utils import wan_type, route, ipr, addr
import ipaddress


class xlat464(wan_type):
    # Validate arguments
    def __new__(cls, args):
        # Validate that it is an IP
        if args.aftr is not None:
            try:
                ipaddress.ip_address(args.aftr)
            except:
                return None
        #Validation successful
        return super().__new__(cls)

    # Init DS-Lite object from args
    def __init__(self,args):
        self.debug = args.debug
        self.iface = args.interface
        #Validate arguments, return None on error
        if args.aftr is None:
            self.aftr = ipaddress.ip_address("2001:db8:d00d::")
        else:
            self.aftr = ipaddress.ip_address(args.aftr)
        if self.debug: print(f"DS-Lite AFTR IP is {self.aftr}")

    def setup(self):
        # Set DS-Lite AFTR IP on lo
        self.aftr_lo = addr(self.aftr,"lo")
        # Add DS-Lite tunnel with outer IP of client's IP / AFTR IP
        self.aftr_if = "dslite0"
        # Add IPv4 to tunnel iface 
        self.aftr_v4 = addr("192.0.0.1",self.aftr_if)
        if self.debug: print("In DS-Lite setup")

    # Teardown DS-Lite tunnel
    def __del__(self):
        print("Del DS-Lite")