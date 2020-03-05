import click
import os
import pprint


import overturecli.metadata as metadata
import overturecli.files_metadata as files_metadata
import overturecli.clin as clin

PP = pprint.PrettyPrinter(indent=4)

@click.group()
def cli():
    pass

@click.command()
@click.option('--upload-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True), envvar='UPLOAD_DIR', help='Path containing the metadata and files to upload')
@click.option('--elasticsearch-url', type=click.STRING, envvar='ELASTICSEARCH_URL', help='Elasticsearch connection string')
@click.option('--overture-auth-token', type=click.STRING, envvar='OVERTURE_AUTH_TOKEN', help='Token to use when uploading to the overture stack')
def batch_upload(upload_dir, elasticsearch_url):
    submitted_metadata = metadata.get_submission_metadata(upload_dir)
    for analysis_metadata in submitted_metadata:
        files_metadata = metadata.get_submission_files_metadata(upload_dir, analysis_metadata)
        samples_metadata = metadata.get_sample_related_metadata(elasticsearch_url, analysis_metadata)
        filled_analysis_metadata = metadata.join_metadata(files_metadata, samples_metadata, analysis_metadata)
        PP.pprint(filled_analysis_metadata)

cli.add_command(batch_upload)
