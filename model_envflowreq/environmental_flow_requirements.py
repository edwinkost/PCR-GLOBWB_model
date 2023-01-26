import os
import sys
import logging

import pcraster as pcr

import virtualOS as vos

# set the logger
logger = logging.getLogger(__name__)


# set default minimum gradient to assure there are no zero values for
# the gradient.
default_gradmin = 1.0e-6
default_include_hmod = True

# set NoneType
NoneType = type(None)

#####################
# specific functions #
# used by the class #
#####################
def discharge_manning(h, mannings_n, channel_gradient, \
                      channel_width, gradmin = default_gradmin, \
                      shallow_flow_approximation = False):


    wetted_area = h * channel_width
    if shallow_flow_approximation:

        hydraulic_radius = h

    else:

        hydraulic_radius = pcr.ifthenelse(wetted_area > 0, \
                  wetted_area / (channel_width + 2 * h), \
                  pcr.scalar(0))

    return  hydraulic_radius ** (2.0 / 3.0) * \
            pcr.max(channel_gradient, gradmin) ** 0.5 * \
            wetted_area / mannings_n


# TODO: make names of the channel parameters correspond with the
# rest of the module
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

    # calculate the estimated height from the discharge
    h_est = pcr.scalar(mannings_n * q)
    return  pcr.ifthenelse((h_est > 0) & (width > 0), \
                            (h_est / (pcr.max(gradmin, gradient) ** 0.5 * \
                                      width)) ** 0.6, 0)


