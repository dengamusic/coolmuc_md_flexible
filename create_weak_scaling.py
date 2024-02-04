import os
import sys

traversals = ["lc_c01_3b", "lc_c04_3b", "lc_c08_3b", "lc_sliced_c02_3b", "lc_sliced_3b"]
threads = [1, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56]
length_1_thread = 13.5
def create_directory(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")


def create_yamls_in_directory(directory, spacing, box_size, cell_size):
    yamls = []
    longest_axis = [length_1_thread * t - spacing for t in threads]
    for axis in longest_axis:
        for traversal in traversals:
            yaml_file = os.path.join(directory, f"{traversal}_{axis}.yaml")
            create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size, axis)
            yamls.append(yaml_file)
    return yamls


def create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size, axis):
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
deltaT                               :  0
iterations                           :  10
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
      box-length                     :  [{box_size[0]}, {box_size[1]}, {axis}]
      bottomLeftCorner               :  [0, 0, 0]
      particle-spacing               :  {spacing}
      velocity                       :  [0, 0, 0]
      particle-type-id               :  0
'''

    with open(yaml_file, 'w') as file:
        file.write(file_string)


def create_bash_script(directory, duration, yamls):

    script_content = f'''\
#!/bin/bash
#SBATCH -J {directory}
#SBATCH --get-user-env
#SBATCH --clusters=cm2_tiny
#SBATCH --partition=cm2_tiny
#SBATCH --nodes=1-1
#SBATCH --cpus-per-task=56
# 56 is the maximum reasonable value for CooLMUC-2
#SBATCH --mail-type=end
#SBATCH --mail-user=nanxingnick.deng@tum.de
#SBATCH --export=NONE
#SBATCH --time={duration}

module load slurm_setup

cd $HOME
'''
#     for num_threads in 1 4 8 12 16 20 24 28 32 36 40 44 48 52 56; do
#     export
#     OMP_NUM_THREADS =$num_threads
#
#
# '''
    longest_axis = [length_1_thread * t - spacing for t in threads]
    job_string = 'AutoPas/build/examples/md-flexible/md-flexible --yaml-file coolmuc_md_flexible/'
    for i in range(threads.__len__()):
        script_content += f"export OMP_NUM_THREADS={threads[i]}\n"
        for traversal in traversals:
            yaml_file = os.path.join(directory, f"{traversal}_{longest_axis[i]}.yaml")
            script_content += job_string + yaml_file + "\n"

    with open(f"{directory}/{directory}.sh", 'w') as file:
        file.write(script_content)


def submit_sbatch(directory):
    os.chdir(directory)
    os.system(f"sbatch {directory}.sh")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <spacing> [<box_size>] <cell_size> <duration>")
        sys.exit(1)

    spacing = float(sys.argv[1])
    # box_size = [int(i) for i in sys.argv[2].split(",")]
    box_size = [length_1_thread, length_1_thread, 56 * length_1_thread]
    csf = float(sys.argv[3])
    if csf < 1:
        traversals.remove("lc_c04_3b")
    duration = sys.argv[4]
    directory = f"weak_s{spacing}_box{box_size[0]}{box_size[1]}{box_size[2]}_CSF{csf}"

    create_directory(directory)
    box_size = [length_1_thread - spacing, length_1_thread - spacing, 0]
    yamls = create_yamls_in_directory(directory, spacing, box_size, csf)
    print(f"Created YAML files in directory '{directory}' with spacing={spacing}, box_size={box_size}, cell_size={csf}")
    create_bash_script(directory, duration, yamls)
    print("Created bash scripts.")
    submit_sbatch(directory)
