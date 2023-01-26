import os
import sys
import pcraster as pcr

# Import settings
import test_settings as ts

# Set default minimum gradient to assure there are no zero values for
# the gradient.
default_gradmin = 1.0e-6
default_include_hmod = True

## TO-DO:
## - Write function to limit abstraction with hmod and hlim (DONE)
## - Accept input to determine if hmod is incorporated or only hard limit (DONE)
## - If only hard limit -> use Q90 for the hard limit (DONE)
## - If soft limit -> use Q90 for soft, Q95 for hard
## - Make sure that qlim, qmod and discharge are loaded per timestep

from spatialDataSet2PCR import setClone, \
                               spatialAttributes, \
                               spatialDataSet

def approximate_shallow_flow_depth(q, mannings_n, gradient, width, \
                                  gradmin = default_gradmin):
                                      
    '''
approximate_shallow_flow_depth: function that calculates the water \
height in a channel from the discharge, gradient, mannings n and \
the channel width.

    Input:
    ======
    q                   : lower -hard- limit of the environmental flow
                          requirement in [m3/s];
    mannings_n          : upper -soft- limit of the environmental flow
                          requirement in [m3/s];
    mannings_n          : Mannings coefficient for the river;
    gradient            : the gradient of the channel;
    width               : the width of the channel;
    gradmin             : the minimum gradient in order to assure a
                          non-zero gradient, standard = 1.0e-6;


    Output:
    =======
    height              : returns the water height in the channel given
                          that the height and width are larger than
                          zero.

    '''
    
    # Calculate the estimated height from the discharge
    h_est = mannings_n * q
    return  pcr.ifthenelse((h_est > 0) & (width > 0), \
                            (h_est / (pcr.max(gradmin, gradient) ** 0.5 * \
                                      width)) ** 0.6, 0)

class env_flow_req(object):

    def __init__(self, include_envFlow):

        object.__init__(self)

        # include the environmental flow or not, as specified in the init
        assert isinstance(include_envFlow, bool), 'only boolean variable allowed'
        self.include_envFlow = include_envFlow

        # initialize the environmental flow requirement with settings
        # from the settings (ts) python file
        self.qlim = pcr.spatial(pcr.scalar(ts.qlim))
        self.qmod = pcr.spatial(pcr.scalar(ts.qmod))
        
        # returns None
        return None

    def update_q_env_flow_req(self, qlim, qmod):

        '''
update_q_env_flow_req: function intrinsic to the class environflowreq \
that sets the hard and flexible limit (resp. qlim and qmod) to the \
environmental flow requirements.

    Input:
    ======
    qlim                : lower -hard- limit of the environmental flow
                          requirement in [m3/s];
    qmod                : upper -soft- limit of the environmental flow
                          requirement in [m3/s];

    Output:
    =======
    None                : returns None, sets the discharge of the envir-
                          onmental flow requirements internally.

        '''
        
        # Check if the given limits are already a scalar field
        # If this is not the case, make a scalar field
        if not isinstance(qlim, pcr.Field):
            self.qlim = pcr.spatial(pcr.scalar(qlim))
            
        if not isinstance(qmod, pcr.Field):
            self.qmod = pcr.spatial(pcr.scalar(qmod))
        
        
        
        ## I have already added the pcr.spatial & pcr.scalar in the __init__ section
        ## Therefore it might not be necesarry to check here once again.
        
        
        
        # If the given limits are a scalar field they can be assigned
        self.qlim = qlim
        self.qmod = qmod

        # returns None
        return None

    def update_h_env_flow_req(self, \
                            mannings_n, gradient, width):
        
        '''
update_h_env_flow_req: function intrinsic to the class environflowreq \
that converts  and updates the hard and flexible limit (resp. qlim \
and qmod) to the height in [m] instead of discharge in [m3/s].

    Input:
    ======
    qlim                : lower -hard- limit of the environmental flow
                          requirement in [m3/s];
    qmod                : upper -soft- limit of the environmental flow
                          requirement in [m3/s];
    mannings_n          : Mannings coefficient for the river;
    gradient            : the gradient of the channel
    width               : the width of the channel

    Output:
    =======
    None                : returns None, sets the discharge of the envir-
                          onmental flow requirements internally.

        '''
        # Convert the discharge limits to height limits
        self.hlim = approximate_shallow_flow_depth(self.qlim, mannings_n, \
                                                       gradient, width)
        self.hmod = approximate_shallow_flow_depth(self.qmod, mannings_n, \
                                                       gradient, width)

        # returns None
        return None
        
    def estimate_volume_after_envFlow(self, discharge, mannings_n, \
                                      gradient, width, include_hmod = \
                                      default_include_hmod):
        '''
estimate_volume_after_envFlow: function that calculates the water \
height available for human demand in [m]. 

    Input:
    ======
    discharge           : the discharge for the current timestep [m3/s];
    mannings_n          : Mannings coefficient for the river;
    gradient            : the gradient of the channel
    width               : the width of the channel
    include_hmod        : accepts Boolean input and determines if the \
                          soft limit is included or not.

    Output:
    =======
    abstractableVolume  : the amount of water that is available for \
                          abstractions without breaching the environ- \
                          mental flow requirement.

        '''
        # Make sure the discharge is transformed to height as well
        self.discharge_height = approximate_shallow_flow_depth(discharge,\
                                                              mannings_n,\
                                                              gradient,\
                                                              width)
        # Check if hmod is included
        if include_hmod == True:
            # Use formula with soft cap
            self.readAvlChannelStorage = pcr.max(0, self.discharge_height - self.hmod) \
                                      + pcr.max(0, (pcr.min(self.hmod, self.discharge_height)-self.hlim) \
                                      * ((self.discharge_height-0.5* \
                                      (self.hlim+self.hmod))/self.discharge_height))
            
        elif include_hmod == False:
            # Use hard limit
            self.readAvlChannelStorage = pcr.max(0, self.discharge_height - self.hlim)
        
        else:
            sys.exit("include_hmod should be Boolean.")
        
        # returns the amount of water available for extraction once
        # the environmental flow requirement has been met.
        return self.readAvlChannelStorage


