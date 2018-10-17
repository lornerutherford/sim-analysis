# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
utility functions dedicated for main.py


"""

from utils.miscUtils  import copy_object




def print_start_message():
    print "------------------------------------------------------------------------------------------------------"
    print " picVisualizer v1.02.03 (2018) by Paul Scherkl (University of Strathclyde, paul.scherkl@strath.ac.uk) "
    print "------------------------------------------------------------------------------------------------------"



def set_analyzer_copies(globalAnalyzers, loadedPtclObjs, loadedFldObjs):
    from dumps.dumpUtils.particlesUtils import make_particles_cuts
    from dataAnalyzer import  ParticlesAnalyzer, FieldAnalyzer
    newAnalyzers = []
    
    for analyzer in globalAnalyzers:
        
        if isinstance(analyzer, ParticlesAnalyzer):
            newParticlesAnalyzer = copy_object(analyzer, ParticlesAnalyzer() ) # create copy of PlotterObject including contained Particles objects
            
            for localPtcl in newParticlesAnalyzer.particles:            # copy loaded data into Particles objects
                matchingIndexObj = [lPtcl for lPtcl in loadedPtclObjs if lPtcl.index  == localPtcl.index]
                if matchingIndexObj:
                    localPtcl = copy_object( matchingIndexObj[0], localPtcl ) # the iterator connects loaded data with the local copy
                    make_particles_cuts(localPtcl)
            newAnalyzers.append( newParticlesAnalyzer )
            
            
            
        if isinstance(analyzer, FieldAnalyzer):
            newFieldAnalyzer = copy_object(analyzer, FieldAnalyzer() ) # create copy of PlotterObject including contained Particles objects
            
            for localFld in newFieldAnalyzer.fields:            # copy loaded data into Particles objects
                matchingIndexObj = [lFld for lFld in loadedFldObjs if lFld.index  == localFld.index]
                if matchingIndexObj:
                    localFld = copy_object( matchingIndexObj[0], localFld ) # the iterator connects loaded data with the local copy

            newAnalyzers.append( newFieldAnalyzer )
            
            
    return newAnalyzers





def setup_plotter_copies(globalplotters, loadedPtclObjs, loadedFldObjs):
    """ 
    Creates copies of any plotter object defined by user. 
    The copy process includes any contained sub-objects and their settings (user settings are preserved!)
    This function also assigns the previously loaded data to the copies
    Finally, after the loaded data is copied, local Particle cuts are performed
    
    Parameters
    ----------
    globalplotters: list
        List of user-defined plotter objects
        
    loadedPtclObjs: list
        List of Particles objects (after loading)
        
    loadedFldObjs: list
        List of Field objects (after loading)
        
    Returns
    -------
    List with copies of plotter objects     
    """
    
    from dumps.dumpUtils.particlesUtils import make_particles_cuts
    from plotter import  Plotter2D, PlotterPhaseSpace, MultiPlot
    newplotters = []

    for plotter in globalplotters:
        
        if isinstance(plotter, PlotterPhaseSpace):
            newPlotterPhaseSpace = copy_object(plotter, PlotterPhaseSpace() ) # create copy of PlotterObject including contained Particles objects
            
            for localPtcl in newPlotterPhaseSpace.particles:            # copy loaded data into Particles objects
                matchingIndexObj = [lPtcl for lPtcl in loadedPtclObjs if lPtcl.index  == localPtcl.index]
                if matchingIndexObj:
                    localPtcl = copy_object( matchingIndexObj[0], localPtcl ) # the iterator connects loaded data with the local copy
                    make_particles_cuts(localPtcl)
            newplotters.append( newPlotterPhaseSpace )
            
            
        if isinstance(plotter, Plotter2D):
            newPlotter2D = copy_object(plotter, Plotter2D() )

            for localPtcl in newPlotter2D.particles:            # copy loaded data into Particles objects
                matchingIndexObj = [lPtcl for lPtcl in loadedPtclObjs if lPtcl.index  == localPtcl.index]
                if matchingIndexObj:
                    localPtcl = copy_object( matchingIndexObj[0], localPtcl )
                    localPtcl.plane = plotter.plane if plotter.plane is not None else localPtcl.plane
                    make_particles_cuts(localPtcl)
                
            for localFld  in newPlotter2D.fields:            # copy loaded data into Particles objects
                matchingIndexObj = [lFld for lFld in loadedFldObjs if lFld.index  == localFld.index]
                if matchingIndexObj:
                    localFld = copy_object( matchingIndexObj[0], localFld )
                    localFld.plane = plotter.plane if plotter.plane is not None else localFld.plane
                    localFld.plane_offset = plotter.plane_offset if plotter.plane_offset is not None else localFld.plane_offset
            
            newplotters.append( newPlotter2D )
            
    for plotter in globalplotters:
        if isinstance(plotter, MultiPlot):
            newMultiPlotter = copy_object(plotter, MultiPlot() )
            for localPlotter in newMultiPlotter.plotters:
                
                if isinstance(localPlotter, PlotterPhaseSpace):

                    for localPtcl in localPlotter.particles:            # copy loaded data into Particles objects
                        matchingIndexObj = [lPtcl for lPtcl in loadedPtclObjs if lPtcl.index  == localPtcl.index]
                        if matchingIndexObj:
                            localPtcl = copy_object( matchingIndexObj[0], localPtcl )
                            make_particles_cuts(localPtcl)
                        
                if isinstance(localPlotter, Plotter2D):

                    for localPtcl in localPlotter.particles:            # copy loaded data into Particles objects
                        matchingIndexObj = [lPtcl for lPtcl in loadedPtclObjs if lPtcl.index  == localPtcl.index]
                        if matchingIndexObj:
                            localPtcl = copy_object( matchingIndexObj[0], localPtcl )
                            localPtcl.plane = localPlotter.plane if localPlotter.plane is not None else localPtcl.plane
                            make_particles_cuts(localPtcl)
                        
                    for localFld  in localPlotter.fields:            # copy loaded data into Particles objects
                        matchingIndexObj = [lFld for lFld in loadedFldObjs if lFld.index  == localFld.index]
                        if matchingIndexObj:
                            localFld = copy_object( matchingIndexObj[0], localFld )
                            localFld.plane = localPlotter.plane if localPlotter.plane is not None else localFld.plane
                            localFld.plane_offset = localPlotter.plane_offset if localPlotter.plane_offset is not None else localFld.plane_offset
        
            newplotters.append( newMultiPlotter )

    return newplotters
    



