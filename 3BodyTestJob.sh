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
#SBATCH --time=00:20:00

module load slurm_setup
module load cmake/3.21.4
module load gcc/11.2.0

cd $HOME

cd AutoPas/build
cmake ..
make md-flexible -j
make runTests -j
ctest -R TraversalComparison3B

cd $HOME

for num_threads in 32 56; do
        export OMP_NUM_THREADS=$num_threads
        AutoPas/build/examples/md-flexible/md-flexible --yaml-file AutoPas/examples/md-flexible/input/3BodyTest.yaml
done
