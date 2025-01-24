from rdflib import Graph

graph = Graph()
graph.parse("prov/software.prov.jsonld", format = "json-ld")
graph.parse("prov/environments.prov.jsonld", format = "json-ld")
graph.parse("sub_02/ses_20130717141500/anat/sub-02_ses-20130717141500_T1w.prov.jsonld", format = "json-ld")
graph.parse("sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld", format = "json-ld")
print(len(graph))
graph.serialize(destination = "prov/experiment_1/merged_provenance.ttl")
