# DHCPv6 Server Code
from scapy.layers import dhcp6

class dhcp_srv:
    # Validate arguments
    def __new__(cls, args):
        print("New DHCPv6 server",args)
        #Validate arguments, return None on error
        #Validation successful
        return super().__new__(cls)
    
    def __init__(self):
        pass

    def setup(self):
        pass

    def __del__(self):
        pass