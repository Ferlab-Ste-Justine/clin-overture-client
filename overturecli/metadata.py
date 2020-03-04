import csv
import os
from datetime import datetime
from .schemas import SubmittedClinReadAlignmentAnalysis
from .files_metadata import get_file_metadata

def get(upload_path):
    with open(os.path.join(upload_path, 'metadata.json')) as metadata_file:
        file_content = metadata_file.read()
        print(file_content)
        return SubmittedClinReadAlignmentAnalysis().load(file_content)

