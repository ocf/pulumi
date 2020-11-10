from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

prometheus_namespace = Namespace("prometheus")

# TODO: Add TLS to the ingresses in this config.

# See values reference below....
# https://github.com/prometheus-community/helm-charts/blob/main/charts/prometheus/values.yaml

prometheus = Chart(
    "prometheus",
    ChartOpts(
        chart="prometheus",
        version="11.16.8",
        fetch_opts=FetchOpts(
            repo="https://prometheus-community.github.io/helm-charts"),
        namespace=prometheus_namespace.metadata["name"],
        values={
            "alertmanager": {
                "enabled": True,
                "ingress": {
                    "enabled": True,
                    "hosts": ["alertmanager.dev-k8s.ocf.berkeley.edu"],
                },
            },
            "server": {
                "ingress": {
                    "enabled": True,
                    "hosts": ["prometheus.dev-k8s.ocf.berkeley.edu"],
                }
            },
        },
    ),
)
