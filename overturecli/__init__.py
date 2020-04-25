import os
import logging

import click
import json
import pprint

logging.basicConfig(level=os.environ.get("OVERTURE_CLI_LOG_LEVEL", "INFO"))
PP = pprint.PrettyPrinter(indent=4)

from keycloak import KeyCloakClient

import overturecli.metadata as metadata
import overturecli.song_calls as song_calls
import overturecli.score_calls as score_calls
import overturecli.store as store


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
@click.option('--study-id', type=click.STRING, envvar='MAIN_STUDY', help='ID of the analyses study')
@click.option('--publication-status', type=click.Choice(['PUBLISHED', 'UNPUBLISHED'], case_sensitive=False), default='PUBLISHED', help='Whether to get published or unpublished analyses')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def show_analyses(
    study_id,
    publication_status,
    song_url,
    auth_token
):
    analyses = song_calls.get_analyses(
        study_id,
        publication_status,
        song_url,
        auth_token
    )
    click.echo(json.dumps(analyses, indent=4, sort_keys=True))

@click.command()
@click.option('--download-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True), required=True, help='Path where the file should be downloaded. Note that it will not work if the path is not in a volume of the container the client is running in.')
@click.option('--file-object-id', type=click.STRING, required=True, help='Object id of the file')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--score-url', type=click.STRING, envvar='SCORE_URL', help='Score url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def download_file(
    download_dir,
    file_object_id,
    song_url,
    score_url,
    auth_token
):
    score_calls.download_file(
        download_dir,
        file_object_id,
        song_url,
        score_url,
        auth_token
    )

@click.command()
@click.option('--upload-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True), envvar='UPLOAD_DIR', help='Path containing the metadata and files to upload')
@click.option('--song-url', type=click.STRING, envvar='SONG_URL', help='SONG url')
@click.option('--score-url', type=click.STRING, envvar='SCORE_URL', help='Score url')
@click.option('--auth-token', type=click.STRING, default=get_auth_token, help='Authentication token')
def batch_upload(
    upload_dir, 
    song_url,
    score_url,
    auth_token
):
    submitted_metadata = metadata.get_submission_metadata(upload_dir)
    for index, analysis_metadata in enumerate(submitted_metadata, start=0):
        stored_analysis = store.find_or_insert_analysis(index, upload_dir)
        if not stored_analysis['created']:
            files_metadata = metadata.get_submission_files_metadata(upload_dir, analysis_metadata)
            filled_analysis_metadata = metadata.integrate_metadata(files_metadata, analysis_metadata)
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

        if not stored_analysis['published']:
            song_calls.publish_analysis(analysis_metadata['studyId'], analysis_id, song_url, auth_token)
            store.save_analysis_publication(index, upload_dir)
        else:
            click.echo("Files for analysis {analysis_id} already published. Skipping publication.".format(analysis_id=analysis_id))


cli.add_command(create_analysis_definition)
cli.add_command(create_study)
cli.add_command(keycloak_login)
cli.add_command(show_analyses)
cli.add_command(download_file)
cli.add_command(batch_upload)