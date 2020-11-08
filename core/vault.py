from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

vault_namespace = Namespace("vault")

cilium = Chart(
    "vault",
    ChartOpts(
        chart="vault",
        version="0.8.0",
        fetch_opts=FetchOpts(
            repo="https://helm.releases.hashicorp.com"),
        namespace=vault_namespace.metadata["name"],
        values={
            # Not yet configured...
            # https://github.com/hashicorp/vault-helm/blob/master/values.yaml
        },
    ),
)
