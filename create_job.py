import os
import sys

traversals = ["lc_c01_3b", "lc_c04_3b", "lc_c08_3b", "lc_sliced_c02_3b", "lc_sliced_3b"]


def create_directory(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")


def create_yamls_in_directory(directory, spacing, box_size, cell_size):
    for traversal in traversals:
        yaml_file = os.path.join(directory, f"{traversal}.yaml")
        create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size)


def create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size):
    newton3 = "dis" if "c01" in traversal else "en"
    file_string = f'''\
container                            :  [LinkedCells] 
functor-3b                           :  axilrod-teller
traversal-3b                         :  [{traversal}] 
newton3-3b                           :  [{newton3}abled]
data-layout-3b                       :  [AoS]
verlet-rebuild-frequency             :  10
verlet-skin-radius-per-timestep      :  0.02
selector-strategy                    :  Fastest-Absolute-Value
tuning-strategies                    :  []
tuning-interval                      :  2000
tuning-samples                       :  3
tuning-max-evidence                  :  10
cutoff                               :  2.5
cell-size                            :  [{cell_size}]
deltaT                               :  0.002
iterations                           :  100
boundary-type                        :  [periodic, periodic, periodic]
fastParticlesThrow                   :  false
Sites:
  0:
    epsilon                          :  1.
    sigma                            :  1.
    mass                             :  1.
    nu                               :  0.073 # Value for Argon
Objects:
  CubeClosestPacked:
    0:
      box-length                     :  [{box_size[0]}, {box_size[1]}, {box_size[2]}]
      bottomLeftCorner               :  [0, 0, 0]
      particle-spacing               :  {spacing}
      velocity                       :  [0, 0, 0]
      particle-type-id               :  0

log-level                            :  warn
no-flops                             :  false
no-end-config                        :  true
no-progress-bar                      :  false
vtk-filename                         :  3BodyTest
vtk-output-folder                    :  3BodyTestOutput
vtk-write-frequency                  :  10
'''

    with open(yaml_file, 'w') as file:
        file.write(file_string)


def create_bash_script(directory, yaml_file, duration):
    script_content = f'''\
#!/bin/bash
#SBATCH -J 3btest
#SBATCH --get-user-env
#SBATCH --clusters=cm2_tiny
#SBATCH --partition=cm2_tiny
#SBATCH --nodes=1-1
#SBATCH --cpus-per-task=56
# 56 is the maximum reasonable value for CooLMUC-2
#SBATCH --mail-type=end
#SBATCH --mail-user=nanxingnick.deng@tum.de
#SBATCH --export=NONE
#SBATCH --time=00:{duration}:00

module load slurm_setup

cd $HOME

for num_threads in 1 2 4 8 16 32 56; do
    export OMP_NUM_THREADS=$num_threads
    AutoPas/build/examples/md-flexible/md-flexible --yaml-file coolmuc_md_flexible/{directory}/{yaml_file}
done
'''

    with open(f"{directory}/{yaml_file[:-5]}.sh", 'w') as file:
        file.write(script_content)


def create_bash_scripts(directory, duration):
    for traversal in traversals:
        create_bash_script(directory, f"{traversal}.yaml", duration)


def submit_sbatch(directory):
    os.chdir(directory)
    for traversal in traversals:
        os.system(f"sbatch {traversal}.sh")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <spacing> <box_size> <cell_size> <duration>")
        sys.exit(1)

    spacing = float(sys.argv[1])
    box_size = int(sys.argv[2])
    csf = float(sys.argv[3])
    duration = int(sys.argv[4])
    directory = f"spacing{spacing}_box{box_size}_CSF{csf}"

    create_directory(directory)
    create_yamls_in_directory(directory, spacing, [box_size, box_size, box_size], csf)
    print(f"Created YAML files in directory '{directory}' with spacing={spacing}, box_size={box_size}, cell_size={csf}")
    create_bash_scripts(directory, duration)
    print("Created bash scripts.")
    submit_sbatch(directory)
    print("Submitted sbatch.")
