"""
Higher level abstractions on top of the SONG SDK to get robust client-specific fonctionality.

It makes several calls with the sdk in each function and is opinionated about user feedback
"""

import os
import shutil
import json
import click

from song import SongClient

# pylint: disable=R0913

VERIFY_CERTIFICATES = os.environ.get("OVERTURE_CLI_VERIFY_CERTIFICATES", "true") == "true"

def create_study(
        study_id,
        name,
        description,
        organization,
        song_url,
        auth_token
):
    """
    Creates a study, checking if the study already exists first and printing a message if it does
    """
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )
    if not study_id in song_client.get_studies_list():
        song_client.create_study(
            study_id,
            name,
            description,
            organization
        )
    else:
        click.echo('study already present. Skipping creation.')

def create_analysis_definition(
        schema,
        song_url,
        auth_token
):
    """
    Creates an analysis schema definition, checking if the definition already exists in SONG first
    and printing a message if it does.
    """
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )

    schemas = song_client.get_schemas()
    if not schema['name'] in [result.name for result in schemas.resultSet]:
        song_client.create_schema(json.dumps(schema))
    else:
        click.echo('analysis already present. Skipping creation.')

def upload(study_id, payload, song_url, auth_token):
    """
    Upload an analysis in SONG
    """
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )
    response = song_client.create_custom_analysis(
        study_id,
        payload
    )
    return response['analysisId']

def create_manifest(
        upload_dir,
        study_id,
        analysis_id,
        song_url,
        auth_token
):
    """
    Gets the files manifest string for a given analysis from SONG and outputs it in a file
    """
    files_dir = os.path.join(upload_dir, 'files')
    manifest_dir = os.path.join(upload_dir, 'manifests')
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )
    manifest = song_client.get_analysis_manifest(
        study_id,
        analysis_id,
        files_dir
    )
    if os.path.isdir(manifest_dir):
        shutil.rmtree(manifest_dir)
    os.makedirs(manifest_dir)
    manifest.write(
        os.path.join(manifest_dir, 'manifest.txt'),
        overwrite=True
    )

def get_analyses(study_id, status, song_url, auth_token):
    """
    Gets all the analyses with a given status and study from SONG
    """
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )
    return song_client.get_analyses(study_id, status)

def publish_analysis(study_id, analysis_id, song_url, auth_token):
    """
    Publish the given analysis in SONG.

    TODO: A check to see if the analysis is already published should be made here.
    """
    song_client = SongClient(
        song_url,
        auth_token,
        VERIFY_CERTIFICATES
    )
    song_client.publish_analysis(study_id, analysis_id)
