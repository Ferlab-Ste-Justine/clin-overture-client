import copy
import csv
import json
import os
from datetime import datetime
from overturecli import schemas
from .files_metadata import get_file_metadata
from .clin import get_sample_related_entities

def get_submission_metadata(upload_path):
    with open(os.path.join(upload_path, 'metadata.json')) as metadata_file:
        return [
            schemas.SubmittedClinReadAlignmentAnalysis().load(
                analysis_metadata
            ) for analysis_metadata in json.loads(metadata_file.read())
        ]

def get_submission_files_metadata(upload_path, analysis_metadata):
    return [
        schemas.FileMetadata().load({
            **file_metadata, 
            **get_file_metadata(os.path.join(upload_path, 'files', file_metadata['fileName'])), 
            **{"fileAccess": "controlled", "studyId": analysis_metadata["studyId"]}
        }) for file_metadata in analysis_metadata['files']
    ]

def get_sample_related_metadata(elasticsearch_url, analysis_metadata):
    return [
        schemas.Sample().load(
            get_sample_related_entities(elasticsearch_url, sample_metadata['submitterSampleId'])
        ) for sample_metadata in analysis_metadata['samples']
    ]

def join_metadata(files_metadata, samples_metadata, analysis_metadata):
    analysis_metadata = copy.deepcopy(analysis_metadata)
    analysis_metadata['samples'] = samples_metadata
    analysis_metadata['files'] = files_metadata
    return analysis_metadata

def analysis_upload_to_json(upload_analysis):
    return schemas.UploadClinReadAlignmentAnalysis().dumps(upload_analysis)