# ~ ## TO-DO:
# ~ ## - Make sure qlim and qmod are loaded in and not hard coded

# ~ # add the test of the class
# ~ # in the main
# ~ def main():

    # ~ # set the map for the clone and the channel geometry
    # ~ inputpath = '/data/hydroworld/pcrglobwb2_input_release/version_2019_11_beta_extended/pcrglobwb2_input/'
    # ~ clone_filename = '/home/6148379/PCR-GLOBWB_model/clone_landmask_maps/clone_danube.map'
    # ~ channelwidth_filename    = os.path.join(inputpath, \
                                      # ~ 'global_05min/routing/channel_properties/bankfull_width.nc')
    # ~ channelmannings_n       = 0.04
    # ~ channelgradient_filename = os.path.join(inputpath, \
                                      # ~ 'global_05min/routing/channel_properties/channel_gradient.nc')
    # ~ channeldepth_filename    = os.path.join(inputpath, \
                                      # ~ 'global_05min/routing/channel_properties/bankfull_depth.nc')
    # ~ qlim_filename = '/scratch/6148379/pcrglobwb2_output/05min/data/EFR_1958-1999.nc'
    # ~ discharge_filename = '/scratch/6148379/pcrglobwb2_output/05min/WATCH_Human_1960-1999/netcdf/discharge_dailyTot_output.nc'


    # ~ # get the spatial attributes and set the clone
    # ~ clone_attributes = spatialAttributes(clone_filename)
    # ~ setClone(clone_attributes)

    # ~ # read in the channel properties
    # ~ channelwidth    = getattr(spatialDataSet('cwidth', channelwidth_filename, \
                                  # ~ 'FLOAT32', 'SCALAR', \
                                  # ~ clone_attributes.xLL, \
                                  # ~ clone_attributes.xUR, \
                                  # ~ clone_attributes.yLL, \
                                  # ~ clone_attributes.yUR, \
                                  # ~ clone_attributes.xResolution, \
                                  # ~ clone_attributes.yResolution, \
                                  # ~ pixels = clone_attributes.numberCols, \
                                  # ~ lines  = clone_attributes.numberRows), 'cwidth')
    # ~ channelgradient = getattr(spatialDataSet('grad', channelgradient_filename, \
                                  # ~ 'FLOAT32', 'SCALAR', \
                                  # ~ clone_attributes.xLL, \
                                  # ~ clone_attributes.xUR, \
                                  # ~ clone_attributes.yLL, \
                                  # ~ clone_attributes.yUR, \
                                  # ~ clone_attributes.xResolution, \
                                  # ~ clone_attributes.yResolution, \
                                  # ~ pixels = clone_attributes.numberCols, \
                                  # ~ lines  = clone_attributes.numberRows), 'grad')
    # ~ channeldepth   = getattr(spatialDataSet('cdepth', channeldepth_filename, \
                                  # ~ 'FLOAT32', 'SCALAR', \
                                  # ~ clone_attributes.xLL, \
                                  # ~ clone_attributes.xUR, \
                                  # ~ clone_attributes.yLL, \
                                  # ~ clone_attributes.yUR, \
                                  # ~ clone_attributes.xResolution, \
                                  # ~ clone_attributes.yResolution, \
                                  # ~ pixels = clone_attributes.numberCols, \
                                  # ~ lines  = clone_attributes.numberRows), 'cdepth')
    # ~ qlim = 1000
    # ~ discharge = 3000
    # ~ # soft limit should be larger then the hard cap
    # ~ qmod = qlim*2

    # ~ my_efr = envFlowReq(ts.include_envFlow)

    # ~ my_efr.update_q_env_flow_req(qlim, qmod)
    # ~ my_efr.update_h_env_flow_req(channelmannings_n,\
                                # ~ channelgradient, channelwidth)
    
    # ~ readAvlChannelStorage = my_efr.estimate_volume_after_envFlow(discharge, channelmannings_n,\
                                                              # ~ channelgradient, channelwidth)
    # ~ pcr.aguila(readAvlChannelStorage)

if __name__ == "__main__":

    main()
    sys.exit('all done')


