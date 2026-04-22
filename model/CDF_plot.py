# Quick CDF plotting to check data
# March 28
# JCS

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import datetime
import netCDF4 as nc

def readNetCDFAll(fileName, var_name):
    f = nc.Dataset(fileName)
    lat = f.variables["latitude"][:]
    lon = f.variables["longitude"][:]
    data = f.variables[var_name][:]
    time = f.variables["time"][:]
    t_unit = f.variables["time"].units
    t_cal = f.variables["time"].calendar
    tvalue = nc.num2date(time,units = t_unit,calendar = t_cal)
    dates = [i.strftime("%Y-%m-%d") for i in tvalue]
    #df = makeDataFrame(dates, data, "%Y-%m-%d", var_name)
    f.close()
    return(data, dates, lat, lon)
# read in files
turner_dir = '/scratch/depfg/steya001/global_05min_geodar_turner_250/subsets/'
rens_geodar_dir = '/scratch/depfg/steya001/global_05min_geodar_rens/subsets/'
baseline_dir = '/scratch/depfg/steya001/global_05min_baseline_final/subsets/'

# variables to evaluate
discharge = 'discharge_dailyTot_output.nc'
wb_storage = 'waterBodyStorage_monthEnd_output.nc'
rf_demand = 'sosreduction_demand_monthTot_output.nc'
rf_orig = 'sosreduction_dailyTot_output.nc'
sw_abstraction = 'surfaceWaterAbstraction_monthTot_output.nc'
sw_infiltration ='surfaceWaterInf_annuaTot_output.nc'

models = [turner_dir, rens_geodar_dir, baseline_dir]
model_name = ['turner_250', 'rens_geodar', 'baseline']
basin = "26"
latitude = 51.8619
longitude = 6.1186
latitude = 50.60690926	# dma near MOnschau
longitude = 6.388548675 # dam near Monscahu
data_plot = pd.DataFrame()
counter = 1

for model in models:

    if model == rens_geodar_dir or model == baseline_dir:
        rf = 'RensReduction_dailyTot_output.nc'
    else:
        rf = rf_orig
    file_name = model + "M"+ basin + "/netcdf/" +  wb_storage#sw_infiltration#sw_abstraction#rf# #discharge
    print(file_name)
    data = xr.open_dataset(file_name).sel(lat = latitude, lon = longitude, method = 'nearest').to_dataframe().reset_index()
    #data = pd.rename(data[''])
    if counter == 1:
        data_plot =data.iloc[:,[0,3]]
    else:
        data_plot = pd.merge(data_plot,data.iloc[:,[0,3]], how = 'outer', on = 'time')
        print('entered this')
    counter = counter +1

data_plot['soswater_reduction_factor'] = data_plot[data_plot['soswater_reduction_factor']] = 1
stat = 'count'
sn.ecdfplot(data_plot.iloc[:,1], stat=stat, label = model_name[0])
sn.ecdfplot(data_plot.iloc[:,2], stat=stat, label = model_name[1])
sn.ecdfplot(data_plot.iloc[:,3], stat=stat, label = model_name[2])
plt.legend()
plt.xlabel('WB storage ')
plt.title( 'Raw WB storage near Monscahu')

sn.histplot(data_plot.iloc[:,1], stat=stat, label = model_name[0])
sn.histplot(data_plot.iloc[:,2], stat=stat, label = model_name[1])
sn.histplot(data_plot.iloc[:,3], stat=stat, label = model_name[2])
plt.legend()
plt.xlabel('RF ')
plt.title( 'Raw Reduciton Factor CDF near Monscahu')

sn.histplot(x, stat=stat, cumulative=True, alpha=.4)












# looped values will work later but right now we need to hard code\
basins = ["26","44","51","02","13","47"]

#variables = [discharge, wb_storage, rf, rf_demand, sw_abstraction, sw_infiltration]
variables = [discharge]
models = [turner_dir, rens_geodar_dir, baseline_dir]
stat = "count"
for basin in basins: 
    for model in models:   
        for var in variables:
            file_name = model + "M"+ basin + "/netcdf/" + var
            print(file_name)
            data = xr.open_dataset(file_name)
            sn.histplot(data['discharge'], stat=stat, cumulative=True, alpha=.4)
