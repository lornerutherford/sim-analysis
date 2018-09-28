# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 20:56:34 2017

@author: Paul Scherkl
"""
import numpy as np
import h5py
from dumps                  import Field
from dataReader.readerUtils import get_grid_data
import glob


def load_field(print_progress, pathToData, dumpNumber, fldList, gridData):
    """
    Main function to control field loading. 
    Creates a copy of the requested Field object, determines which loading routine to use (depending on user input), and loads data into new Field object
    Also, extracts grid information
    
    Parameters
    ----------
    pathToData: string, required
        Points to the folder where simulated files are located
            
    dumpNumber: int, required
        Current dump that will be loaded and processed
        
    fldList: list, required
        Contains [<species name>, <species obj>, <load switch>]
    
        
    gridData: dict, required
        Empty or partially filled dict that contains grid data
        
    Returns
    -------
    [Updated list of fields objects, gridData]
    """    
  
    from utils.miscUtils import copy_object
   
    loadedFldObjs = []
    
    for i in range(len(fldList)):
        speciesEntry = fldList[i]
        if speciesEntry[2]:
            speciesName = speciesEntry[0]
            newFldObj = copy_object(speciesEntry[1], Field() )
            
            
            
            
            #----------------------------------------------------------
            #     Junction for different loading methods
            #----------------------------------------------------------
            if speciesEntry[1].file_kind.lower() == "vsim":
                newFldObj, gridData = load_field_file_vsim( pathToData, dumpNumber, speciesName, newFldObj,gridData) 
            
            
            
            
            
            if isinstance(newFldObj, Field): # loading successful
                loadedFldObjs.append(newFldObj)
                if print_progress:
                        print "       " + speciesName + "_" + str(dumpNumber) + " loaded"
                        
            elif newFldObj == 0:
                print ("       (!) Warning: Cannot read field file " + speciesName + "_" + str(dumpNumber) + ", ignored")
            elif newFldObj == 1:
                print ("       (!) Warning: Field " + speciesName + "_" + str(dumpNumber) + ", not found, ignored")

    return loadedFldObjs, gridData





def load_field_file_vsim(pathToData, dumpNumber, currentSpecies, fldObj, gridData):
    """
    Field loading routine
    
    Parameters
    ----------
    pathToData: string, required
        Points to the folder where simulated files are located
            
    dumpNumber: int, required
        Current dump that will be loaded 
        
    currentSpecies: string, required
        Name of field that will be loaded
    
    gridData: dict, required
        Empty or partially filled dict that contains grid data
        
    Returns
    -------
    if loading successful:
        [Object of class Particles that contains the 3D maxtrix obtained from the dump file, gridData]  
    else:
        [error code, gridData]
    """    
    import scipy.constants as const
    
    for currentFile in  glob.glob(pathToData + "*" + currentSpecies + "_" + str(dumpNumber) + ".*") :
        if h5py.is_hdf5(currentFile):
            
            inStream = h5py.File(currentFile)

            if inStream.__contains__(currentSpecies):
                fldObj.fieldMatrix = np.array(inStream [ currentSpecies ], dtype=np.float64) 
            else:
                return 0, gridData
            
            if fldObj.kind == None: 
                if currentSpecies.lower().find("elec") == 0 or currentSpecies.lower().find("efield") == 0 or currentSpecies.lower().find("lasersplusplasma") > -1:
                    fldObj.kind = "electric"
                elif currentSpecies.lower().find("mag")  == 0 or currentSpecies.lower().find("bfield") == 0:
                    fldObj.kind = "magnetic"
                elif currentSpecies.lower().find("rho")  == 0:
                    fldObj.kind = "chargedens"
                elif currentSpecies.lower().find("j")  == 0:
                    fldObj.kind = "currdens"
                else: 
                    print ("       (!) Warning: Cannot determine kind of field " + currentSpecies + "_" + str(dumpNumber) + ". PicViz assumes electric field. Please set \"kind\" variable if necessary.")
                    fldObj.kind = "electric"
                   
            
            # do unit conversion here
            if fldObj.kind.lower() == "electric":
                fldObj.fieldMatrix = fldObj.fieldMatrix / 1.0e9
                
            if fldObj.kind.lower() == "chargedens":
                fldObj.fieldMatrix = fldObj.fieldMatrix /const.e
                
            if fldObj.kind.lower() == "fluid":
                fldObj.kind = "chargedens" # Note: treat species in plotting routines as particles/cubic meter
            
            
            
            if fldObj.component == None:
                fldObj.component = 0
                
            if fldObj.project == None:
                fldObj.project = 0

            if fldObj.show_colorbar == None:
                fldObj.show_colorbar = 1

            fldObj.labels  = inStream[ currentSpecies ].attrs["vsLabels"]
            gridData       = get_grid_data(inStream, gridData)
            inStream.close()
            
            fldObj.loaded = 1
            return fldObj, gridData
        
    return 1, gridData
            
            
            
