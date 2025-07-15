import rdflib

g = rdflib.Graph()
g.parse("dMaster/data/ontologies/time.ttl", format="turtle")
g.serialize("dMaster/data/ontologies/time.owl", format="xml")
print("Converted time.ttl to time.owl (RDF/XML)") 