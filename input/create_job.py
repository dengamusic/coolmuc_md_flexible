import sys
import os
import yaml

files = ["C01.yaml", "C04.yaml", "C08.yaml", "C02Sliced.yaml", "Sliced.yaml"]


def create_directory(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")


def create_yamls_in_directory(directory, spacing, box_size, cell_size):
    for filename in files:
        yaml_file = os.path.join(directory, filename)
        update_yaml_file(yaml_file, spacing, box_size, cell_size)


def update_yaml_file(yaml_file, spacing, box_size, cell_size):
    with open("input.yaml", 'r') as file:
        config = yaml.safe_load(file)

    # Update values
    config['Objects']['CubeClosestPacked'][0]['box-length'] = box_size
    config['Objects']['CubeClosestPacked'][0]['particle-spacing'] = spacing
    config['cell-size'] = [cell_size]

    with open(yaml_file, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <spacing> <box_size> <cell_size>")
        sys.exit(1)

    spacing = float(sys.argv[1])
    box_size = float(sys.argv[2])
    csf = float(sys.argv[3])
    directory = f"spacing{spacing}_box{box_size}_CSF{csf}"

    create_directory(directory)
    create_yamls_in_directory(directory, spacing, [box_size, box_size, box_size], csf)
    print(f"Created YAML files in directory '{directory}' with spacing={spacing}, box_size={box_size}, cell_size={csf}")
