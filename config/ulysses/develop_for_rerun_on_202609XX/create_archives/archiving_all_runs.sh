
#~ [edwingwt@int6 pcrglobwb_ulysses_2023-12-XX_rerun_on_202609]$ ls -lah
#~ total 3.0K
#~ drwxr-xr-x+ 6 edwin edwin 4.0K Oct 12 19:44 .
#~ drwxr-xr-x+ 5 edwin edwin 4.0K Oct 12 19:44 ..
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:52 emearth
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:45 era5land
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:44 mswep
#~ dr-xr-xr-x+ 3 edwin edwin 4.0K Oct 12 19:54 w5e5

sbatch -J "era5land_archiving" --export FORCING_NAME="era5land" slurm_for_create_archives.sh
sbatch -J "emearth_archiving" --export FORCING_NAME="emearth" slurm_for_create_archives.sh
sbatch -J "mswep_archiving" --export FORCING_NAME="mswep" slurm_for_create_archives.sh
sbatch -J "w5e5_archiving" --export FORCING_NAME="w5e5" slurm_for_create_archives.sh


