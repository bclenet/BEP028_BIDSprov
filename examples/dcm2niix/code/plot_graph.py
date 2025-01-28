from argparse import ArgumentParser

from prov.serializers.provrdf import ProvRDFSerializer
from prov.dot import prov_to_dot

# Parse arguments
parser = ArgumentParser(description='Visualize RDF graph as image.')
parser.add_argument('-i', '--input', type=str, required=True,
    help='input RDF file')
parser.add_argument('-o', '--output', type=str, required=True,
    help='output graph as PNG')
arguments = parser.parse_args()

# Open file
with open(arguments.input, 'r', encoding = 'utf-8') as file:
	doc = ProvRDFSerializer().deserialize(file)

dot = prov_to_dot(doc)
dot.write_png(arguments.output)
