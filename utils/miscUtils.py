# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""

class picVizException(Exception):
    "Exception raised for invalid use of the picViz"
    pass



def copy_object(source, target):
    from dumps   import Particles, Field, FieldLine, ParticlesLine
    from plotter import  Plotter2D, PlotterPhaseSpace, PlotterHist
    
    for targetProp, targetVal in vars(target).items():
        for sourceProp, sourceVal in vars(source).items():
                
            if targetProp == sourceProp:
                
                if targetProp is "particles":
                    target.particles = []
                    for ptclObj in source.particles:
                        target.particles.append( copy_object(ptclObj, Particles() )  )
                    break    
                elif targetProp is "fields":
                    target.fields = []
                    for fldObj in source.fields:
                        target.fields.append( copy_object(fldObj, Field() )  )
                    break   
                elif targetProp is "plotters":
                    target.plotters = []
                    for plotterObj in source.plotters:
                        if isinstance(plotterObj, Plotter2D):
                            target.plotters.append( copy_object( plotterObj, Plotter2D() )  )
                        if isinstance(plotterObj, PlotterPhaseSpace):
                            target.plotters.append( copy_object( plotterObj, PlotterPhaseSpace() )  )
                        if isinstance(plotterObj, PlotterHist):
                            target.plotters.append( copy_object( plotterObj, PlotterHist() )  )
                    break          

                elif targetProp is "lines":
                    target.lines = []
                    for lineObj in source.lines:

                        if isinstance(lineObj, FieldLine):
                            target.lines.append( copy_object( lineObj, FieldLine() )  )
                        if isinstance(lineObj, ParticlesLine):
                            target.lines.append( copy_object( lineObj, ParticlesLine() )  )
                    break
                else:
                    if targetVal is None:
                        if isinstance(sourceVal, (list,tuple, dict)):
                            sourceVal = list(sourceVal)
                        setattr(target, targetProp, sourceVal)
                        break
                    
                    
                    elif targetProp == "loaded":
                        target.loaded = sourceVal
                        break
                    
                    
    return target

def create_directory(path):
    import os
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
            return path
        except:
            print ("   (!) Could no create directory " + path +" for outPath, command ignored")
            return


def export(data, dumpObj, plotter, prefix = ""):
    """exports arbitrary data to file (at pathToData)"""
    import numpy as np
    from dumps   import Particles, Field, FieldLine, ParticlesLine
    name = ""
    path = ""
    if  isinstance(dumpObj, Particles):
        name = "Ptcl_"
        try:
            name +=  dumpObj.name + "_" + plotter.plane + "_" + str(dumpObj.index)
        except:
            name +=  dumpObj.name + "_" + plotter.direction + "_" + str(dumpObj.index)
        path = plotter.outPath + dumpObj.name + "//"
        
    elif  isinstance(dumpObj, Field):
        name = "Fld_"
        name +=  dumpObj.name + "_" + dumpObj.kind + "_" + str(dumpObj.component) + "_" + str(dumpObj.index)
        path = plotter.outPath + dumpObj.name + "//"

    elif isinstance(dumpObj, (FieldLine,ParticlesLine)):
        name = "LinePtcl" if isinstance(dumpObj, ParticlesLine) else "LineFld"
        path = plotter.outPath + name + "//"
        name += "_x=" +  str(dumpObj.x_range) + "_y=" +  str(dumpObj.y_range) +"_z=" +  str(dumpObj.z_range)
       
    if prefix is not "":
        prefix += "_"
    create_directory(path)
    outfile = path  + str(name)+ "_" + str(prefix) + str(plotter.dumpNumber) +".txt"
    np.savetxt(outfile, data, fmt='%.9f', delimiter='    ', newline='\n', header= '', footer='', comments='')









