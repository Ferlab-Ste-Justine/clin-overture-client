"""
Higher level abstractions on top of the score client.

The execution of the Score client as a separate container app is not ideal and this can be refacted
separately without impacting the rest of the client functionality at a later time.
"""

import os
import docker

SCORE_CLIENT_IMAGE = os.environ['SCORE_CLIENT_IMAGE']
CONTAINER_NAME = os.environ['CONTAINER_NAME']

def upload_files(
        upload_dir,
        song_url,
        score_url,
        auth_token
):
    """
    Call the score client in a separate container to upload the files in a given manifest
    on Score's object store
    """
    manifest_path = os.path.join(upload_dir, 'manifests', 'manifest.txt')
    client = docker.from_env()
    client.containers.run(
        image=SCORE_CLIENT_IMAGE,
        remove=True,
        detach=False,
        volumes_from=[CONTAINER_NAME],
        environment={
            "ACCESSTOKEN": auth_token,
            "METADATA_URL": song_url,
            "STORAGE_URL": score_url
        },
        network_mode='host',
        command=[
            "/score-client/score-client-dist/bin/score-client",
            "upload",
            "--manifest",
            manifest_path
        ]
    )

def download_file(
        download_dir,
        file_object_id,
        song_url,
        score_url,
        auth_token
):
    """
    Call the score client in a separate container to download a file from Score's object store
    """
    client = docker.from_env()
    client.containers.run(
        image=SCORE_CLIENT_IMAGE,
        remove=True,
        detach=False,
        volumes_from=[CONTAINER_NAME],
        environment={
            "ACCESSTOKEN": auth_token,
            "METADATA_URL": song_url,
            "STORAGE_URL": score_url
        },
        network_mode='host',
        command=[
            "/score-client/score-client-dist/bin/score-client",
            "download",
            "--object-id",
            file_object_id,
            "--output-dir",
            download_dir
        ]
    )
