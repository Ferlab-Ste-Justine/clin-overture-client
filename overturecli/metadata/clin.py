import os
from elasticsearch import Elasticsearch

def get_sample_related_entities(elasticsearch_url, submitterSampleId):
    es = Elasticsearch([elasticsearch_url])
    res = es.search(
        index="patient", 
        body={"query": { "match": { "samples.container":  submitterSampleId }}}
    )
    if len(res['hits']['hits']) > 0:
        result = res['hits']['hits'][0]['_source']
        sample = list(filter(
            lambda sample: sample['container'][0]==submitterSampleId, 
            result['samples']
        ))[0]
        sample_speciment = list(filter(
            lambda specimen: specimen['id'] == sample['parent']['id'],
            result['specimens']
        ))[0]
        return {
            'submitterSampleId': submitterSampleId,
            'sampleType': sample['type']['text'],
            'specimen': {
                'submitterSpecimenId': sample_speciment['container'][0],
                'specimenType': 'Normal',
                'specimenTissueSource': sample_speciment['type']['text'],
                'tumourNormalDesignation': 'Normal'
            },
            'donor': {
                'submitterDonorId': result['id'],
                'studyId': result['studies'][0]['id'],
                'gender': result['gender'].capitalize()
            }
        }
    else:
        raise Exception("submitterSampleId {submitterSampleId} cannot be found in Elasticsearch".format(submitterSampleId=submitterSampleId))