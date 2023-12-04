import sys
import os
import yaml

def update_yamls_in_directory(directory, spacing, box_size, cell_size):
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            yaml_file = os.path.join(directory, filename)
            update_yaml_file(yaml_file, spacing, box_size, cell_size)

def update_yaml_file(yaml_file, spacing, box_size, cell_size):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    # Update values
    config['Objects']['CubeClosestPacked'][0]['box-length'] = box_size
    config['Objects']['CubeClosestPacked'][0]['particle-spacing'] = spacing
    config['cell-size'] = [cell_size]

    with open(yaml_file, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <directory> <spacing> <box_size> <cell_size>")
        sys.exit(1)

    directory = sys.argv[1]
    spacing = float(sys.argv[2])
    box_size = float(sys.argv[3])
    cell_size = int(sys.argv[4])

    update_yamls_in_directory(directory, spacing, [box_size, box_size, box_size], cell_size)
    print(f"Updated YAML files in directory '{directory}' with spacing={spacing}, box_size={box_size}, cell_size={cell_size}")
