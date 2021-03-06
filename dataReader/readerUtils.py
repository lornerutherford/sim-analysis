# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""

import h5py
import numpy as np
import glob






def set_load_switches(plotters, analyzers):
    import itertools
    
    def iterate(obj):
        try:
            for ptclObj in obj.particles:
                    if ptclObj.plot_data or ptclObj.lines: 
                        ptclObj.load = 1
                        continue
        except: pass                    
        try:
            for fldObj in obj.fields:
                if fldObj.plot_data or fldObj.lines: 
                    fldObj.load = 1
                    continue
        except: pass                    

    for obj in itertools.chain(plotters, analyzers):
        try:
            for plotter in obj.plotters:
                iterate(plotter)
        except:
            iterate(obj)
    return plotters, analyzers




def load_data(print_progress, print_gridData, pathToData,  dumpNumber, plotters, analyzers):
    """
    Utility function that cordinates loading of particles, fields, and grid data
    
    """
    from dataReader.particleReader      import load_particles
    from dataReader.fieldReader         import load_field
    import itertools
    
    currentGridData = {}
    particleObjList = []
    fieldObjList    = []
    
    
    for obj in itertools.chain(plotters, analyzers):
        try:
            for plotter in obj.plotters:
                try:
                    particleObjList, currentGridData = load_particles(print_progress, pathToData, dumpNumber, plotter.particles, particleObjList, currentGridData)
                except: pass
        
                try:
                    fieldObjList,   currentGridData  = load_field(print_progress, pathToData, dumpNumber, plotter.fields, fieldObjList,currentGridData)
                except: pass
        except:
                try:
                    particleObjList, currentGridData = load_particles(print_progress, pathToData, dumpNumber, obj.particles, particleObjList, currentGridData)
                except: pass
        
                try:
                    fieldObjList,   currentGridData  = load_field(print_progress, pathToData, dumpNumber, obj.fields, fieldObjList,currentGridData)
                except: pass
            


            
    
    
    if print_gridData and currentGridData:
        print("\n       -------- Grid Data ---------")
        for key in currentGridData:
            print("       " + key + " = " + str(currentGridData[key]))
        print("       ----------------------------\n")
    
    return particleObjList, fieldObjList, currentGridData







def get_meta_data(print_metaData, pathToData, plotters, analyzers):
    """
    Main function to control meta data loading
    
    Parameters
    ----------
    pathToData: string, required
        Points to the folder where simulated files are located
        
    particleSwitchList: dict, required
        Checks if file shall be loaded
        
    fields: list, required
        Fields names that will be processed
        
    fieldSwitchList: dict, required
        Checks if file shall be loaded
        
    Returns
    -------
    dict filled with beautiful meta data       
    """    
    if print_metaData:
        import itertools
        metaData = {}
        
   
        for obj in itertools.chain(plotters, analyzers):
            try:
                for ptcl in obj.particles:
                    if ptcl.load:
                        metaData = load_meta_data(pathToData, ptcl.name, metaData)
                        break
            except: pass
        
            try:
                for fld in obj.fields:
                    if fld.load:
                        metaData = load_meta_data(pathToData, fld.name, metaData)
                        break
            except: pass
                        
                
            
        print("\n       -------- Meta Data --------")
        for key in metaData:
            print("       " + key + " = " + str(metaData[key]))
        print("       ---------------------------\n")


        return metaData




def load_meta_data(pathToData, currentSpecies, metaData):
    """
    Loading function for meta data.
    Checks for certain keywords and tries to extract them from dump file. 
    
    Parameters
    ----------
    pathToData: string, required
        Points to the folder where simulated files are located
        
    
    currentSpecies: string, required
        Name of species
        
    metaData: dict, required
        empty or partially filled dict that will be extended by this function
        
        
    Returns
    -------
    dict filled with beautiful meta data       
    """    
    for currentFile in  glob.glob(pathToData + "*" + currentSpecies + "*") :
        
        if h5py.is_hdf5(currentFile):
            inStream = h5py.File(currentFile, "r")
            
                
            if not "PICName" in metaData:
                if inStream.__contains__("runInfo"):
                    metaData["PICName"] = inStream["runInfo"].attrs["vsSoftware"] + " v. " +  inStream["runInfo"].attrs["vsSwVersion"] 
                    
    return metaData

    
    
def get_grid_data(h5Stream, gridData):
    """
    Loading function for grid data.
    Checks for certain keywords and tries to extract them from dump file. 
    
    Parameters
    ----------
    h5Stream: h5py file stream, required
        Currently opened file stream 
        
    
    gridData: dict, required
        empty or partially filled dict that will be extended by this function
        
        
    Returns
    -------
    dict filled with beautiful grid data       
    """    
    boxLimitKey = "globalGridGlobalLimits" if h5Stream.__contains__("globalGridGlobalLimits") else "compGridGlobalLimits" if h5Stream.__contains__("compGridGlobalLimits") else "update grid data reader"
    boxGridKey  = "globalGridGlobal"       if h5Stream.__contains__("globalGridGlobal")       else "compGridGlobal" if h5Stream.__contains__("compGridGlobal") else "update grid data reader"
    
    
    if not "NDIM" in gridData:
        if h5Stream.__contains__(boxLimitKey):
            gridData["NDIM"] = len( h5Stream[boxLimitKey].attrs["vsLowerBounds"] )

            
    if not "boxSize" in gridData:
        if h5Stream.__contains__(boxLimitKey):
            lowers = h5Stream[boxLimitKey].attrs["vsLowerBounds"]
            uppers = h5Stream[boxLimitKey].attrs["vsUpperBounds"]
            gridData["boxSize"] = ( uppers - lowers )* 1e6

    if not "numCells" in gridData:
        if h5Stream.__contains__(boxGridKey):
            gridData["numCells"] = h5Stream[boxGridKey].attrs["vsNumCells"] 


    if not "cellSize" in gridData:
        if "boxSize" in gridData and "numCells" in gridData:
            gridData["cellSize"] = [ np.round(gridData["boxSize"][0]/(gridData["numCells"][0] ), 3),  np.round(gridData["boxSize"][1]/(gridData["numCells"][1] ), 3), np.round(gridData["boxSize"][2]/(gridData["numCells"][2] ), 3)  ]


            
    if not "numStep" in gridData:
        if h5Stream.__contains__("time"):
            gridData["numStep"] = h5Stream["time"].attrs["vsStep"]
            
    if not "runTime" in gridData or ("runTime" in gridData and gridData["runTime"] == 0.0):
        if h5Stream.__contains__("time"):
            gridData["runTime"] = h5Stream["time"].attrs["vsTime"]

    if not "timeStep" in gridData:
        if h5Stream.__contains__("time"):
            gridData["timeStep"] = gridData["runTime"]/gridData["numStep"]
    return gridData
