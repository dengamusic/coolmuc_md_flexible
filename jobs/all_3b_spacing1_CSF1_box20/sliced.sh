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
#SBATCH --time=00:30:00

module load slurm_setup

cd $HOME

for num_threads in 1 2 4 8 16 32 56; do
        export OMP_NUM_THREADS=$num_threads
        AutoPas/build/examples/md-flexible/md-flexible --yaml-file coolmuc_md_flexible/input/all_3b_spacing1_CSF1/3BodyTestSliced.yaml
done
