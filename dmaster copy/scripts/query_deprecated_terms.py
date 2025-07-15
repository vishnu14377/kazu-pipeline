from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

# Create a new graph
g = Graph()

# Load the ontology
g.parse("dMaster/ontologies/combined_ontology.ttl", format="turtle")

# Define the SPARQL query
query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?property
WHERE {
  ?property ?p ?o .
  FILTER(STRSTARTS(STR(?property), "http://example.org/disease-master-ontology#"))
}
"""

# Prepare and execute the query
q = prepareQuery(query)
results = g.query(q)

# Print results
print("Deprecated properties in disease-master-ontology namespace:")
print("-" * 50)
for row in results:
    print(row.property) 