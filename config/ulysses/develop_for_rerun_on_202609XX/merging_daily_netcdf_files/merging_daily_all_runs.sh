
sbatch -J "emearth_merging" --export FORCING_NAME="emearth",FIRST_YEAR=1981,LAST_YEAR=2019 slurm_for_merging_daily_nc_files.sh

