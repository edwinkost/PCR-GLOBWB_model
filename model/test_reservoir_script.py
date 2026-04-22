dam_file = '/data/hydroworld/pcrglobwb2_input_release/version_2019_11_beta/pcrglobwb2_input/global_05min/routing/surface_water_bodies/waterBodies5ArcMin.nc'

waterbodies = xr.open_dataset(dam_file)
filtered_waterbodies =waterbodies.sel(time = '2000-01-01')
netcdf_dams = filtered_waterbodies.to_netcdf()

clone_map_name = '/data/hydroworld/others/05ArcMinCloneMaps/new_masks_from_top/clone_M40.map'
pcr.setclone(clone_map_name)

waterbodyIds = vos.singleTryNetcdf2PCRobjClone(dam_file,varName='resMaxCapInp', dateInput = '2000-01-01',  cloneMapFileName =clone_map_name) # DOUBLE CHECK THIS



import xarray as xr 
import datetime
import virtualOS as vos # pull over the new virtual os from the local stuff
import pcraster as pcr
import numpy as np
conversion = 1e6
# read in file
file_name = '/scratch/steya001/reservoir_operations/Turner_netcdfs/Turner_all.nc'
nc_turner = xr.open_dataset(file_name) ## may need to change this to netcdf instead of xarray

year_val = 2000
month_val =10
day_val = 19
date = '2000-'+ str(month_val)+'-'+ str(day_val)
file_name = '/scratch/steya001/reservoir_operations/Turner_netcdfs_week/' + date +".nc"


flood_pcr = vos.singleTryNetcdf2PCRobjClone(file_name,varName='flood',  cloneMapFileName =clone_map_name) # DOUBLE CHECK THIS
conservation_pcr = vos.netcdf2PCRobjClone(file_name, 'conservation', cloneMapFileName =clone_map_name) # DOUBLE CHECK THIS
        
flood_orig_np = pcr.pcr2numpy(flood_pcr, mv = np.nan)
flood_non_zero = flood_orig_np[flood_orig_np>0]
conserve_orig_np = pcr.pcr2numpy(conservation_pcr, mv = np.nan)
conserve_non_zero = conserve_orig_np[conserve_orig_np >0]
         
#test_bounds = pd.DataFrame(np.repeat(variables.values, 7, axis=0)) # will need to remove this once we have the nc files created 

# DO EVERYTHIN AS XARRAY THEN WRITE TO NETCDF/PCRASTER AT THE END

flood_final = pcr.cover(flood_pcr, waterbodyIds) # fills in missing values in flood with waterbody cap

conservation_final = pcr.cover(conservation_pcr, waterbodyIds*0.1)

flood_final_np= pcr.pcr2numpy(flood_final, mv = np.nan)
flood_final_non_zero = flood_final_np[flood_final_np >0]

conservation_final_np= pcr.pcr2numpy(conservation_final, mv = np.nan)
conservation_final_non_zero = conservation_final_np[conservation_final_np >0]


# VALUES FOR THE MODEL
flood = pcr.cover(flood_pcr,  self.waterBodyCap)
#conservation = pcr.cover(pcr.ifthen(variables_pcr.flood < np.nan, v self.waterBodyCap*0.1))



#flood = filtered_turner['flood']*conversion
#conservation = test_bounds.iloc[day_val,2]*conversion
# gather previous storage 
#current_storage = self.waterBodyStorage + self.inflowInM3PerSec

# calculate water balance
# we would have to reconstruct release parameters which we don't have data for.....
demand = self.demand #self.demand?

### HOW TO CREATE ZEROS MAP
## HOW TO GET RELEASES


# make pcr map of the current storage, mv = -999 and the demand
current_storage = flood - conservation # makes it a pcr map so we can actually figure out how to do the thing
demand = current_storage /100 # makes another pcr map

if(pcr.boolean(current_storage > flood_final)):
    print('yes')

## HOW TO WRITE THESE>.....
reductionFactor = (current_storage -conservation)/(flood - conservation)
self.reductionFactor_turner = reductionFactor#
resvOutflow = reductionFactor * avgOutflow * length_of_time_step                      # unit: m3

release = flood -100
## Have to convert this logic to pcraster
new_storage = pcr.ifthen(current_storage < conservation, current_storage) # first if statement
release == ? # set releases to 0

new_storage = pcr.ifthen(current_storage >= conservation, pcr.ifthen(current_storage <= flood, value) )

difference = current_storage- flood
release = pcr.max(demand - difference, zeros_map) + difference
new_storage = current_storage - release


# if current_storage < conservation: # can't have 0 release so it will have to be the minimum release (ie environmental flow or demand)
#     release = 0
#     new_storage = current_storage
# if current_storage >= conservation and current_storage <= flood: # Active zone
#     release = self.inflow
#     reduction_factor = (current_storage -conservation)/(flood - conservation)
#     release = release *reduction_factor 
#     new_storage = current_storage - release
#     #   self.waterBodyStorage - self.minResvrFrac*self.waterBodyCap)/\
#     #      (self.maxResvrFrac - self.minResvrFrac)*self.waterBodyCap)
#     # based on average outflow
#     #   resvOutflow  = pcr.max(0, pcr.min(resvOutflow, self.avgInflow * length_of_time_step)) # unit: m3                                          
# if current_storage > flood: #STARFIT algorithm sets a desired release to draw storage back into range within one week and can be constrained to max release
#     difference = current_storage - flood
#     release = max(demand - difference, 0) + difference 
#     # if demand < difference:
#     #     release = difference
#     # else:
#     #     release = demand
#     new_storage = current_storage - release