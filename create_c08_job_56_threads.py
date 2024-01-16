import os
import sys

traversals = ["lc_c08_3b"]


def create_directory(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")


def create_yamls_in_directory(directory, spacings, csf, box_size, iterations):
    files = []
    for traversal in traversals:
        for spacing in spacings:
            for cell_size in csf:
                yaml_file = os.path.join(directory, f"c08_{spacing}_{cell_size}.yaml")
                create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size, iterations)
                files.append(yaml_file)

    return files


def create_yaml_file(yaml_file, traversal, spacing, box_size, cell_size, iterations):
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
iterations                           :  {iterations}
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
no-progress-bar                      :  true
'''

    with open(yaml_file, 'w') as file:
        file.write(file_string)


def create_bash_script(directory, yamls, duration="01:00:00"):
    yamls_string = ""
    for yaml in  yamls:
        yamls_string += f"AutoPas/build/examples/md-flexible/md-flexible --yaml-file coolmuc_md_flexible/{yaml}\n"

    script_content = f'''\
#!/bin/bash
#SBATCH -J c08_spacing_ov
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

cd /dss/dsshome1/05/ge93quw2/

export OMP_NUM_THREADS=56
{yamls_string}
'''

    with open(f"{directory}/{yaml_file[:-5]}.sh", 'w') as file:
        file.write(script_content)


def create_bash_scripts(directory, yamls):
    for traversal in traversals:
        if "c01" in traversal:
            create_bash_script(directory, f"{traversal}.yaml", duration_c01)
        else:
            create_bash_script(directory, f"{traversal}.yaml", yamls)


def submit_sbatch(directory):
    os.chdir(directory)
    for traversal in traversals:
        os.system(f"sbatch {traversal}.sh")


if __name__ == "__main__":


    # spacing = float(sys.argv[1])
    # box_size = [int(i) for i in sys.argv[2].split(",")]
    # csf = float(sys.argv[3])
    # if csf < 1:
    #     traversals.remove("lc_c04_3b")
    # iterations = int(sys.argv[4])
    # duration = sys.argv[5]
    # duration_c01 = sys.argv[6]
    directory = "spacing_overlap_1010250"
    spacings = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    csf = [1, 0.5, 0.3333, 0.25, 0.2, 0.1667]
    box_size = [10, 10, 250]

    create_directory(directory)
    yamls = create_yamls_in_directory(directory, spacings, csf, box_size, iterations)
    print(f"Created YAML files")
    create_bash_scripts(directory, yamls)
    print("Created bash scripts.")
    #submit_sbatch(directory)
