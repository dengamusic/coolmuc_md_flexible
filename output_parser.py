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
pattern = re.compile(r'Using (\d+) Threads[\s\S]*?Total wall-clock time\s+: (\d+)', re.MULTILINE)

# Find all matches
matches = pattern.findall(input_text)

grouped_dict = {}
[grouped_dict.setdefault(threads, []).append(time) for threads, time in matches]
zipped_result = list(zip(*list(grouped_dict.values())))
print("Cores used : {0}".format(list(grouped_dict.keys())))
# print(list(grouped_dict.values()))
print(zipped_result)
