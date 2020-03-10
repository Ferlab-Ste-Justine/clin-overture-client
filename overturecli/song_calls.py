import os

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
    song_client.create_study(
        id,
        name,
        description,
        organization
    )

def upload(studyId, payload, song_url, auth_token):
    song_client = SongClient(
        song_url,
        auth_token
    )
    response = song_client.create_custom_analysis(
        studyId,
        payload
    )
    return response.analysisId

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
    try:
        os.makedirs(manifest_dir)
    except OSError as e:
        pass
    manifest.write(
        manifest_dir,
        overwrite=True
    )