import os
import sys


def create_directory(directory_name):
    directory_path = os.path.join(os.getcwd(), directory_name)

    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")


def create_yaml_in_directory(directory):
    yaml_file = os.path.join(directory, f"fallingDrop.yaml")
    create_yaml_file(directory)
    return yaml_file


def create_yaml_file(yaml_file):
    file_string = f'''\
container                        :  [LinkedCells]
verlet-rebuild-frequency         :  10
verlet-skin-radius-per-timestep  :  0.02
verlet-cluster-size              :  4
selector-strategy                :  Fastest-Absolute-Value
data-layout                      :  [AoS, SoA]
data-layout-3b                   :  [AoS]
traversal                        :  [ lc_c01, lc_c18, lc_c08, lc_sliced_c02, vl_list_iteration, vlc_c01, vlc_c18, vlc_sliced_c02, vcl_cluster_iteration, vcl_c01_balanced, vcl_c06 ] # Please see AllOptions.yaml for a comprehensive list of traversals
traversal-3b                     :  [lc_c01_3b, lc_c08_3b, lc_c04_3b, lc_sliced_3b, lc_sliced_c02_3b] # ds_sequential_3b
tuning-strategies                :  []
tuning-interval                  :  2500
tuning-samples                   :  3
tuning-max-evidence              :  10
functor                          :  Lennard-Jones AVX
functor-3b                       :  axilrod-teller

newton3                          :  [disabled, enabled]
newton3-3b                       :  [disabled, enabled]

cutoff                           :  3
box-min                          :  [0, 0, 0]
box-max                          :  [7.25, 7.25, 7.25]
cell-size                        :  [1.0, 0.5, 0.33, 0.25]
deltaT                           :  0.0005
iterations                       :  15000
boundary-type                    :  [reflective,reflective,reflective]
globalForce                      :  [0,0,-12]
Sites:
  0:
    epsilon                      :  1.
    sigma                        :  1.
    mass                         :  1.
Objects:
  # "water"
  CubeClosestPacked:
    0:  
      particle-spacing           :  1.122462048
      bottomLeftCorner           :  [1, 1, 1]
      box-length                 :  [48, 28, 10]
      velocity                   :  [0, 0, 0]
      particle-type-id           :  0
  Sphere:
    0:  
      center                     :  [18, 15, 30]
      radius                     :  6
      particle-spacing           :  1.122462048
      velocity                   :  [0, 0, 0]
      particle-type-id           :  0
# thermostat:
#   initialTemperature             :  1
#   targetTemperature              :  4
#   deltaTemperature               :  0.1
#   thermostatInterval             :  10
#   addBrownianMotion              :  false

log-level: warn
no-flops: false
no-end-config: true
no-progress-bar: false
vtk-filename: 3BodyTest
vtk-output-folder: 3BodyTestOutput
vtk-write-frequency: 1000
'''

    with open(yaml_file, 'w') as file:
        file.write(file_string)


def create_bash_script(directory):
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
#SBATCH --time=10:00:00

module load slurm_setup

cd $HOME

export OMP_NUM_THREADS=56
AutoPas/build2/examples/md-flexible/md-flexible --yaml-file coolmuc_md_flexible/{directory}/fallingDrop.yaml
'''

    with open(f"{directory}/{directory}.sh", 'w') as file:
        file.write(script_content)


def submit_sbatch(directory):
    os.chdir(directory)
    os.system(f"sbatch {directory}.sh")


if __name__ == "__main__":
    directory = "fallingDrop"
    create_directory(directory)
    yaml = create_yaml_in_directory(directory)
    print(f"Created YAML files in {directory}.")
    create_bash_script(directory)
    print("Created bash scripts.")
    #submit_sbatch(directory)
