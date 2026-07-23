import numpy as np
from netCDF4 import Dataset

# ---------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------
outfile = "pet.nc"

# ---------------------------------------------------------------------
# Create NetCDF file
# ---------------------------------------------------------------------
nc = Dataset(outfile, "w", format="NETCDF4")

# ---------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------
ntime = 31
ny = 950
nx = 1000

nc.createDimension("time", None)   # Unlimited
nc.createDimension("y", ny)
nc.createDimension("x", nx)

# ---------------------------------------------------------------------
# Grid mapping variable
# ---------------------------------------------------------------------
crs = nc.createVariable("lambert_azimuthal_equal_area", "i4")

crs.semi_major_axis = 6378137.0
crs.EPSG_code = "EPSG:3035"
crs.latitude_of_projection_origin = 52.0
crs.inverse_flattening = 298.257223563
crs.longitude_of_projection_origin = 10.0
crs.proj4_params = (
    "+proj=laea +lat_0=52 +lon_0=10 "
    "+x_0=4321000 +y_0=3210000 "
    "+ellps=GRS80 +units=m +no_defs"
)
crs.false_northing = 3210000.0
crs.grid_mapping_name = "lambert_azimuthal_equal_area"
crs.false_easting = 4321000.0

# ---------------------------------------------------------------------
# Coordinate variables
# ---------------------------------------------------------------------
time = nc.createVariable("time", "i8", ("time",))
y = nc.createVariable("y", "f8", ("y",))
x = nc.createVariable("x", "f8", ("x",))

# Time attributes
time.standard_name = "time"
time.axis = "T"
time.calendar = "standard"
time.units = "days since 1990-01-01"

# X attributes
x.standard_name = "projection_x_coordinate"
x.long_name = "x coordinate of projection"
x.units = "Meter"
x.axis = "X"

# Y attributes
y.standard_name = "projection_y_coordinate"
y.long_name = "Y coordinate of projection"
y.units = "Meter"
y.axis = "Y"

# ---------------------------------------------------------------------
# PET variable
# ---------------------------------------------------------------------
pet = nc.createVariable(
    "pet",
    "f4",
    ("time", "y", "x"),
    fill_value=-9999.0,
    zlib=True,
    complevel=4,
)

pet.units = "mm"
pet.grid_mapping = "lambert_azimuthal_equal_area"

# ---------------------------------------------------------------------
# Example coordinate values
# Replace these with your own coordinates
# ---------------------------------------------------------------------
x[:] = np.arange(nx) * 1000.0
y[:] = np.arange(ny) * 1000.0

# Example time values (days since 1990-01-01)
time[:] = np.arange(ntime)

# ---------------------------------------------------------------------
# Example PET data
# Replace with your own data array of shape (31,950,1000)
# ---------------------------------------------------------------------
pet[:, :, :] = np.random.rand(ntime, ny, nx).astype(np.float32)

# ---------------------------------------------------------------------
# Optional global attributes
# ---------------------------------------------------------------------
nc.Conventions = "CF-1.8"

# ---------------------------------------------------------------------
# Close file
# ---------------------------------------------------------------------
nc.close()

print(f"Created {outfile}")
