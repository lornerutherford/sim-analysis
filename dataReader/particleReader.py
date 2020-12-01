# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""

import h5py
import numpy as np
import scipy.constants as const
import glob
from dumps                  import Particles
from dataReader.readerUtils import get_grid_data
from utils.miscUtils        import copy_object

def load_particles(print_progress, pathToData, dumpNumber, ptclList, loadedPtclObjs, gridData):
    """
    Main function to control particle loading
    Creates a copy of the requested Particles object, determines which loading routine to use (depending on user input), and loads data into new Particles object
    Also, extracts grid information
    
    
    Parameters
    ----------
    pathToData: string, required
            Points to the folder where simulated files are located
            
    dumpNumber: int, required
        Current dump that will be loaded and processed
        
    ptclList: list, required
        
    gridData: dict, required
        Empty or partially filled dict that contains grid data
        
    Returns
    -------
    [A list of particle objects, gridData]
    """    

    
    for ptcl in ptclList:
        if ptcl.load:
            newPtclObj = copy_object(ptcl, Particles() )
            
            
            #----------------------------------------------------------
            #     Junction for different loading methods
            #----------------------------------------------------------
            if ptcl.file_kind.lower() == "vsim":
                newPtclObj, gridData = load_particles_file_vsim( pathToData, dumpNumber, ptcl.name,  newPtclObj, gridData )
            
            
            
            if isinstance(newPtclObj, Particles):    # loading successful
                
                from dumps.dumpUtils.particlesUtils import make_particles_cuts
                make_particles_cuts(newPtclObj)
                if len(newPtclObj.X) == 0:
                    newPtclObj.loaded = 0
                    if print_progress:
                        print("       " + ptcl.name + "_" + str(dumpNumber) + " loaded, but empty due to cuts, ignored")
                else: 
                    newPtclObj.loaded = 1
                    loadedPtclObjs.append(newPtclObj)
                    if print_progress:
                        print("       " + ptcl.name + "_" + str(dumpNumber) + " loaded")
                
            elif newPtclObj == 0:
                print ("       (!) Warning: Cannot read particle file " + ptcl.name + "_" + str(dumpNumber) + ", ignored")
                
            elif newPtclObj == 1:
                print ("       (!) Warning: Particles " + ptcl.name + "_" + str(dumpNumber) + " not found, ignored")

    return loadedPtclObjs, gridData



def load_particles_file_vsim(pathToData, dumpNumber, speciesName, ptclObj, gridData):
    """
    Particle loading routine
    
    Parameters
    ----------
    pathToData: string, required
            Points to the folder where simulated files are located
            
    dumpNumber: int, required
        Current dump that will be loaded 
        
    speciesName: string, required
        Name of particles that will be loaded
    
    ptclObj: Particles, required
        Object of type Particles. It's phase space is updated with loaded file
    
    gridData: dict, required
        Empty or partially filled dict that contains grid data
       
    Returns
    -------
    if loading successful:
        [ Object of class Particles that contains the 6D phase space obtained from the dump file, gridData]
    else:
        [error code, gridData]
    """    
    
    for currentFile in  glob.glob(pathToData + "*" + speciesName + "*_" + str(dumpNumber) + ".h5") :
        if h5py.is_hdf5(currentFile):
            inStream = h5py.File(currentFile,"r")
            try:
                speciesMatrix = np.array(inStream[ speciesName ])
            except:
                return 0, gridData
            
            try: ptclObj.labels = inStream[ speciesName ].attrs["vsLabels"].split(",")
            except: ptclObj.labels = {}

            try:  NDIM =    inStream[ speciesName ].attrs["numSpatialDims"]
            except:       NDIM = 3
            
            try:      ptclObj.numPtclsInMacro = inStream[ speciesName ].attrs["numPtclsInMacro"]
            except: pass

            if "globalGridGlobalLimits" in inStream.keys():
                ptclObj.xLab = inStream["globalGridGlobalLimits"].attrs["vsLowerBounds"][0]*1e6
            elif "compGridGlobalLimits" in inStream.keys():
                ptclObj.xLab = inStream["compGridGlobalLimits"].attrs["vsLowerBounds"][0]*1e6
            else:
                ptclObj.xLab = 0
            gridData = get_grid_data(inStream, gridData)
            inStream.close()


            ptclObj.X      = speciesMatrix[:,0]  *1e6 - ptclObj.xLab
            ptclObj.Y      = speciesMatrix[:,1]*1e6
            
            if NDIM == 3:
                ptclObj.Z      = speciesMatrix[:,2]*1e6
                ptclObj.PX     = speciesMatrix[:,3]   
                ptclObj.PY     = speciesMatrix[:,4]
                ptclObj.PZ     = speciesMatrix[:,5]
            elif NDIM == 2:
                ptclObj.Z      =  np.zeros(len(ptclObj.X))
                ptclObj.PX     = speciesMatrix[:,2]   
                ptclObj.PY     = speciesMatrix[:,3]
                ptclObj.PZ     = speciesMatrix[:,4]
            
            
            if speciesName + "_tag" in ptclObj.labels:
                ptclObj.Tag = speciesMatrix[:,ptclObj.labels.index(speciesName + "_tag")]
            else:
                try:    ptclObj.Tag = speciesMatrix[:, 6]
                except: ptclObj.Tag    = np.ones(len(ptclObj.X))
                
            if speciesName + "_weight" in ptclObj.labels:
                ptclObj.Weight = speciesMatrix[:, ptclObj.labels.index(speciesName + "_weight")]
            else:
                try:    ptclObj.Weight = speciesMatrix[:, 7]
                except: ptclObj.Weight    = np.ones(len(ptclObj.X))
                
            if np.max(ptclObj.PX) > 0:
                ptclObj.YP     = ptclObj.PY / ptclObj.PX * 1000
                ptclObj.ZP     = ptclObj.PZ / ptclObj.PX * 1000
                ptclObj.YP[np.isnan(ptclObj.YP)] = 0.
                ptclObj.ZP[np.isnan(ptclObj.ZP)] = 0.
            else:
                ptclObj.YP     = np.zeros(len(ptclObj.PY))
                ptclObj.ZP     = np.zeros(len(ptclObj.PZ))
                
            ptclObj.T      = ptclObj.X / const.speed_of_light * 1e9
            ptclObj.T      = np.max(ptclObj.T) - ptclObj.T
            gammaCol        = np.sqrt((ptclObj.PX**2 + ptclObj.PY**2 + ptclObj.PZ**2)/(const.speed_of_light**2))
            eMassInMeV = const.value("electron mass energy equivalent in MeV"  )
            ptclObj.E  = eMassInMeV*(np.sqrt(1 + gammaCol**2) - 1)
            ptclObj.EX = eMassInMeV*(np.sqrt(1 + (ptclObj.PX / const.speed_of_light)**2) - 1)   
            ptclObj.EY = eMassInMeV*(np.sqrt(1 + (ptclObj.PY / const.speed_of_light)**2) - 1)   
            ptclObj.EZ = eMassInMeV*(np.sqrt(1 + (ptclObj.PZ / const.speed_of_light)**2) - 1)   
            ptclObj.Etrans = np.sqrt(ptclObj.EY**2 + ptclObj.EZ**2)
            return ptclObj, gridData
    
    return 1, gridData
    

        
    


