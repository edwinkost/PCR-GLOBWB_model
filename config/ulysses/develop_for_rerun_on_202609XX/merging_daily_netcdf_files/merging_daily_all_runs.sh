
#~ [edwingwt@int6 pcrglobwb_ulysses_2023-12-XX_rerun_on_202609]$ ls -lah
#~ total 3.0K
#~ drwxr-xr-x+ 6 edwin edwin 4.0K Oct 12 19:44 .
#~ drwxr-xr-x+ 5 edwin edwin 4.0K Oct 12 19:44 ..
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:52 emearth
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:45 era5land
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:44 mswep
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:54 w5e5

sbatch -J "era5land_merging" --export FORCING_NAME="era5land",FIRST_YEAR=1981,LAST_YEAR=2022 slurm_for_merging_daily_nc_files.sh
sbatch -J "emearth_merging" --export FORCING_NAME="emearth",FIRST_YEAR=1981,LAST_YEAR=2019 slurm_for_merging_daily_nc_files.sh
sbatch -J "mswep_merging" --export FORCING_NAME="mswep",FIRST_YEAR=1981,LAST_YEAR=2019 slurm_for_merging_daily_nc_files.sh
sbatch -J "w5e5_merging" --export FORCING_NAME="w5e5",FIRST_YEAR=1981,LAST_YEAR=2019 slurm_for_merging_daily_nc_files.sh
