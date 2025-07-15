from owlready2 import get_ontology, sync_reasoner, onto_path
import os

# Set the path to your ontology files
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ontologies'))
onto_path.append(os.path.join(base_dir, 'phenotype'))
onto_path.append(os.path.join(base_dir, 'disease'))

# Load phenotype ontology first (so imports resolve)
phenotype_onto = get_ontology(f"file://{onto_path[0]}/phenotype_core.ttl").load()
disease_onto = get_ontology(f"file://{onto_path[1]}/disease_core.ttl").load()

# Run the reasoner (requires Java)
with disease_onto:
    sync_reasoner()  # Uses HermiT by default

# Check for SeverityLevel class
SeverityLevel = None
for cls in disease_onto.classes():
    if cls.name == "SeverityLevel":
        SeverityLevel = cls
        break

print("SeverityLevel found in disease ontology:", SeverityLevel is not None)

# Check for individuals
for label in ["Mild", "Moderate", "Severe"]:
    found = False
    for ind in disease_onto.individuals():
        if ind.name == label:
            found = True
            print(f"Individual '{label}' found in disease ontology.")
    if not found:
        print(f"Individual '{label}' NOT found in disease ontology.")

# Optionally, print all subclasses/individuals of SeverityLevel
if SeverityLevel:
    print("Individuals of SeverityLevel:")
    for ind in SeverityLevel.instances():
        print(" -", ind) 