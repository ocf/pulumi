#!/usr/bin/env python3

import socket

from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

traefik_namespace = Namespace("traefik")

# Get the current IP address for kubernetes to expose as a NodePort
node_ip = socket.gethostbyname(socket.gethostname())
exposed_ips = [node_ip]


def traefik_chart_transformation(obj, opts):
    # The default Traefik chart's Service is a LoadBalancer in the default namespace
    # We set it to a NodePort, listening on all IPs, in the traefik namespace
    if obj["kind"] == "Service":
        obj["spec"]["type"] = "NodePort"
        obj["metadata"]["namespace"] = traefik_namespace.metadata["name"]
        obj["spec"]["externalIPs"] = exposed_ips


traefik = Chart(
    "traefik",
    ChartOpts(
        chart="traefik",
        version="9.10.1",
        fetch_opts=FetchOpts(
            repo="https://helm.traefik.io/traefik"),
        namespace=traefik_namespace.metadata["name"],
        values={
            # Debugging
            # "logs": {"general": {"level": "DEBUG"}},
            # These are the ports that Traefik has open
            "ports": {
                # This one is used for readiness/liveness probes, and is not exposed
                "traefik": {
                    "port": 9000,
                    "expose": True,
                    "exposedPort": 9000,
                    "protocol": "TCP",
                },
                # This one is exposed on port 80, and is used for HTTP
                # It redirects traffic it receives to HTTPS
                "web": {
                    "port": 8000,
                    "expose": True,
                    "exposedPort": 80,
                    "protocol": "TCP",
                    "redirectTo": "websecure",
                },
                # This one is exposed on port 443, and is used for HTTPS
                "websecure": {
                    "port": 8443,
                    "expose": True,
                    "exposedPort": 443,
                    "protocol": "TCP",
                    "tls": {
                        "enabled": True,
                    }
                },
            },
        },
        transformations=[traefik_chart_transformation],
    ),
)
