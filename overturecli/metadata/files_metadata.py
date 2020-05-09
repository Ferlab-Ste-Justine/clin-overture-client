"""
Implements the logic to get the all files metadata from the filesystem that SONG requires
"""

import os
import hashlib

_HASH_CHUNK_SIZE = 8192
_EXTENSION_TYPE_MAPPING = {
    '.txt': 'TXT',
    '.html': 'HTML',
    '.tsv': 'TSV',
    '.csv': 'CSV',
    '.cram': 'CRAM',
    '.crai': 'CRAI'
}

def _hash_path(file_path):
    with open(file_path, "rb") as file_handle:
        file_hash = hashlib.md5()
        while chunk := file_handle.read(_HASH_CHUNK_SIZE):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def get_file_metadata(file_path):
    """
    For a file at the specified path, retrieve the metadata from the filesystem that SONG expects
    """
    extension = os.path.splitext(file_path)[1]
    return {
        'fileSize': os.stat(file_path).st_size,
        'fileName': os.path.basename(file_path),
        'fileType': _EXTENSION_TYPE_MAPPING[str.lower(extension)],
        'fileMd5sum': _hash_path(file_path)
    }
