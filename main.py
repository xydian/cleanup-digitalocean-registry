# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import requests


def delete_repository_tag(
    token: str,
    repository_name: str,
    tag: str
):
    request_url = 'https://api.digitalocean.com/v2/registry/modugen-registry/repositories/' + repository_name + '/tags/' + tag
    resp = requests.delete(
        request_url,
        headers={
            "Authorization": "Bearer " + token
        }
    )
    assert 204 == resp.status_code


def get_repo_tags(
    token: str,
    repository_name: str
):
    request_url = 'https://api.digitalocean.com/v2/registry/modugen-registry/repositories/' + repository_name + '/tags'
    resp = requests.get(
        request_url,
        headers={
            "Authorization": "Bearer " + token
        }
    )

    assert resp.status_code == 200

    resp_json = resp.json()
    return resp_json


# This simple cleanup script deletes all docker images in a digitalocean registry that are not labeled
# with the tag 'latest'
if __name__ == '__main__':
    token = sys.argv[1]
    registry = sys.argv[2]
    repo_name = sys.argv[3]

    resp_json = get_repo_tags(token, repo_name)

    latest_manifest_digest = None
    for val in resp_json["tags"]:
        if val["tag"] == "latest":
            latest_manifest_digest = val["manifest_digest"]

    assert latest_manifest_digest is not None

    for val in resp_json["tags"]:
        tag = val["tag"]
        manifest_digest = val["manifest_digest"]
        if manifest_digest != latest_manifest_digest:
            delete_repository_tag(
                token,
                repo_name,
                tag
            )
