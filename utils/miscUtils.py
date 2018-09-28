# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""

class picVizException(Exception):
    "Exception raised for invalid use of the picViz"
    pass



def copy_object(source, target):
    from dumps   import Particles, Field, FieldLine, ParticlesLine
    from plotter import  Plotter2D, PlotterPhaseSpace
    
    
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
                    break          
                elif targetProp is "lines" and source.lines is not None:
                    target.lines = []
                    for lineObj in source.lines:
                        if isinstance(lineObj, FieldLine):
                            target.lines.append( copy_object( lineObj, FieldLine() )  )
                        if isinstance(lineObj, ParticlesLine):
                            target.lines.append( copy_object( lineObj, ParticlesLine() )  )
                        
                    break
                else:
                    if targetVal is None:
                        if isinstance(sourceVal, list):
                            sourceVal = list(sourceVal)
                        setattr(target, targetProp, sourceVal)
                        break
                    
                    
                    elif targetProp == "loaded":
                        target.loaded = sourceVal
                        break
                    
                    
    return target

def create_directory(path):
    import os
    if not isinstance(path, basestring ):
        print ("   (!) Given variable " + str(path) +" is not a valid string for Outpath, command ignored")
        return
    else:
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
                return path
            except:
                print ("   (!) Could no create directory " + path +" for outPath, command ignored")
                return