class environmental_flow_requirements(object):

    """environmental_flow_requirements: class object of the PCR-GLOBWB \
model that holds and updates information on the environmantal flow \
requirements,
Environmental flow requirements in PCR-GLOBWB are defined in terms of the \
discharge rate and the associated water depths estimated using the \
shallow flow approximation and Manning's equation.

Environmental flow requirements can be set in two limits, an upper \
limit, that ideally is preserved, and a lower limit that must be \
maintained.
In the case of streams, the limit is defined in terms of the reserved \
water depth to maintain the environmental flow and that falls between \
the lower and the upper limit, and which varies with the surface \
water demand.
In the case of reservoirs, the limit is defined in terms of the discharge \
and varies between the upper and the lower limit depenndent on the \
avaiable storage and the reservoir storage limits.

"""

    def __str__(self):

        # TODO: this can be a generic function to be called
        # with the correct arguments for each module

        selected_setting_names = ['is_spatial', 'is_temporal', \
                                  'allow_year_substitution', \
                                  'number_time_steps', 'data', \
                                  'variable_name']

        message_str = str.join(' ', \
                          ('Environmental flow requirements are included', \
                           'with the following settings:'))

        var_name    = 'limit_based_on_discharge_ratio'
        message_str = str.join('', \
                              (message_str, \
                               '\n\t%-32s: %s' % (var_name, \
                                                   str(getattr(self, var_name)))))

        for var_name in self.variable_info.keys():

            message_str = str.join('', \
                        (message_str, '\n\t', var_name))

            # iterate over the settings
            for setting_name, entry_name in self.variable_info[var_name].items():

                if setting_name in selected_setting_names:

                    message_str = str.join('', \
                                      (message_str, \
                                       '\n\t%-32s: %s' % (setting_name, \
                                                       str(entry_name))))

        return message_str


    def __init__(self, configuration):

        # initialize the object
        object.__init__(self)

        # set the information to process the input
        inputpath = configuration.globalOptions['inputDir']

        # identify the relevant config_section
        if 'routing' in vars(configuration).keys():
            config_section = 'routing'
        elif 'routingOptions' in vars(configuration).keys():
            config_section = 'routingOptions'
        else:
            sys.exit('Environmental flow requirements cannot be set from config file')

        # downward compatibility
        # NOTE: for PCR-GLOBWB3 this should be specified at the main
        # level, facilitating the use of old-style data
        # set the synonyms to read in old-style input;
        # this can be streamlined by including this information per
        # section in the configuration file; in that case, only
        # a generic section and a specific section need to be processed
        # without to much unnecessary, void iterations over the names
        # and aliases.
        name_and_aliases = {'discharge_lower_limit_variable_name' : \
                                        ['qlim_variable_name', \
                                         'efr_variable_name', \
                                         'envFlowVarName'], \
                            'discharge_upper_limit_variable_name' : \
                                        ['qmod_variable_name', \
                                         'efr_variable_name', \
                                         'envFlowVarName'], \
                            'discharge_lower_limit_data'          : \
                                        ['efr_qlim_filename', \
                                         'envFlowLimNC'], \
                            'discharge_upper_limit_data'          : \
                                        ['efr_qmod_filename', \
                                         'envFlowModNC'], \
                            'limit_based_on_discharge_ratio'      : \
                                         ['dischargeBasedEnvironmentalFlow']}

        # variable settings per input field
        self.variable_info = { \
             'discharge_lower_limit_input'     :  \
                            {'variable_name'           : 'discharge_lower_limit_variable_name', \
                             'units'                   : 'm**3/s', \
                             'data'                    : 'discharge_lower_limit_data', \
                             'is_spatial'              : False, \
                             'is_temporal'             : False, \
                             'number_time_steps'       : 0, \
                             'allow_year_substitution' : True, \
                             'data_type'               : pcr.Scalar, \
                             'correction_constant'     : 0.00, \
                             'correction_factor'       : 1.00, \
                             'default_value'           : 0.00, \
                             'valid_range'             : [0, None], \
                             }, \
             'discharge_upper_limit_input'     : \
                            {'variable_name'           : 'discharge_upper_limit_variable_name', \
                             'units'                   : 'm**3/s', \
                             'data'                    : 'discharge_upper_limit_data', \
                             'is_spatial'              : False, \
                             'is_temporal'             : False, \
                             'number_time_steps'       : 0, \
                             'allow_year_substitution' : True, \
                             'data_type'               : pcr.Scalar, \
                             'correction_constant'     : 0.00, \
                             'correction_factor'       : 1.00, \
                             'default_value'           : 0.00, \
                             'valid_range'             : [0, None], \
                             }, \
                            }

        # TODO: replace this with a generic function that
        # returns the correct input from the parsed config file
        # that can be incorporated in the different modules
        # check on the input:
        settings_info = {}
        for name, aliases in name_and_aliases.items():

            entry_name = None

            for alias in aliases:

                if alias in getattr(configuration, config_section).keys():

                    entry_name = alias

            # set the values: there are three options:
            # no match has been defined, and the result is None;
            # the entry is None; or, a specific entry value is given.

            if not isinstance(entry_name, NoneType):

                settings_info[name] = getattr(configuration, \
                                          config_section)[entry_name]

                if settings_info[name].lower() == 'none':
                    settings_info[name] = None

            else:

                settings_info[name] = entry_name

        # set the information on the nature of the limit
        var_name    = 'limit_based_on_discharge_ratio'
        setattr(self, var_name, settings_info[var_name])

        # process the configuration using the dictionary with the
        # information on the retrieved settings
        for var_name in self.variable_info.keys():

            # iterate over the settings
            for setting_name, entry_name in self.variable_info[var_name].items():

                if isinstance(entry_name, str) and \
                              entry_name in settings_info.keys():

                    # set the entry
                    self.variable_info[var_name][setting_name] = \
                                  settings_info[entry_name]

            # check on the data type
            if 'data' in self.variable_info[var_name].keys():

                # set the information
                is_spatial, is_temporal, \
                   number_time_steps = vos.test_file_structure(inputpath, \
                                           self.variable_info[var_name]['data'], \
                                           self.variable_info[var_name]['variable_name'])

                self.variable_info[var_name]['is_spatial']  = is_spatial
                self.variable_info[var_name]['is_temporal'] = is_temporal
                self.variable_info[var_name]['number_time_steps'] = number_time_steps

                # set the data
                setattr(self, var_name,
                        vos.input_field( \
                            name                    = var_name, \
                            variable_name           = self.variable_info[var_name]['variable_name'], \
                            units                   = self.variable_info[var_name]['units'], \
                            data                    = self.variable_info[var_name]['data'], \
                            is_spatial              = self.variable_info[var_name]['is_spatial'], \
                            is_temporal             = self.variable_info[var_name]['is_temporal'], \
                            number_time_steps       = self.variable_info[var_name]['number_time_steps'], \
                            allow_year_substitution = self.variable_info[var_name]['allow_year_substitution'], \
                            data_type               = self.variable_info[var_name]['data_type'], \
                            correction_constant     = self.variable_info[var_name]['correction_constant'], \
                            correction_factor       = self.variable_info[var_name]['correction_factor'], \
                            default_value           = self.variable_info[var_name]['default_value'], \
                            valid_range             = self.variable_info[var_name]['valid_range'], \
                            ))

        # set the water depths associated with the limits of the environmental flow
        # as well as the reserved water depth, the discharge and volume
        # TODO: make the names more transparent and in agreement
        # with the naming conventions
        self.discharge_lower_limit        = None
        self.discharge_upper_limit        = None
        self.discharge_reserved_limit     = None
        self.waterdepth_lower_limit       = None
        self.waterdepth_upper_limit       = None
        self.waterdepth_reserved_limit    = None
        self.channelvolume_reserved_limit = None

        # returns None
        return None

    def update_depth_limits(self, qlim, qmod, \
                            mannings_n, channel_gradient, channel_width):

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
    hlim                : lower -hard- limit of the environmental flow
                          requirement in [m];
    hmod                : upper -soft- limit of the environmental flow
                          requirement in [m]; note that hmod is greater
                          or equal to hlim and both values are larger or
                          equal to 0.

        '''
        # Convert the discharge limits to height limits
        hlim = approximate_shallow_flow_depth(qlim, mannings_n, \
                                                        channel_gradient, \
                                                        channel_width)
        hmod = approximate_shallow_flow_depth(qmod, mannings_n, \
                                                        channel_gradient, \
                                                        channel_width)

        # returns None
        return hlim, hmod

    def estimate_reserved_volume(self, \
                                 hlim, hmod,
                                 channel_volume, \
                                 pot_withdrawal, \
                                 mannings_n, \
                                 channel_gradient, \
                                 channel_depth, \
                                 channel_width, \
                                 surface_water_area, \
                                 ):
        '''
