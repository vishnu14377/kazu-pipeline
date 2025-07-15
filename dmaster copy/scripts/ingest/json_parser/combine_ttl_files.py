import os
import sys
import re
import glob
import argparse

def escape_literals(content):
    """Escape newlines in literals to make them valid RDF."""
    lines = content.split('\n')
    result = []
    in_literal = False
    current_literal = []
    
    for line in lines:
        # Check if we're starting a literal
        if '"' in line and not in_literal:
            parts = line.split('"', 1)
            result.append(parts[0])  # Add the part before the literal
            in_literal = True
            current_literal = [parts[1]]
        # Check if we're ending a literal
        elif '"' in line and in_literal:
            parts = line.split('"', 1)
            current_literal.append(parts[0])
            # Join the literal parts and escape newlines
            literal = ' '.join(current_literal).replace('\n', '\\n')
            result.append(f'"{literal}"{parts[1]}')
            in_literal = False
            current_literal = []
        # We're in the middle of a literal
        elif in_literal:
            current_literal.append(line)
        # Regular line
        else:
            result.append(line)
    
    return '\n'.join(result)

def combine_ttl_files(input_dir, output_file):
    """Combine multiple TTL files into a single file."""
    ttl_files = sorted(glob.glob(os.path.join(input_dir, '*.ttl')))
    
    if not ttl_files:
        print(f"No TTL files found in {input_dir}")
        return
    
    # Helper to check if a line is a valid, complete triple
    def is_valid_triple_line(line):
        line = line.strip()
        if not line:
            return False
        # Skip lines that start with a quote (orphaned literal)
        if line.startswith('"'):
            return False
        # Skip incomplete rdfs:label lines
        if line.endswith('rdfs:label') or line.endswith('rdfs:label '):
            return False
        # Only allow lines that start with a valid subject and have at least two spaces and end with a period
        if (line.startswith(':') or line.startswith('<') or ':' in line.split(' ')[0]) and line.count(' ') >= 2 and line.endswith('.'):
            return True
        return False
    
    # Read and process all files
    all_prefixes = set()
    all_triples = set()
    
    for ttl_file in ttl_files:
        with open(ttl_file, 'r') as f:
            content = f.read()
            escaped_content = escape_literals(content)
            lines = escaped_content.split('\n')
            
            # Collect prefixes
            for line in lines:
                line = line.strip()
                if line.startswith('@prefix'):
                    all_prefixes.add(line)
            
            # Collect triples
            for line in lines:
                line = line.strip()
                if is_valid_triple_line(line):
                    all_triples.add(line)
    
    # Write the combined file
    with open(output_file, 'w') as out:
        # Write prefixes
        for prefix in sorted(all_prefixes):
            out.write(prefix + '\n')
        out.write('\n')
        
        # Write triples
        for triple in sorted(all_triples):
            out.write(triple + '\n')
    
    print(f"Successfully combined TTL files into {output_file}")

def main():
    """Main function to combine TTL files."""
    input_dir = "output/ttl"
    output_file = "output/combined_cohorts.ttl"
    
    try:
        combine_ttl_files(input_dir, output_file)
    except Exception as e:
        print(f"Error combining TTL files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 