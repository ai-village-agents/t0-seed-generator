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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T0 Seed Extractor CLI")
    parser.add_argument("--text", type=str, help="Text to extract seed from")
    parser.add_argument("--file", type=str, help="File to read text from")
    parser.add_argument("--type", type=str, default="structural", help="Memory type")
    
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
    print(json.dumps(result, indent=2))
