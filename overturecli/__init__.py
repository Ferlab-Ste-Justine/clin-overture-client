import click
import json
import os
import pprint

from keycloak import KeyCloakClient

import overturecli.metadata as metadata
import overturecli.song_calls as song_calls
import overturecli.score_calls as score_calls
import overturecli.store as store

PP = pprint.PrettyPrinter(indent=4)

#import logging
#songLogger = logging.getLogger('song')
#songLogger.setLevel(10)

def get_auth_token():
    env_token = os.environ.get('AUTH_TOKEN', None)
    if env_token is None:
        store_token = store.get_auth_token()
        if store_token is None:
            raise Exception("Auth token is necessary, but not specified")
        return store_token
    else:
        return env_token

@click.group()
def cli():
    pass

@click.command()
@click.option('--schema-path', type=click.Path(exists=True, file_okay=True, dir_okay=False), help='Path to schema')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def create_analysis_definition(
    schema_path,
    song_url,
    auth_token
):
    with open(schema_path) as schema_file:
        song_calls.create_analysis_definition(
            json.load(schema_file),
            song_url,
            auth_token
        )

@click.command()
@click.option('--id', type=click.STRING, help='ID of the study to create')
@click.option('--name', type=click.STRING, help='Name of the study to create')
@click.option('--description', type=click.STRING, help='Description of the study to create')
@click.option('--organization', type=click.STRING, help='Organization of the study to create')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def create_study(
    id,
    name,
    description,
    organization,
    song_url,
    auth_token
):
    song_calls.create_study(
        id,
        name,
        description,
        organization,
        song_url,
        auth_token
    )

@click.command()
@click.option('--keycloak-url', type=click.STRING, envvar='KEYCLOAK_URL', help='Keycloak connection string')
@click.option('--keycloak-username', type=click.STRING, envvar='KEYCLOAK_USERNAME', help='Keycloak username')
@click.option('--keycloak-password', type=click.STRING, envvar='KEYCLOAK_PASSWORD', help='Keycloak password')
@click.option('--keycloak-secret', type=click.STRING, envvar='KEYCLOAK_SECRET', help='Keycloak secret')
def keycloak_login(
    keycloak_url,
    keycloak_username,
    keycloak_password,
    keycloak_secret
):
    token = KeyCloakClient(
        '{keycloak_url}/auth/realms/{keycloak_realm}'.format(
            keycloak_url=keycloak_url,
            keycloak_realm='clin'
        ),
        'clin-proxy-api',
        keycloak_secret
    ).login(
        keycloak_username, 
        keycloak_password
    )
    store.store_auth_token(token)

@click.command()
@click.option('--upload-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True), envvar='UPLOAD_DIR', help='Path containing the metadata and files to upload')
@click.option('--elasticsearch-url', type=click.STRING, envvar='ELASTICSEARCH_URL', help='Elasticsearch connection string')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--score-url', type=click.STRING, envvar='SCORE_URL', help='Score url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def batch_upload(
    upload_dir, 
    elasticsearch_url,
    song_url,
    score_url,
    auth_token
):
    submitted_metadata = metadata.get_submission_metadata(upload_dir)
    for index, analysis_metadata in enumerate(submitted_metadata, start=0):
        stored_analysis = store.find_or_insert_analysis(index, upload_dir)
        if not stored_analysis['created']:
            files_metadata = metadata.get_submission_files_metadata(upload_dir, analysis_metadata)
            samples_metadata = metadata.get_sample_related_metadata(elasticsearch_url, analysis_metadata)
            filled_analysis_metadata = metadata.join_metadata(files_metadata, samples_metadata, analysis_metadata)
            study_id = filled_analysis_metadata['studyId']
            analysis_id = song_calls.upload(
                study_id,
                metadata.analysis_upload_to_json(filled_analysis_metadata), 
                song_url, 
                auth_token
            )
            store.save_analysis_creation(index, upload_dir, analysis_id)
        else:
            analysis_id = stored_analysis['id']
            click.echo("Analysis {analysis_id} already exists. Skipping creation.".format(analysis_id=analysis_id))

        if not stored_analysis['files_uploaded']:
            song_calls.create_manifest(
                upload_dir,
                analysis_metadata['studyId'],
                analysis_id,
                song_url,
                auth_token
            )
            score_calls.upload_files(
                upload_dir,
                song_url,
                score_url,
                auth_token
            )
            store.save_analysis_files_upload(index, upload_dir)
        else:
            click.echo("Files for analysis {analysis_id} already uploaded. Skipping upload.".format(analysis_id=analysis_id))

cli.add_command(create_analysis_definition)
cli.add_command(create_study)
cli.add_command(keycloak_login)
cli.add_command(batch_upload)