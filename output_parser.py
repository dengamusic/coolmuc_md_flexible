import glob
import os
import sys
import re


def parse_file(file_name, lexika):
    try:
        with open(file_name, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    # Define the regular expression pattern
    pattern = re.compile(
        r'traversal-3b\s+:  \[(.*)][\s\S]*?Using (\d+) Threads[\s\S]*?One iteration +: +(\d+)[\s\S]*?Total wall-clock time\s+: (\d+) ns[\s\S]*?GFLOPs +: +(\d+.\d+)[\s\S]*?GFLOPs\/sec +: +(\d+.\d+)[\s\S]*?Hit rate +: +(\d+.\d+)',
        re.MULTILINE
    )# Find all matches
    matches = pattern.findall(input_text)
    #print(matches)

    [traversal_dict, cores_dict, gflops_dict, gflops_sec_dict, hit_rate_dict, times_per_iteration_dict] = lexika
    [gflops_dict.setdefault(traversal, []).append(float(gflops)) for traversal, _, _, _, gflops, _, _ in matches]
    [gflops_sec_dict.setdefault(traversal, []).append(float(gflops_sec)) for traversal, _, _, _, _, gflops_sec, _ in matches]
    [hit_rate_dict.setdefault(traversal, []).append(float(hit_rate)) for traversal, _, _, _, _, _, hit_rate in matches]
    [traversal_dict.setdefault(traversal, []).append(int(time)) for traversal, _, _, time, _, _, _ in matches]
    [cores_dict.setdefault(int(threads), []).append(None) for _, threads, _, _, _, _, _ in matches]
    [times_per_iteration_dict.setdefault(traversal, []).append(int(time_per_iteration)) for traversal, _, time_per_iteration, _, _, _, _ in matches]



def parse_directory(directory):
    traversal_dict = {}
    times_per_iteration_dict = {}
    cores_dict = {}
    gflops_dict = {}
    gflops_sec_dict = {}
    hit_rate_dict = {}
    lexika = [traversal_dict, cores_dict, gflops_dict, gflops_sec_dict, hit_rate_dict, times_per_iteration_dict]
    for file in sorted(os.listdir(directory)):
        if file.endswith(".out"):
            parse_file(f"{directory}/{file}", lexika)

    print("Total Wall Clock Times:")
    [print("{}_times = {}".format(traversal, traversal_dict.get(traversal))) for traversal in traversal_dict.keys()]

    print("\nTimes per Iteration:")
    [print("{}_times = {}".format(traversal, times_per_iteration_dict.get(traversal))) for traversal in
     traversal_dict.keys()]

    print("\nGFLOPs:")
    [print("{}_gflops = {}".format(traversal, gflops_dict.get(traversal))) for traversal in traversal_dict.keys()]

    print("\n:GFLOPs/sec")
    [print("{}_gflops_sec = {}".format(traversal, gflops_sec_dict.get(traversal))) for traversal in
     traversal_dict.keys()]

    print("\nHit Rates:")
    [print("{}_hit_rate = {}".format(traversal, hit_rate_dict.get(traversal))) for traversal in traversal_dict.keys()]


# if 1 argument is given, parse that file
if len(sys.argv) == 2:
    parse_directory(sys.argv[1])
else:
    for dir_name in glob.glob('spacing*/'):
        print(dir_name)
        parse_directory(dir_name)
        print("\n\n")
            # You can add your code here to open and process each file
            # For example, to read the file:
            # with open(file_name, 'r') as file:
            #     contents = file.read()
            #     print(contents)
