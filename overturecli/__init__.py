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
def batch_upload(upload_dir, elasticsearch_url):
    submitted_metadata = metadata.get(upload_dir)
    PP.pprint(submitted_metadata)

cli.add_command(batch_upload)
