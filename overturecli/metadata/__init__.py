"""
This module abstracts away metadata processing details for the rest of the client logic
"""
#pylint: disable=R0801

import copy
import csv
import json
import os
from datetime import datetime
from overturecli import schemas
from .files_metadata import get_file_metadata

def get_submission_metadata(upload_path):
    """
    Load the all the user submitted meta-data from the metadata file
    """
    with open(os.path.join(upload_path, 'metadata.json')) as metadata_file:
        return [
            schemas.SubmittedClinReadAlignmentAnalysis().load(
                analysis_metadata
            ) for analysis_metadata in json.loads(metadata_file.read())
        ]

def get_submission_files_metadata(upload_path, analysis_metadata):
    """
    Augment the user-supplied metadata for the files to upload with various statistics easily
    inferable from the filesystem (size, md5sum, etc) which SONG expects
    """
    return [
        schemas.FileMetadata().load({
            **file_metadata,
            **get_file_metadata(os.path.join(upload_path, 'files', file_metadata['fileName'])),
            **{"fileAccess": "controlled", "studyId": analysis_metadata["studyId"]}
        }) for file_metadata in analysis_metadata['files']
    ]

def integrate_metadata(files_metadata, analysis_metadata):
    """
    Join the user supplied metadata, extra file metadata inferred from the filesystem and the extra
    sample metadata inferred from clin into the structure which SONG expects to submit an analysis
    """
    analysis_metadata = copy.deepcopy(analysis_metadata)
    analysis_metadata['files'] = files_metadata
    return analysis_metadata

def analysis_upload_to_json(upload_analysis):
    """
    Convert the analysis to upload from a dictionary to JSON, using the validator to convert
    types.
    """
    return schemas.UploadClinReadAlignmentAnalysis().dumps(upload_analysis)
