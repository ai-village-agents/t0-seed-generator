import re
import json
import argparse
from collections import Counter
import sys

def extract_seed(text, memory_type="structural"):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = {'the', 'a', 'and', 'of', 'to', 'in', 'i', 'it', 'was', 'on', 'with', 'for', 'my', 'that', 'this'}
    keywords = [w for w in words if w not in stopwords and len(w) > 4]
    common = [word for word, count in Counter(keywords).most_common(5)]
    hook = ' '.join(text.split()[:7])
    
    return {
        "seed": common,
        "type": memory_type,
        "hook": hook,
        "raw_string": f"SEED: [{', '.join(common)}] | TYPE: {memory_type} | REGENERATES: A memory about {memory_type} themes, centering on '{hook}...'"
    }

def compare_seeds(seed1, seed2):
    s1_set = set(seed1['seed'])
    s2_set = set(seed2['seed'])
    overlap = list(s1_set.intersection(s2_set))
    return {
        "seed1": seed1['seed'],
        "seed2": seed2['seed'],
        "overlap": overlap,
        "overlap_count": len(overlap),
        "jaccard_similarity": len(overlap) / len(s1_set.union(s2_set)) if s1_set.union(s2_set) else 0.0
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T0 Seed Extractor CLI")
    parser.add_argument("--text", type=str, help="Text to extract seed from")
    parser.add_argument("--file", type=str, help="File to read text from")
    parser.add_argument("--type", type=str, default="structural", help="Memory type")
    parser.add_argument("--compare", type=str, help="File to compare against the primary text/file")
    
    args = parser.parse_args()
    
    text = ""
    if args.file:
        try:
            with open(args.file, 'r') as f:
                text = f.read()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()
        
    if not text.strip():
        print(json.dumps({"error": "No text provided"}))
        sys.exit(1)
        
    result = extract_seed(text, args.type)
    
    if args.compare:
        try:
            with open(args.compare, 'r') as f:
                compare_text = f.read()
            compare_result = extract_seed(compare_text, args.type)
            comparison = compare_seeds(result, compare_result)
            result["comparison"] = comparison
        except Exception as e:
             result["comparison_error"] = str(e)

    print(json.dumps(result, indent=2))
