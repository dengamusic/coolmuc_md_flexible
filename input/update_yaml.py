import sys
import yaml


def update_yamls(input_yamls, spacing, box_size, cell_size):
    for yaml_file in input_yamls:
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
    if len(sys.argv) != 3:
        print("Usage: python script.py <spacing> <box_size> <cell_size>")
        sys.exit(1)

    spacing = float(sys.argv[1])
    box_size = float(sys.argv[2])
    cell_size = int(sys.argv[3])

    input_yamls = ["3BodyTestC01.yaml", "3BodyTestC04.yaml", "3BodyTestC08.yaml", "3BodyTestC02Sliced.yaml", "3BodyTestSliced.yaml"]

    update_yaml_file(input_yamls, spacing, [box_size, box_size, box_size], cell_size)
    print(f"Updated YAML files with spacing={spacing}, box_size={box_size}, cell_size={cell_size}")
