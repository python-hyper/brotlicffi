# -*- coding: utf-8 -*-
from __future__ import print_function

import os.path

import requests
import invoke


JENKINS_URL = "https://jenkins.cryptography.io/job/brotlipy-wheel-builder"


@invoke.task
def download_artifacts():
    session = requests.Session()

    response = session.get(
        "{0}/lastBuild/api/json/".format(JENKINS_URL),
        headers={
            "Accept": "application/json"
        }
    )
    response.raise_for_status()
    assert not response.json()["building"]

    paths = []

    last_build_number = response.json()["number"]
    for run in response.json()["runs"]:
        if run["number"] != last_build_number:
            print(
                "Skipping {0} as it is not from the latest build ({1})".format(
                    run["url"], last_build_number
                )
            )
            continue

        response = session.get(
            run["url"] + "api/json/",
            headers={
                "Accept": "application/json",
            }
        )
        response.raise_for_status()
        for artifact in response.json()["artifacts"]:
            response = session.get(
                "{0}artifact/{1}".format(run["url"], artifact["relativePath"])
            )
            out_path = os.path.join(
                os.path.dirname(__file__),
                "dist",
                artifact["fileName"],
            )
            with open(out_path, "wb") as f:
                f.write(response.content)
            paths.append(out_path)

    print(paths)
