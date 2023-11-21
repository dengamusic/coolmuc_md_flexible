import re

# Specify the file name
file_name = "c08_vs_c01.txt"

# Read the content of the file
with open(file_name, 'r') as file:
    input_text = file.read()

# Define the regular expression pattern
pattern = re.compile(r'Using (\d+) Threads[\s\S]*?Total wall-clock time\s+: (\d+) ns', re.MULTILINE)

# Find all matches
matches = pattern.findall(input_text)

# Display the results
for i, (threads_used, wall_time_ns) in enumerate(matches, start=1):
    print(f"Block {i}: Threads Used = {threads_used}, Time = {wall_time_ns} ns")