estimate_reserved_volume: function that calculates the water \
height available for human demand in [m].

    Input:
    ======
    hlim                : lower -hard- limit of the environmental flow
                          requirement in [m];
    hmod                : upper -soft- limit of the environmental flow
                          requirement in [m]; note that hmod is greater
                          or equal to hlim and both values are larger or
                          equal to 0;
    channel_volume      : channel storage [m3] for the current time
                          step;
    pot_withdrawal:     : the potential surface water withdrawal [m3]
                          for the current time step;
    mannings_n          : Mannings coefficient for the river;
    channel_gradient    : the gradient of the channel [m/m];
    channel_depth       : channel depth [m];
    channel_width       : the width of the channel [m];
    surface_water_area  : surface water area [m2].

    Output:
    =======
    reserved_depth,
    reserved_flow        : the depth and the corresponding flow that is
                          available amount of water
                          that is available for abstractions without
                          breaching the environmental flow requirement;
    message_str         : string denoting the update.

        '''
        # set the message string
        message_str = ''

        # get the volumes based on the
        # surface water area

        # get the corresponding depth for the channel storage
        # and the potential withdrawal
        hchannel    = pcr.min(channel_depth, \
                              channel_volume / surface_water_area)
        hwithdrawal = pot_withdrawal / surface_water_area

        # get the claim on the negotiable depth
        # of the environmental flow
        hclaim = pcr.max(0, pcr.min(hwithdrawal, \
                            hwithdrawal - hchannel + hmod, \
                            hmod - hlim))
        hres = hlim + (hmod - hlim) * pcr.ifthenelse(hmod - hlim > 0, \
                       pcr.max(0, 1 - 0.5 * hclaim / (hmod - hlim)), 0)

        # add the reserved discharge, using the depth as hydraulic radius
        qres   = discharge_manning(hres, \
                                   mannings_n, channel_gradient, \
                                   channel_width, \
                                   shallow_flow_approximation = True)

        # return the values of the reserved depth,
        # and discharge, as well as the message string
        return hres, qres, message_str


    def update(self, date, \
                     channel_volume, \
                     pot_withdrawal, \
                     mannings_n, \
                     channel_gradient, \
                     channel_width, \
                     channel_depth, \
                     channel_length, \
                     water_body_relative_storage, \
                     surface_water_area, \
                     water_body_id, \
                     water_body_outlet, \
                     water_body_type, \
                     landmask, \
                     clone_filename, \
                     temppath,
                     inputpath):

        self.discharge_lower_limit, message_str = \
            self.discharge_lower_limit_input.update( \
                                                    date, \
                                                    landmask, \
                                                    clone_filename, \
                                                    temppath,
                                                    inputpath)
        logger.debug(message_str)

        self.discharge_upper_limit, message_str = \
            self.discharge_upper_limit_input.update( \
                                                    date, \
                                                    landmask, \
                                                    clone_filename, \
                                                    temppath,
                                                    inputpath)
        logger.debug(message_str)

        # set the environmental flow reserved water depth
        # the set function can be automated by checking the type of the
        # variable (input_field_class) and updating the value using the
        # set_attr function on the self of the class instance iterating
        # over the argumentes in the kwargs. This misses, however, the
        # additional checks that qlim <= qmod and this should be tested
        # in the update method of the instance instead

        # check on the qlim / qmod
        self.discharge_upper_limit = pcr.ifthenelse( \
                self.discharge_upper_limit < self.discharge_lower_limit, \
                self.discharge_lower_limit, self.discharge_upper_limit)

        # set the water depths for the limits
        self.waterdepth_lower_limit = approximate_shallow_flow_depth( \
                                        q          = self.discharge_lower_limit, \
                                        mannings_n = mannings_n, \
                                        gradient   = channel_gradient, \
                                        width      = channel_width)

        self.waterdepth_upper_limit = approximate_shallow_flow_depth( \
                                    q              = self.discharge_upper_limit, \
                                    mannings_n     = mannings_n, \
                                    gradient       = channel_gradient, \
                                    width          = channel_width) 

        # compute the reserved water depth and volume in relation
        # to the potential withdrawal from surface water; this is
        # the same for all types of surfce water (rivers, lakes, reservoirs)
        self.waterdepth_reserved_limit, self.discharge_reserved_limit, \
            message_str = \
                        self.estimate_reserved_volume( \
                            hlim               = self.waterdepth_lower_limit, \
                            hmod               = self.waterdepth_upper_limit, \
                            channel_volume     = channel_volume, \
                            pot_withdrawal     = pot_withdrawal, \
                            mannings_n         = mannings_n, \
                            channel_gradient   = channel_gradient, \
                            channel_depth      = channel_depth, \
                            channel_width      = channel_width, \
                            surface_water_area = surface_water_area)

        # update the water depth and discharge limit for the water bodies
        # first, update the discharge for the outlet of the reservoirs
        # and estimate the corresponding water depth
        discharge_reserved_limit  = self.discharge_lower_limit + \
                                    water_body_relative_storage * \
                                    (self.discharge_upper_limit -  \
                                     self.discharge_lower_limit)
        waterdepth_reserved_limit = approximate_shallow_flow_depth( \
                                    q          = discharge_reserved_limit, \
                                    mannings_n = mannings_n, \
                                    gradient   = channel_gradient, \
                                    width      = channel_width)
        
        # update the values of the reserved discharge and the corresponding
        # water depth for reservoirs
        self.discharge_reserved_limit  = pcr.ifthenelse(water_body_type == 2, \
                                             discharge_reserved_limit, \
                                             self.discharge_reserved_limit)
        self.waterdepth_reserved_limit = pcr.ifthenelse(water_body_type == 2, \
                                             waterdepth_reserved_limit, \
                                             self.waterdepth_reserved_limit)
        
        # next, extrapolate the values over the water bodies;
        # note that the values for water bodies become zero if
        # the lakes are endorheic.
        self.discharge_reserved_limit  = pcr.ifthenelse(water_body_type == 0, \
                                self.discharge_reserved_limit, \
                                pcr.areamaximum(pcr.ifthenelse(water_body_outlet != 0, \
                                                    self.discharge_reserved_limit, 0), \
                                                water_body_id))

        self.waterdepth_reserved_limit = pcr.ifthenelse(water_body_type == 0, \
                                self.waterdepth_reserved_limit, \
                                pcr.areamaximum(pcr.ifthenelse(water_body_outlet != 0, \
                                                    self.waterdepth_reserved_limit, 0), \
                                                water_body_id))

        # ~ and volume; the reserved volume is set to zero
        # for reservoirs in order to avoid limitations of the abstract-
        # ions.
        # TODO: add the reservoir storage to allow for the local with-
        # drawal.
        self.channelvolume_reserved_limit = pcr.ifthenelse( \
                           water_body_type == 2, \
                           pcr.scalar(0), self.waterdepth_reserved_limit * \
                           surface_water_area)

        # returns None
        return None


# add the test of the class
# in the main
def main():

    # no tests are included in the main module of the environmental
    # flow requirements
    pass

if __name__ == "__main__":

    main()
    sys.exit('all done')


