from pyroute2 import IPRoute
import ipaddress

ipr = IPRoute()

# Route creation class
# Create a route (string) to destination oif (string)
# Automatically clean up on deletion
class route:
    def __init__(self, route: str,oif:str):
        self.route = ipaddress.ip_network(route)
        self.active = True
        try:
            ipr.route("add", dst=str(self.route), oif=ipr.link_lookup(ifname=oif)[0])            
        except Exception as e:
            print(f"Failed to add route to {self.route} dev {oif}: {e}")
            self.active = False

    def __del__(self):
        if self.active:
            try:
                ipr.route("del", dst=str(self.route))
            except Exception as e:
                print(f"Failed to remove route to {self.route}: {e}")


# Address creation class
# Add an address (string) on the output interface (String)
# In CIDR notation
# Implicitly adds on-link route
# Automatically clean up on deletion
class addr:
    def __init__(self, addr: str,oif:str):
        self.addr = ipaddress.ip_interface(addr)
        self.oif = oif
        self.active = True
        try:
            ipr.addr("add",address=str(self.addr), index=ipr.link_lookup(ifname=oif)[0])            
        except Exception as e:
            print(f"Failed to add address {str(self.addr)} dev {oif}: {e}")
            self.active = False

    def __del__(self):
        if self.active:
            try:
                ipr.addr("del",address=str(self.addr),index=ipr.link_lookup(ifname=self.oif)[0])
            except Exception as e:
                print(f"Failed to remove address {str(self.addr)}: {e}")


# Virtual class for each wan type
class wan_type:
    def __init__(self):
        pass
    def setup(self):
        pass
    def __del__(self):
        pass