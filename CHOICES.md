# Choices

Why did we make the choices we made while setting up this cluster?

## k3s

This is one of the more controvertial choices. We chose this because...
- simple setup
- low resource-use
- strong community and company backing
- easy to migrate away from

## cilium

- low pain initial setup
- eBPF-based
    - extensible (powerful custom rule system)
    - fast
- ~njha and ~night are already familiar with it

## (lack of) CoreDNS

- Pulumi should grab service IPs instead of typing `svc.cluster.local`
