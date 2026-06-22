# Lab Topology

This document describes the lab topology in a public-safe way.

## Public-safe example topology

    Client devices
         |
         | Ethernet / Wi-Fi
         |
    Home router / lab gateway
         |
         | Ethernet
         |
    Cisco lab switch
         |
         | Access / trunk ports
         |
    Lab clients / test devices

## Privacy note

Do not publish real values for:

- public IP addresses
- Tailscale IP addresses
- real MAC addresses
- serial numbers
- personal hostnames
- ISP account details
- full production-like configurations

Use anonymized names such as:

- `lab-switch-01`
- `client-01`
- `vlan-10-users`
- `vlan-20-lab`
