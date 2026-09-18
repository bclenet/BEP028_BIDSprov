# Search for all nodes linked to a prov:Entity

"""
https://stackoverflow.com/questions/37186530/how-do-i-construct-get-the-whole-sub-graph-from-a-given-resource-in-rdf-graph
This works because every property is either x: or not, so x:|!x: matches every property,
and then (x:|!x:)* is an arbitrary length path, including paths of length zero,
which means that ?s will be bound to everything reachable from :a, including :a itself.
Then you're grabbing the triples where ?s is the subject.
When you construct the graph of all those triples, you get the subgraph connected to :a.
"""

import json
from io import StringIO

from pyld import jsonld

from rdflib import Dataset, ConjunctiveGraph
from rdflib.plugins.sparql import prepareQuery

with open("example.jsonld", "r") as f:
    base_provenance = json.load(f)

graph = Dataset()
graph.parse(StringIO(json.dumps(jsonld.expand(base_provenance))), format='json-ld')

file_name = "bids::sub-01/anat/c2sub-01_T1w.nii"
file_name = "bids::sub-01/func/sub-01_task-tonecounting_bold.nii"

query = prepareQuery(f"""
    CONSTRUCT {{ ?s ?p ?o }} WHERE {{
        <{file_name}> (<>|!<>)* ?s .
        ?s ?p ?o .
        }}
    """
    )

output_graph = ConjunctiveGraph()
for triple in graph.query(query):
    output_graph.add(triple)

import bids_prov.visualize
bids_prov.visualize.viz_turtle(output_graph.serialize(format="turtle"), "test.png")


print(json.dumps(output_graph.serialize(format="json-ld"), indent=4))


"""
g.parse(data=output, format="json-ld")
g.parse(data=output, format="json-ld")
"""