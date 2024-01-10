import os
import sys
import re

def parse_file(file_name, result):
    try:
        with open(file_name, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    # Define the regular expression pattern
    pattern = re.compile(
        r'traversal-3b\s+:  \[(.*)][\s\S]*?Using (\d+) Threads[\s\S]*?Total wall-clock time\s+: (\d+) ns[\s\S]*?GFLOPs +: +(\d+.\d+)[\s\S]*?GFLOPs\/sec +: +(\d+.\d+)[\s\S]*?Hit rate +: +(\d+.\d+)',
        re.MULTILINE
    )# Find all matches
    matches = pattern.findall(input_text)
    #print(matches)

    traversal_dict = {}
    cores_dict = {}
    gflops_dict = {}
    gflops_sec_dict = {}
    hit_rate_dict = {}
    [gflops_dict.setdefault(traversal, []).append(float(gflops)) for traversal, _, _, gflops, _, _ in matches]
    [gflops_sec_dict.setdefault(traversal, []).append(float(gflops_sec)) for traversal, _, _, _, gflops_sec, _ in matches]
    [hit_rate_dict.setdefault(traversal, []).append(float(hit_rate)) for traversal, _, _, _, _, hit_rate in matches]
    [traversal_dict.setdefault(traversal, []).append(int(time)) for traversal, _, time in matches]
    [cores_dict.setdefault(int(threads), []).append(None) for _, threads, _ in matches]

    # print
   # print("Traversals : {0}".format(list(traversal_dict)))
    #print("Cores used : {0}".format(list(cores_dict.keys())))
    #[print("{:<20} times in ns : {}".format(traversal, traversal_dict.get(traversal))) for traversal in traversal_dict.keys()]
    [print("{}_times = {}".format(traversal, traversal_dict.get(traversal))) for traversal in traversal_dict.keys()]
    [print("{}_gflops = {}".format(traversal, gflops_dict.get(traversal))) for traversal in traversal_dict.keys()]
    [print("{}_gflops_sec = {}".format(traversal, gflops_sec_dict.get(traversal))) for traversal in traversal_dict.keys()]
    [print("{}_hit_rate = {}".format(traversal, hit_rate_dict.get(traversal))) for traversal in traversal_dict.keys()]
    #[result + "{}_times = {}".format(traversal, traversal_dict.get(traversal)) for traversal in traversal_dict.keys()]



if len(sys.argv) != 2:
    print("Usage: python output_parser.py <directory>")
    sys.exit(1)

result = ""
directory = sys.argv[1]
for file in os.listdir(directory):
    if file.endswith(".out"):
        parse_file(f"{directory}/{file}", result)

print(result)