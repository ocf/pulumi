#!/usr/bin/env python3

import pathlib
import tempfile
import urllib3
import zipfile


from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

local_path_provisioner_namespace = Namespace("local-path-provisioner")

# Location on each node to store Persistent Volumes
local_path_storage = "/opt/local-path-provisioner"

# Local path provisioner is not on any helm repo that I know of
# So we have to download and import it locally
# Tracking issue: https://github.com/rancher/local-path-provisioner/issues/89

local_path_provisioner_version = "0.0.18"

local_path_provisioner_location = f"https://github.com/rancher/local-path-provisioner/archive/v{local_path_provisioner_version}.zip"

# Downloads local-path-provisioner
def download_lpp_chart():
    tmpdir_ = tempfile.mkdtemp()

    tmpdir = pathlib.Path(tmpdir_)

    # We don't really need requests to simplify 5 lines
    connection_pool = urllib3.PoolManager()

    download_location = tmpdir / "local-path-provisioner.zip"

    f = open(str(download_location), 'wb')
    resp = connection_pool.request('GET', local_path_provisioner_location)
    f.write(resp.data)
    f.close()

    resp.release_conn()

    with zipfile.ZipFile(download_location, 'r') as zip:
        zip.extractall(str(tmpdir))

    chart_location = tmpdir / f"local-path-provisioner-{local_path_provisioner_version}" / "deploy" / "chart"

    return str(chart_location)


local_path_provisioner = Chart(
    "local-path-provisioner",
    LocalChartOpts(
        path=download_lpp_chart(),
        namespace=local_path_provisioner_namespace.metadata["name"],
        values={
            "nodePathMap": [{
                "node": "DEFAULT_PATH_FOR_NON_LISTED_NODES",
                "paths": [local_path_storage],
            }],
        },
    )
)
