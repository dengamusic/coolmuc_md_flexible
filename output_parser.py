import sys
import re

# if len(sys.argv) != 2:
#     print("Usage: python output_parser.py <filename>")
#     sys.exit(1)

# Get the filename from the command-line argument
file_name = "c08_vs_c01.txt" #sys.argv[1]

# Read the content of the file
try:
    with open(file_name, 'r') as file:
        input_text = file.read()
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
    sys.exit(1)

# Define the regular expression pattern
pattern = re.compile(
    r'traversal-3b\s+:  \[(.*)][\s\S]*?Using (\d+) Threads[\s\S]*?Total wall-clock time\s+: (\d+) ns',
    re.MULTILINE
)# Find all matches
matches = pattern.findall(input_text)
#print(matches)

traversal_dict = {}
cores_dict = {}
[traversal_dict.setdefault(traversal, []).append(int(time)) for traversal, _, time in matches]
[cores_dict.setdefault(int(threads), []).append(None) for _, threads, _ in matches]

# print
print("Traversals : {0}".format(list(traversal_dict)))
print("Cores used : {0}".format(list(cores_dict.keys())))
[print("{:<20} times in ns : {}".format(traversal, traversal_dict.get(traversal))) for traversal in traversal_dict.keys()]
