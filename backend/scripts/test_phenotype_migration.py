from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

# Create a new graph
g = Graph()

# Load the phenotype ontology
g.parse("dMaster/ontologies/phenotype/phenotype_core.ttl", format="turtle")

# Define the SPARQL query to test migrated properties
query = """
PREFIX : <http://example.org/phenotype-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?type ?domain ?range ?comment
WHERE {
    ?property a owl:ObjectProperty ;
             rdfs:label ?label ;
             rdfs:comment ?comment .
    OPTIONAL { ?property rdfs:domain ?domain }
    OPTIONAL { ?property rdfs:range ?range }
    FILTER(?property IN (
        :hasSupportingPhenotype,
        :hasRequiredPhenotype,
        :hasExclusionPhenotype,
        :hasComorbidity,
        :hasLabValue,
        :hasLaterality,
        :hasAnatomicalLocation,
        :hasPhenotype
    ))
}
ORDER BY ?property
"""

# Prepare and execute the query
q = prepareQuery(query)
results = g.query(q)

# Print results
print("Testing Migrated Phenotype Properties:")
print("-" * 80)
print(f"{'Property':<25} {'Domain':<30} {'Range':<30} {'Comment'}")
print("-" * 80)

for row in results:
    property_name = str(row.property).split("#")[-1]
    domain = str(row.domain).split("#")[-1] if row.domain else "owl:Class"
    range_val = str(row.range).split("#")[-1] if row.range else "Not specified"
    comment = str(row.comment)
    print(f"{property_name:<25} {domain:<30} {range_val:<30} {comment}") 