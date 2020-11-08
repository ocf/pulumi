#!/usr/bin/env python3

"""The OCF Kubernetes configuration"""

from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

cilium_namespace = Namespace("cilium")

cilium = Chart(
    "cilium",
    ChartOpts(
        chart="cilium",
        version="1.8.5",
        fetch_opts=FetchOpts(
            repo="https://helm.cilium.io"),
        namespace=cilium_namespace.metadata["name"],
        values={
            # The values change when upgrading cilium to 1.9, watch out!
            "operator": {
                "numReplicas": 1,
            },
        },
    ),
)
