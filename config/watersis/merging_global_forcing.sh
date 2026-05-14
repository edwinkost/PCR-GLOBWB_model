
#~ cyes@ac6-100.bullx:/ec/fws4/sb/project/C3SHydroGL/edwin/watersis_forcing/global/v20260514$ ls -lah source/1970/01/*
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/e_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/hurs_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 101M Apr 28 10:28 source/1970/01/pet_hargreaves_samani_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/pre_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/psl_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/rlds_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/rsds_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/sh_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/tas_day.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/tasmax_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/tasmin_0p1.nc
#~ -r-xr-x--x+ 1 nemk c3hygl 597M Apr 28 10:26 source/1970/01/wind_0p1.nc

#~ (pcrglobwb_python3) cyes@ac6-100.bullx:/ec/fws4/sb/project/C3SHydroGL/edwin/watersis_forcing/global/v20260514$ ls -lah
#~ total 12K
#~ drwxr-sr-x 2 cyes c3hygl 4.0K May 13 23:15 .
#~ drwxr-sr-x 3 cyes c3hygl 4.0K May 13 23:11 ..
#~ lrwxrwxrwx 1 cyes c3hygl   77 May 13 23:15 source -> /ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/

SOURCE_DIR="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/"

cdo -L -f nc4 -mergetime  ${SOURCE_DIR}/*/*/pet_hargreaves_samani_0p1.nc global_pet_hargreaves_samani_0p1_v20260514.nc &
cdo -L -f nc4 -mergetime  ${SOURCE_DIR}/*/*/pre_0p1.nc                   global_pre_0p1_v20260514.nc                   &        
cdo -L -f nc4 -mergetime  ${SOURCE_DIR}/*/*/tas_day.nc                   global_tas_day_0p1_v20260514.nc               &            
wait

#~ cdo -L -f nc4 -mergetime  ${SOURCE_DIR}/1970/*/pet_hargreaves_samani_0p1.nc test.nc

