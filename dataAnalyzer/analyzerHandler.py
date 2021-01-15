# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:47:00 2018

@author: P. Scherkl

"""


def analyze_data(analyzerList, gridData, dumpNumber, is_first, tmpAnalDataList):
    
    from utils.miscUtils import create_directory
    from dataAnalyzer import ParticlesAnalyzer, FieldAnalyzer
    from dumps.dumpUtils.particlesUtils import get_quantity_from_string, get_particles_vector_from_string
    
    
    ptclAnalCounter    = 0
    fldAnalCounter     = 0
    counter            = 0
    
    

    for analyzer in analyzerList:
        loadCheck = check_anal_requests(analyzer)
        if not loadCheck:
            print ("       (!) Warning: Analyzer of type " + str(type(analyzer)) + " does not contain any loaded dumps, ignored")
            
        
        summaryOutName = analyzer.outPath + "analyzer_" + str(counter) + "_summary.txt" if analyzer.file_name is None else analyzer.outPath + "analyzer_" + analyzer.file_name + "_summary.txt"
        create_directory(analyzer.outPath)
        
        if analyzer.print_data and loadCheck: 
            print("\n       ----- Analyzer " + str(counter) + " data -----" )
            if is_first and analyzer.save_summary_txt:
                with open(summaryOutName, "w") as f:
                    f.write("\n       ----- Analyzer " + str(counter) + " data -----")
            
        
        create_directory(analyzer.outPath)
        if isinstance(analyzer, ParticlesAnalyzer):
            if is_first:
                tmpAnalDataList[counter] = [[] for i in range(len(analyzer.particles))]
                
            for i in range(len(analyzer.particles)):
                
                ptcls = analyzer.particles[i]
                if analyzer.print_data and ptcls.loaded: print("           ---- " + ptcls.name  + " ----")
                if analyzer.save_summary_txt and ptcls.loaded: 
                    with open(summaryOutName, "a") as f:
                        f.write("\n\n           ---- " + ptcls.name + "_" + str(dumpNumber) + " ----")
                
                
                tmpAnalData      = {"dumpNum":[dumpNumber]}
                for quant in analyzer.quantityList:
                    tmpAnalData[quant] = [get_quantity_from_string(ptcls, quant, analyzer.bin_size)] if ptcls.loaded else [0]
                    if analyzer.print_data and ptcls.loaded: print(get_quantity_val_string(quant, tmpAnalData[quant][0]))
                    if analyzer.save_summary_txt and ptcls.loaded: 
                        with open(summaryOutName, "a") as f:
                            f.write("\n" + get_quantity_val_string(quant, tmpAnalData[quant][0]))
                        
                    
                  
                existingAnalData = load_analyzer_file(analyzer, ptclAnalCounter, ptcls.name) if is_first and analyzer.use_existing_file else tmpAnalDataList[counter][i]                
                tmpAnalData = tmpAnalData if is_first and (not analyzer.use_existing_file or not existingAnalData) else mergeData(existingAnalData, tmpAnalData) 

                tmpAnalDataList[counter][i] = tmpAnalData
                ptclAnalCounter += 1
                if analyzer.save_txt:
                    save_analyzer_file(tmpAnalDataList[counter][i], analyzer, counter, ptcls.name)

    #TODO: add analyzer methods for fields
                
        counter += 1
    return tmpAnalDataList
                
                


def check_anal_requests(analyzer):
    try:
        for ptcl in analyzer.particles:
            if ptcl.loaded: 
                return 1
    except: pass
    try:
        for fld in analyzer.fields:
            if fld.loaded: 
                return 1
    except: pass
    return 0
    
    

def get_quantity_val_string(quant, val):
    import numpy as np
    quantString = '{:.2e}'.format(val) if val> 1e2 or val<1e-2 else str(np.round(val,2))
    unitString  = get_unit_for_analyzer("ptcl,0,0,"+quant)
    return "           " + quant + " " * (8 - len(quant)) + "= "+ str(quantString) + " "*(9-len(str(quantString))) + unitString





def get_analyzer_file_name(analyzer, counter, speciesName):
    from dataAnalyzer import ParticlesAnalyzer
    
    if analyzer.file_name is None:
        return analyzer.outPath + "PtclData_" + str(counter) + "_" + speciesName + ".txt" if isinstance(analyzer, ParticlesAnalyzer) else analyzer.outPath + "FldData_" + str(counter) + "_" + speciesName + ".txt"
    else:
        return analyzer.outPath + analyzer.file_name + "_" + speciesName + ".txt"






def load_analyzer_file(analyzer, counter, speciesName):
    """if specified by user, try to load an existing output file. if not existing, return empty dict and print warning"""
    import pandas as pd
    import numpy as np
    
    fileName = get_analyzer_file_name(analyzer, counter, speciesName)        

    try: 
        dataDict = pd.read_csv(fileName, sep = "\t", dtype = np.float64)
        dataDict = dataDict.to_dict()
        if not len(dataDict["dumpNum"]): 
            print ("       (!) Warning: Existing picViz analyzer output file  \"" + fileName + "\" is empty, create new file")
            return {}
        
        for key in dataDict.keys(): # remove shit blanks from keys
            newKey = key.replace(" ", "")
            newKey = newKey if not newKey.find("(") else newKey.split("(")[0]
            dataDict[newKey] = dataDict.pop(key)  
            
        for key in dataDict.keys(): # transform dicts in dict to lists in dict
            dataDict[key] = [ v for v in dataDict[key].values() ]
        
        dataDict["dumpNum"] = [ int(v) for v in dataDict["dumpNum"]]
        return dataDict
    except:
        print ("       (!) Warning: Cannot find existing picViz analyzer output file  \"" + fileName + "\", create new file")
        return {}
    
    
    
def get_unit_for_analyzer(speciesKey):
    """ get unit for calculated parameter. remove latex formatting"""
    from plotter.plotStyleUtils import get_unit_from_component
    unit = get_unit_from_component(speciesKey) 
    if unit.find("$") > -1:
        unit = unit.replace("$", "")
        unit = unit.replace("\mathrm", "")
        unit = unit.replace("{", "")
        unit = unit.replace("}", "")
        unit = unit.replace("\\", "")
        unit = unit.replace(" ", "")
        if unit.find("mum")>-1: unit = "um" 
    return unit

    
def save_analyzer_file(data, analyzer, counter, speciesName):
    """export analyzed data to txt file (name auto generated or defined by user). data gets sorted by dump numbers. creates headers with quanity and unit"""
    import pandas as pd
    from dataAnalyzer import ParticlesAnalyzer
    
    columnWidth = 26 # characters
    decimals    = 6
    
    if analyzer.headers == 2:
    
        def formatHeader(names):
            
            for i in range(len(names)):
                if names[i] is not "dumpNum":
                    nameLen = len(names[i] )
                    string1 = " " * ( columnWidth - nameLen )
                    names[i] = string1 + names[i]
            return names
            
        def formatUnit(names):
            
            for i in range(len(names)):
                if names[i] is not "dumpNum":
                    unit = get_unit_for_analyzer("ptcl,0,0,"+names[i])  if isinstance(analyzer, ParticlesAnalyzer)  else ""
                    names[i] = unit
            return names
        
        colNames =  ["dumpNum"] + analyzer.quantityList + [ key for key in data.keys() if key not in analyzer.quantityList and key.find("dumpNum") == -1 ]
        
        df = pd.DataFrame( data, columns  = colNames)
        df = df.sort_values(by=['dumpNum'])
        df.columns = pd.MultiIndex.from_tuples(zip(df.columns, ["dumpNum"] +formatUnit(colNames)))
        
        try:
            df.to_csv(get_analyzer_file_name(analyzer, counter, speciesName) , index  = False, sep = ",", float_format = "%"+str(columnWidth)+"."+str(decimals)+"e" )
        except:
            print ("       (!) Warning: path for analyzer output does not exist  \"" + analyzer.outPath + "\", ignored")
            
    else:
    
        def formatHeader(names):
            for i in range(len(names)):
                if names[i] is not "dumpNum":
                    unit = get_unit_for_analyzer("ptcl,0,0,"+names[i])  if isinstance(analyzer, ParticlesAnalyzer)  else ""
                    nameLen = len(names[i] ) + len(unit) + 2
                    string1 = " " * ( columnWidth - nameLen ) if i is not 1 else " " * ( columnWidth - nameLen -4)
                    names[i] = string1 + names[i] + "(" + unit + ")"
            return names
    
        colNames =  ["dumpNum"] + analyzer.quantityList + [ key for key in data.keys() if key not in analyzer.quantityList and key.find("dumpNum") == -1 ]
        df = pd.DataFrame( data, columns  = colNames)
        df = df.sort_values(by=['dumpNum'])
        try:
            df.to_csv(get_analyzer_file_name(analyzer, counter, speciesName) , index  = False, sep = "\t", float_format = "%"+str(columnWidth)+"."+str(decimals)+"e", header = formatHeader(colNames) )
        except:
            print ("       (!) Warning: path for analyzer output does not exist  \"" + analyzer.outPath + "\", ignored")




        
        
def mergeData(a, b):
    """merge two analyzer dicts. a is old data, b is new and to be added. 
        values existing in both a and b will be set to the ones in b. 
        empty entries are set to 0"""
    import numpy as np

    for number in b["dumpNum"]:
        if number not in a["dumpNum"]:
            a["dumpNum"] = np.append(a["dumpNum"], number)
            for key in a.keys():
                if key.find("dumpNum") == -1:
                    a[key] = np.append(a[key], np.float64(0.0))
        
    for key in b.keys():
        if not key in a:
            a[key] = np.zeros(len(a["dumpNum"]) )
    
    for i in range(len(b["dumpNum"])):
        i = int(i)

        for key in b:
            if key.find( "dumpNum")>-1: continue
            idx =  np.where( np.asarray(a["dumpNum"]) == b["dumpNum"][i] )   
            a[key][ idx[0][0] ] =b[key][i]
            
    return a    

    
