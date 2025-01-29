#!/usr/bin/python
# coding: utf-8

""" Merge available prov JSON files into one RDF graph """

import json
from pyld import jsonld

# List of available prov files
prov_soft_files = [
	'prov/prov-dcm2niix_ses-01_soft.prov.json',
	'prov/prov-dcm2niix_ses-02_soft.prov.json'
]
prov_env_files = [
	'prov/prov-dcm2niix_ses-01_env.prov.json',
	'prov/prov-dcm2niix_ses-02_env.prov.json'
]
sidecar_files = [
	'sub_02/ses_20130717141500/anat/sub-02_ses-20130717141500_T1w.json',
	'sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.json'
]

# Base jsonld
with open('prov/base.prov.jsonld', encoding = 'utf-8') as file:
	base_provenance = json.load(file)

# Parse Software
for prov_file in prov_soft_files:
	with open(prov_file, encoding = 'utf-8') as file:
		data = json.load(file)
		for key, value in data.items():
			value['Id'] = key
			base_provenance['Records']['Software'].append(value)

# Parse Environments
for prov_file in prov_env_files:
	with open(prov_file, encoding = 'utf-8') as file:
		data = json.load(file)
		for key, value in data.items():
			value['Id'] = key
		 	# /!\ Workaround: environments are added in the Entities list because
		 	# the Environments term is not defined in the BIDS Prov context yet
			base_provenance['Records']['Entities'].append(value)

# Parse Sidecar files
for sidecar_file in sidecar_files:
	with open(sidecar_file, encoding = 'utf-8') as file:
		data = json.load(file)
		if 'GeneratedBy' in data:
			activity = data['GeneratedBy']
			base_provenance['Records']['Activities'].append(activity)
			base_provenance['Records']['Entities'].append({
				"Id": f"bids::{sidecar_file}",
				"GeneratedBy": activity["Id"]
				})

# Write jsonld
with open('prov/experiment_1/merged_provenance.prov.jsonld', 'w', encoding = 'utf-8') as file:
	file.write(json.dumps(base_provenance, indent = 2))
