#!/usr/bin/python3
# Setup simulated WAN interfaces (including DHCPv6)
import os
import argparse
from pyroute2 import IPRoute
import ipaddress
import atexit
import dslite
from native import dualstack, cgnat
from utils import wan_type,route,ipr
from dhcp import dhcp_srv

# Main
parser = argparse.ArgumentParser(prog='wanbench',description='A tool for setting up simulated WAN interfaces for router testing')
parser.add_argument("-i","--interface",help="Linux device name to simulate WAN connectivity")
parser.add_argument("-m","--mtu",help="Downstream interface MTU (default 1500)")
parser.add_argument("-t","--type",help="Type of interface to simulate",action="append")
parser.add_argument("-d","--debug",help="Print out debug information",action="store_true")
parser.add_argument("-p","--prefix",help="Prefix for simulated ISP from which DHCPv6-PD allocation to the client will be generated")
parser.add_argument("-s","--size",help="Prefix size to delegate to the client")
parser.add_argument("-g","--onlink",help="On-link prefix (CIDR notation)")
parser.add_argument("-l","--legacy",help="Legacy global address")
parser.add_argument("-n","--nat",help="Perform NAT44/NAT66 to global addresses",action="store_true")
parser.add_argument("-r","--reuse",help="Reuse factor for A+P Routing")
parser.add_argument("--fargw",help="Far Gateway Address for DHCPv4")
parser.add_argument("--aftr",help="Address of the DSLite AFTR function")
parser.add_argument("--cgnat",help="CGNAT prefix to use")
parser.add_argument("--mapinv",help="For MAP, the number of invalid/unallocated ports")
parser.add_argument("--pref64",help="For 464xlat, RFC6052 translation prefix")
parser.add_argument("--dmr",help="For MAP-T, RFC6052 translation prefix")
parser.add_argument("--index",help="For MAP-E and MAP-T, the subscriber's index in the FMR rule")
args = parser.parse_args()

# Globals
gwan = []
will_exit = False

# Validate MTU
if args.mtu is None:
    args.mtu = 1500

# Validate Prefix
if args.prefix is None:
    args.prefix = ipaddress.ip_network("2001:db8::/32")
    print("Global IPv6 prefix not specified, simulating with 2001:db8::/32 and NAT66")
else:
    args.prefix = ipaddress.ip_network(args.prefix)
    if(args.prefix.prefixlen > 64):
        print(f"Prefix length {args.prefix.prefixlen} is not at least 1 subnet")
        will_exit = True

if args.mapinv is None: args.mapinv = "1024"
if args.pref64 is None: args.pref64 = "64:ff9b::/96"
if args.dmr is None: args.dmr = "2001:db8:6464::/64"

# Validate Size
if args.size is None:
    args.size = 56
elif not args.size.isnumeric():
    print(f"Size {args.size} is invalid")
elif args.size > 64:
    print(f"Size {args.size} is not at least 1 subnet")

# Validate Reuse
if args.reuse is None:
    args.reuse = 8
# TODO must be power of two

# Validate interface
if args.interface is None:
    will_exit = True
    print("Missing required argument Interface")
else:
    #Validate interface exists
    oif=ipr.link_lookup(ifname=args.interface)
    if len(oif) < 1 or oif[0] is None:
        print("Invalid interface",args.interface)
    else:
        # Take interface down (to start)
        ipr.link('set', index=oif[0], state='down')

# Validate type
if args.type is None:
    will_exit = True
    print("Missing required argument Type")
else:
    # Check if we have invalid combinations

    if "dualstack" in args.type:
        print("Type DualStack")
        args.type.remove("dualstack")
        gwan.append(dualstack(args))
        if "cgnat" in args.type:
            print("Cannot have both Dual-Stack and CGNAT, removing CGNAT")
            args.type.remove("cgnat")
    if "cgnat" in args.type:
        print("Type CGNAT")
        args.type.remove("cgnat")
        gwan.append(cgnat(args))
    if "dslite" in args.type:
        print("Type DS-Lite")
        args.type.remove("dslite")
        gwan.append(dslite.dslite(args))
    if "lw4o6" in args.type:
        print("Type Lightweight4over6")
        args.type.remove("lw4o6")
    if "mape" in args.type:
        print("Type MAP-E")
        args.type.remove("mape")
    if "mapt" in args.type:
        print("Type MAP-T")
        args.type.remove("mapt")
    if "464xlat" in args.type:
        print("Type 464XLAT")
        args.type.remove("464xlat")
    if "pppoe" in args.type:
        print("Type PPPoE")
        args.type.remove("pppoe")
    if len(args.type) > 0:
        print("Unknown Types:",args.type)

# Validate DHCP Server
dhcp = dhcp_srv(args)

# Error, print help and exit
if will_exit or len(gwan) == 0 or dhcp is None:
    parser.print_help()
    exit(1)

# Bring interface up
ipr.link('set', index=oif[0], state='up')

# Start DHCP Server (will return on error)
dhcp.setup(gwan)

# Exit