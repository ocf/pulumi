#!/usr/bin/env python3

"""The OCF Kubernetes configuration"""

# Core Services (CNI, Ingress, Storage)
import core.cilium
import core.local_path_provisioner
import core.traefik

# Misc. Infrastructure (Databases, Monitoring, Updates)
import infra.prometheus

# Applications and Services (Jukebox, Matrix, HTTP Things)
# ... none yet ...
