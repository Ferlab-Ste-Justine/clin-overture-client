import os
import shutil
import json
import click

from song import SongClient

def create_study(
    id,
    name,
    description,
    organization,
    song_url,
    auth_token
):
    song_client = SongClient(
        song_url,
        auth_token
    )
    if not id in song_client.get_studies_list():
        song_client.create_study(
            id,
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
    song_client = SongClient(
        song_url,
        auth_token
    )
        
    schemas = song_client.get_schemas()
    if not schema['name'] in [result.name for result in schemas.resultSet]:
        song_client.create_schema(json.dumps(schema))
    else:
        click.echo('analysis already present. Skipping creation.')

def upload(studyId, payload, song_url, auth_token):
    song_client = SongClient(
        song_url,
        auth_token
    )
    response = song_client.create_custom_analysis(
        studyId,
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
    files_dir = os.path.join(upload_dir, 'files')
    manifest_dir = os.path.join(upload_dir, 'manifests')
    song_client = SongClient(
        song_url,
        auth_token
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