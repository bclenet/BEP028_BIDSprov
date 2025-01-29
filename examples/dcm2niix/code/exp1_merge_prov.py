#!/usr/bin/python
# coding: utf-8

""" Merge available prov JSON-LD files into one RDF graph """

import json
from pyld import jsonld

# List of available prov files
prov_files = [
	'prov/software.prov.jsonld',
	'prov/environments.prov.jsonld',
	'sub_02/ses_20130717141500/anat/sub-02_ses-20130717141500_T1w.prov.jsonld',
	'sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld'
]

# Generate RDF graph of each file using pyld
rdf_graph = ''
for prov_file in prov_files:
	with open(prov_file, encoding = 'utf-8') as file:
		rdf_graph += f'# {prov_file}\n'
		rdf_graph += jsonld.normalize(
			jsonld.flatten(data), {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
		rdf_graph += '\n'

# Write RDF graph
with open('prov/experiment_1/merged_provenance.ttl', 'w' , encoding = 'utf-8') as file:
	file.write(rdf_graph)
