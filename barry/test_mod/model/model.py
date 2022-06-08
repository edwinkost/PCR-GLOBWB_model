import lue.framework as lfr

import meteo.meteo as meteo

@lfr.runtime_scope
def main():

    pet = meteo.evap()
    print(lfr.to_numpy(pet))

if __name__ == "__main__":
    main()

#TODO timesteps loop