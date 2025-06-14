# wanbench
Simulation of a variety of WAN IPv4/IPv6 transition mechanisms

This is designed to run on a Linux system with the following requirements:
- The system must have global IPv4 and IPv6 connectivity
- The system must have an Ethernet interface which is connected to the CPE router under test
- The test assumes a single client CPE, and will not properly handle multiple clients. No client address space isolation is attempted, either, so running the script on two interfaces is also likely to fail for some setups (i.e. DS-Lite)

## Options

| Option | Default | Description |
| -- | -- | -- |
| `-i`, `--interface` | | Linux device name of downstream (CPE-facing) Ethernet interface |
| `-t`, `--type` | | Type of interface(s) to simulate. May be specified multiple times. When the client supports multiple types, the order of arguments determines the preference. Must be one of: `dualstack` `cgnat` `dslite` `lw4o6` `mape` `mapt` `464xlat` |
| `-d`, `--debug` | | Print out a significant amount of debug information 
| `-p`, `--prefix` | `2001:db8::/36` | Prefix from which to generate DHCPv6-PD allocation to the client. The client's allocation will be a subset of this prefix, calculated according to the interface type setup. |
| `-s`, `--size` | `56` | Prefix size to delegate to the client using DHCPv6-PD |
| `-g`, `--onlink` | | On-link address (CIDR notation). If specified, will be used for DHCPv6 IA_NA response. If not specified, IA_NA will not be allowed, and only link-local addressing will be used on-link.  |
| `-l`, `--legacy` | `203.0.113.5/24` | Legacy global address, used wherever the global IPv4 address assigned to the client would be used. Specified in CIDR notation, where the prefix length is returned to the client via DHCP and the first address in the subnet is used as the ISP's gateway address. If a /32 is used, then the 'far' gateway address will be used. |
| `-n`, `--nat` | | Perform NAT44 / NAT66 between the legacy IP, prefix IPv6, and onlink IPv6, using the upstream IPs assigned to the test system. This allows testing with sufficiently large prefixes without owning public IPv4 and IPv6 space. This does *NOT* imply that NAT66 is not *cursed*. |
| `-r`, `--reuse` | `8` | Re-use ratio for statically allocated address+port mapped types (MAP-E, MAP-T) |
| `--fargw` | `100.64.0.1` | For dual-stack, when assigning a /32 to the client, use this as the 'far' gateway address |
| `--aftr`' | `2001:db8:d00d::` | Address of the AFTR function (configured as a routed address)
| `--cgnat`| `100.69.96.5/24` | For cgnat, the address to assign to the client. The router will take the first address of this network, and the specified address will be assigned to the client. |
| `--mapinv` | `1024` | For MAP, the number of invalid / unallocated ports (must be a power of two) |
| `--pref64` | `64:ff9b::/96` | For 464xlat, the RFC6052 translation prefix |
| `--dmr` | `2001:db8:6464::/64` | For MAP-T, the default mapping rule RFC6052 translation prefix | 
| `--index` | | For MAP-E and MAP-T, the subscriber index to calculate IP + Port Range (where the valid range = the number of addresses in `-l` * the reuse factor `-r`) |
| `--ra64` | | Include 464xlat Pref64 in router advertisement (otherwise, only `ipv4only.arpa` is available for detection) |
| `--slaac` | | Configure router advertisement to allow SLAAC ('Autonomous' address allocation) in addition to DHCPv6