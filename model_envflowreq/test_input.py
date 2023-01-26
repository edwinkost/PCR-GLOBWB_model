import os
import virtualOS as vos

def main():

    inputpath = 'data/hydroworld/pcrglobwb2_input_release/version_2019_11_beta_extended/pcrglobwb2_input'
    variable_name = 'discharge'
    
    for filename in ['/home/beek0120/Projects/PCRGLOBWB/PCR-GLOBWB_model/model_envflowreq/data/EFR_1958-1999.nc', \
                     '/home/beek0120/Projects/PCRGLOBWB/PCR-GLOBWB_model/model_envflowreq/data/EFR_constant_1958-1999.map', \
                     '/home/beek0120/Projects/PCRGLOBWB/PCR-GLOBWB_model/model_envflowreq/data/EFR_constant_1958-1999.nc', \
                     'None', None]:
    
        is_spatial, is_temporal, \
           number_time_steps = vos.test_file_structure(inputpath, \
                                   filename, \
                                   variable_name)
    
        print(filename, is_spatial, is_temporal, \
           number_time_steps)


if __name__ == "__main__":

    main()
