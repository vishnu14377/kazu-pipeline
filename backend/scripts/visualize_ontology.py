from rdflib import Graph, Namespace
import graphviz
import os

def load_ontology(file_path):
    """Load a TTL file into an RDF graph."""
    g = Graph()
    g.parse(file_path, format="turtle")
    return g

def combine_ontologies(graphs):
    """Combine multiple RDF graphs into one."""
    combined = Graph()
    for g in graphs:
        combined += g
    return combined

def visualize_ontology(graph, output_file="ontology_visualization"):
    """Create a visual representation of the ontology using Graphviz."""
    dot = graphviz.Digraph(comment='Ontology Visualization')
    dot.attr(rankdir='LR')  # Left to right layout
    
    # Add nodes for classes
    for s, p, o in graph.triples((None, None, None)):
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#Class':
            label = str(s).split('#')[-1]
            dot.node(str(s), label, shape='box')
        elif p == 'http://www.w3.org/2000/01/rdf-schema#subClassOf':
            dot.edge(str(s), str(o), label='subClassOf')
        elif p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#ObjectProperty':
            label = str(s).split('#')[-1]
            dot.node(str(s), label, shape='diamond')
        elif p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#DatatypeProperty':
            label = str(s).split('#')[-1]
            dot.node(str(s), label, shape='ellipse')
    
    # Add edges for domain and range
    for s, p, o in graph.triples((None, None, None)):
        if p == 'http://www.w3.org/2000/01/rdf-schema#domain':
            dot.edge(str(s), str(o), label='domain')
        elif p == 'http://www.w3.org/2000/01/rdf-schema#range':
            dot.edge(str(s), str(o), label='range')
    
    # Save the visualization
    dot.render(output_file, format='png', cleanup=True)
    print(f"Visualization saved as {output_file}.png")

def main():
    # Load all ontology files
    ontology_files = [
        'ontology.ttl',
        'disease_core.ttl',
        'diagnosis_core.ttl'
    ]
    
    graphs = []
    for file in ontology_files:
        if os.path.exists(file):
            print(f"Loading {file}...")
            g = load_ontology(file)
            graphs.append(g)
        else:
            print(f"Warning: {file} not found")
    
    if graphs:
        # Combine ontologies
        print("Combining ontologies...")
        combined = combine_ontologies(graphs)
        
        # Visualize
        print("Creating visualization...")
        visualize_ontology(combined)
    else:
        print("No ontology files found to combine")

if __name__ == "__main__":
    main() 