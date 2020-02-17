import click
import os
import pprint


import overturecli.samples as samples
import overturecli.files_metadata as files_metadata
import overturecli.clin as clin

PP = pprint.PrettyPrinter(indent=4)

@click.group()
def cli():
    pass

@click.command()
@click.option('--samples-file', type=click.File('r'), envvar='SAMPLES_FILE', help='File containing a list of the sample submitter ids and their files')
@click.option('--elasticsearch-url', type=click.STRING, envvar='ELASTICSEARCH_URL', help='Elasticsearch connection string')
def batch_upload(samples_file, elasticsearch_url):
    _samples = samples.get_samples(samples_file)
    _samples = files_metadata.add_files_metadata(
        os.path.dirname(samples_file.name), 
        _samples
    )
    _samples = clin.expand_related_entities(elasticsearch_url, _samples)
    PP.pprint(_samples)

cli.add_command(batch_upload)
