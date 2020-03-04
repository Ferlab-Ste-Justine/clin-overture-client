import os
import copy
import hashlib

HASH_CHUNK_SIZE=8192
EXTENSION_TYPE_MAPPING = {
    '.txt': 'TXT',
    '.html': 'HTML',
    '.tsv': 'TSV',
    '.csv': 'CSV',
    '.cram': 'CRAM',
    '.crai': 'CRAI'
}

def hash_path(file_path):
    with open(file_path, "rb") as file_handle:
        file_hash = hashlib.md5()
        while chunk := file_handle.read(HASH_CHUNK_SIZE):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def get_file_metadata(file_path):
    extension = os.path.splitext(file_path)[1]
    return {
        'size': os.stat(file_path).st_size,
        'name': os.path.basename(file_path),
        'type': EXTENSION_TYPE_MAPPING[str.lower(extension)],
        'md5sum': hash_path(file_path)
    }