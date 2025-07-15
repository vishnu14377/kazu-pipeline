from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL

def find_entities_by_label(graph: Graph, label_text: str, type_uri) -> list:
    """
    Find all subjects in the graph that have an rdfs:label equal to label_text 
    (in any language) and are of rdf:type == type_uri.
    Returns a list of matching subject URIs.
    """
    matches = []
    for subj, _, obj in graph.triples((None, RDFS.label, None)):
        if isinstance(obj, Literal):
            if str(obj) == label_text:
                if (subj, RDF.type, type_uri) in graph:
                    matches.append(subj)
    return matches
