#!/usr/bin/python3
# Setup simulated WAN interfaces (including DHCPv6)
import os
import argparse
from pyroute2 import IPRoute
import ipaddress
import atexit
import dslite
from utils import wan_type,route,ipr
from dhcp import dhcp_srv

# Main
parser = argparse.ArgumentParser(prog='wanbench',description='A tool for setting up simulated WAN interfaces for router testing')
parser.add_argument("-i","--interface",help="Linux device name to simulate WAN connectivity")
parser.add_argument("-m","--mtu",help="Downstream interface MTU (default 1500)")
parser.add_argument("-t","--type",help="Type of interface to simulate, may be specified multiple times, must be one of: "
                    "dualstack cgnat dslite lw4o6 mape mapt 464xlat",action="append")
args = parser.parse_args()

# Globals
gwan = []
will_exit = False

# Validate MTU
if args.mtu is None:
    args.mtu = 1500

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
    if "dualstack" in args.type:
        print("Type DualStack")
    if "cgnat" in args.type:
        print("Type CGNAT")
    if "dslite" in args.type:
        gwan.append(dslite.dslite(args))
    if "lw4o6" in args.type:
        print("Type Lightweight4over6")
    if "mape" in args.type:
        print("Type MAP-E")
    if "mapt" in args.type:
        print("Type MAP-T")
    if "464xlat" in args.type:
        print("Type 464XLAT")

# Error, print help and exit
if will_exit or len(gwan) == 0:
    parser.print_help()
    exit(1)

# Start DHCP Server
dhcp = dhcp_srv(args)

# Exit