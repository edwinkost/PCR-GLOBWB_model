#!/bin/bash 


sbatch -J 2005-2014_dynqual_merging --export START_YEAR=2005,END_YEAR=2014 merge_netcdf_example_sbatch.sh
sbatch -J 2015-2020_dynqual_merging --export START_YEAR=2015,END_YEAR=2020 merge_netcdf_example_sbatch.sh
sbatch -J 2021-2030_dynqual_merging --export START_YEAR=2021,END_YEAR=2030 merge_netcdf_example_sbatch.sh
sbatch -J 2031-2040_dynqual_merging --export START_YEAR=2031,END_YEAR=2040 merge_netcdf_example_sbatch.sh
sbatch -J 2041-2050_dynqual_merging --export START_YEAR=2041,END_YEAR=2050 merge_netcdf_example_sbatch.sh
sbatch -J 2051-2060_dynqual_merging --export START_YEAR=2051,END_YEAR=2060 merge_netcdf_example_sbatch.sh
sbatch -J 2061-2070_dynqual_merging --export START_YEAR=2061,END_YEAR=2070 merge_netcdf_example_sbatch.sh
sbatch -J 2071-2080_dynqual_merging --export START_YEAR=2071,END_YEAR=2080 merge_netcdf_example_sbatch.sh
sbatch -J 2081-2090_dynqual_merging --export START_YEAR=2081,END_YEAR=2090 merge_netcdf_example_sbatch.sh
sbatch -J 2091-2100_dynqual_merging --export START_YEAR=2091,END_YEAR=2100 merge_netcdf_example_sbatch.sh

#~ edwinoxy@tcn1176.local.snellius.surf.nl:/gpfs/work4/0/einf6448/users/dgraham/DynQual_DO_GFDL_SSP3RCP7$ ls -lah
#~ total 6.0K
#~ drwxr-s--- 12 dgraham prjs0584 4.0K Dec 15 10:48 .
#~ drwxr-s---  3 dgraham prjs0584 4.0K Nov  8 16:10 ..
#~ dr-xr-s--- 56 dgraham prjs0584 4.0K Nov 12 18:29 2005-2014
#~ dr-xr-s--- 56 dgraham prjs0584 4.0K Nov 15 05:37 2015-2020
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Nov 20 15:22 2021-2030
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Nov 24 20:41 2031-2040
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Nov 29 00:24 2041-2050
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Dec  3 02:55 2051-2060
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Dec  7 05:43 2061-2070
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Dec 11 07:41 2071-2080
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Dec 15 10:48 2081-2090
#~ drwxr-s--- 56 dgraham prjs0584 4.0K Dec 19 12:49 2091-2100
