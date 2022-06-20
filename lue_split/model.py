
import config
try:
    import lue.framework as lfr
    import luepcr as pcr
    print("LUE is USED.")
    pass

except:
    import pcraster as pcr
    print("PCRASTER is USED.")

import meteo.meteo as meteo
import pre_process.input

import time
    
@lfr.runtime_scope
def main():

    landSurfaceData = pre_process.input.landSurfaceData()
    meteoData = pre_process.input.meteoData()
    statesData = pre_process.input.statesData()
    gridData = pre_process.input.gridData()

    startTime = time.time()
    actualET = 0.0

    for i in range(0,10):
        meteo_module = meteo.Meteo(landSurfaceData, meteoData, statesData, gridData)

        actualET = actualET + meteo_module.actualET


        # GET RUNTIME
        if i == 9: 
            actualET_max = pcr.max(actualET, 1.0)
            set_brake = pcr.pcr2numpy(actualET_max, config.MV)

            try:
                if set_brake.all() == set_brake.all():
                    endTime = time.time() - startTime
                    print(endTime) 
            except: 
                if set_brake == set_brake:
                    endTime = time.time() - startTime
                    print(endTime)
            

if __name__ == "__main__":
    main()