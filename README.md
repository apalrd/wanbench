# wanbench
Simulation of a variety of WAN IPv4/IPv6 transition mechanisms

This is designed to run on a Linux system with the following requirements:
- The system must have global IPv4 and IPv6 connectivity
- The system must have an Ethernet interface which is connected to the CPE router under test
- Global IPv4 connectivity will use NAT44 via the system's default IPv4 interface, even for cases which simulate 'global' connectivity. 
- Global IPv6 connectivity will use NAT66 via the system's default IPv6 interface, due to difficulty in getting prefix delegations large enough for testing many of these transition mechanisms (this does *NOT* imply that NAT66 is not *very cursed*)
- The test assumes a single client CPE, and will not properly handle multiple clients. No client address space isolation is attempted, either, so running the script on two interfaces is also likely to fail for some setups (i.e. DS-Lite)