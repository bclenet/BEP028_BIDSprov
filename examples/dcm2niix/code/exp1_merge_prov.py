import json

from rdflib import Graph
from pyld import jsonld

prov_files = [
	#'prov/common.prov.jsonld',
	'prov/software.prov.jsonld',
	'prov/environments.prov.jsonld',
	'sub_02/ses_20130717141500/anat/sub-02_ses-20130717141500_T1w.prov.jsonld',
	'sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld'
]

with open('prov/bidsprov_context.json', encoding = 'utf-8') as file:
	context = json.load(file)

rdf_graph = ''
for prov_file in prov_files:
	with open(prov_file, encoding = 'utf-8') as file:
		#expanded = json.dumps(jsonld.flatten(jsonld.expand(json.load(file)), ctx = context, options = {'processingMode': 'json-ld-1.1'}), indent = 2)
		#print(expanded)
		rdf_graph += f'# {prov_file}\n'
		rdf_graph += jsonld.normalize(
			json.load(file), {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
		rdf_graph += '\n'

		#graph.parse(data = expanded, format = 'json-ld')
print(rdf_graph)


"""
graph.parse('prov/common.prov.jsonld', format = 'json-ld')
graph.parse('prov/software.prov.jsonld', format = 'json-ld')
graph.parse('prov/environments.prov.jsonld', format = 'json-ld')
graph.parse('sub_02/ses_20130717141500/anat/sub-02_ses-20130717141500_T1w.prov.jsonld', format = 'json-ld')
graph.parse('sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld', format = 'json-ld')
"""
#print(len(graph))
#graph.serialize(destination = 'prov/experiment_1/merged_provenance.ttl')
with open('prov/experiment_1/merged_provenance.ttl', 'w' , encoding = 'utf-8') as file:
	file.write(rdf_graph)
