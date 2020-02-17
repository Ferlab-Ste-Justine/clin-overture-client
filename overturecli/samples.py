import csv

def get_samples(samples_file_handle):
    samples = {}
    reader = csv.reader(samples_file_handle)
    for row in reader:
        samples[row[0]] = row[1:]
    return samples