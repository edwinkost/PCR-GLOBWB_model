import lue.framework as lfr
import numpy as np
import config
import meteo.potEvap as evap

def make_test_array(array_shape,partition_shape, min, max):

    array = lfr.create_array(array_shape=array_shape, partition_shape=partition_shape,dtype=np.dtype(np.float32), fill_value=1.0)
    array = (lfr.uniform(array, min, max) * array) / array

    return array

def ycoordinate(array_shape,partition_shape):

    lat_values = lfr.create_array(array_shape=array_shape, partition_shape=partition_shape,dtype=np.dtype(np.float32), fill_value=1.0)
    lat_values = lfr.uniform(lat_values, -90.0, 90.0)

    return lat_values

def doy(array_shape,partition_shape):

    doy = lfr.create_array(array_shape=array_shape, partition_shape=partition_shape,dtype=np.dtype(np.float32), fill_value=1.0)
    doy = lfr.uniform(doy, 0.0, 365.0)

    return doy


class data_classes():
    def __init__(self):
        self.lat_values = ycoordinate(config.arrayShape, config.partitionShape)
        self.doy = doy(config.arrayShape, config.partitionShape)
        self.temperature2m_K = make_test_array(config.arrayShape, config.partitionShape,-300 ,300)
        self.dewpoint2m_K = make_test_array(config.arrayShape, config.partitionShape,-300 ,300)
        self.surface_pressure_Pa = make_test_array(config.arrayShape, config.partitionShape, -300 ,300)
        self.surface_net_solar_radiation_J_m2 = make_test_array(config.arrayShape, config.partitionShape, -300 ,300)
        self.surface_net_thermal_radiation_J_m2 = make_test_array(config.arrayShape, config.partitionShape, -300 ,300)
        self.u10m_m_s = make_test_array(config.arrayShape, config.partitionShape, 0.0 ,10)
        self.v10m_m_s = make_test_array(config.arrayShape, config.partitionShape, 0.0 ,10)

def data():
    data = data_classes()
    return data

if __name__ == "__main__":
    data()