import json
import sys

file = sys.argv[1]
with open(file,'r') as f:
    print(len(json.load(f)))