# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 12:05:16 2018

@author: Paul Scherkl
"""

import matplotlib.pyplot as plt
import numpy as np
from plotter import Plotter2D, PlotterPhaseSpace, MultiPlot
from plotter.plot2D import check_Plotter2D_axis_limits, plotter2D_makeFigure
from plotter.plotPhaseSpace import check_plotterPhaseSpace_axis_limits, plotterPhaseSpace_makeFigure
from plotter.plotUtils import draw_colorbars, draw_line_axes, get_colorbar_list, get_axis_list
from utils.miscUtils import create_directory

import time





def make_plots(plotList, gridData, dumpNumber):
    """
    Central plotting function. Iterates all plot commands and distributes tasks
    
    
    Parameters
    ----------
    plotList: list
        List of Plotter objects
        
    gridData: dict
        Dict containing simulation grid information
    
    dumpNumber: int
        current dump number
    """
    multiCounter      = 0
    plot2DCounter     = 0
    phaseSpaceCounter = 0
    
    for plotter in plotList:
        startTime = time.time()
        
        colBarList   = []
        lineAxisList = []
        if plotter.make_fig:
            if not check_plot_requests(plotter):
                print ("       (!) Warning: Plotter of type " + str(type(plotter)) + " does not contain any loaded dumps, ignored")
                continue
    
            create_directory(plotter.outPath)
            
            check_Plotter2D_axis_limits(plotter, gridData)
            check_plotterPhaseSpace_axis_limits(plotter)
            
            if isinstance(plotter, (Plotter2D, PlotterPhaseSpace)):
                colBarList.append( get_colorbar_list(plotter, gridData) )
                lineAxisList.append( get_axis_list(plotter, gridData))
                fig, axList = make_figure_and_axes(plotter, gridData, colBarList  = colBarList, lineAxisList = lineAxisList)
                
                if isinstance(plotter, PlotterPhaseSpace):
                    phaseSpaceCounter += 1
                    plotterPhaseSpace_makeFigure(plotter, fig,  axList[-1], gridData)
                else:
                    plot2DCounter += 1
                    plotter2D_makeFigure(plotter, fig, axList[-1], gridData)

                
                
            elif isinstance(plotter, MultiPlot):
                for i in range(len(plotter.plotters)):
                    colBarList.append( get_colorbar_list(plotter.plotters[i], gridData) )
                    lineAxisList.append( get_axis_list(plotter.plotters[i], gridData))

                fig, axList = make_figure_and_axes(plotter, gridData, colBarList  = colBarList,  lineAxisList = lineAxisList)
               
                for i in range(len(plotter.plotters)):
                    if i == np.sum(plotter.grid):
                        break
                    if isinstance(plotter.plotters[i], Plotter2D):
                        plotter2D_makeFigure(plotter.plotters[i], fig, axList[i], gridData)
                    elif isinstance(plotter.plotters[i], PlotterPhaseSpace):
                        plotterPhaseSpace_makeFigure(plotter.plotters[i], fig,  axList[i], gridData)


                multiCounter  += 1
                
                
                
            if plotter.save_fig:
                if isinstance(plotter, PlotterPhaseSpace):
                    plt.savefig(plotter.outPath + "PhaseSpace_" + str(phaseSpaceCounter) +"_direction_" + plotter.direction + "_" + str(dumpNumber) + ".png",  dpi= plotter.dpi, bbox_inches='tight')
                elif isinstance(plotter, Plotter2D):
                    plt.savefig(plotter.outPath + "Plot2D_" + str(plot2DCounter) + "_" + str(dumpNumber)+ ".png",  dpi= plotter.dpi, bbox_inches='tight')
                elif isinstance(plotter, MultiPlot):
                    plt.savefig(plotter.outPath + "MultiPlot_" + str(multiCounter) + "_" + str(dumpNumber) + ".png",  dpi= plotter.dpi, bbox_inches='tight')
            plt.show()
                       
            plt.close(fig)
            stopTime = time.time()
            print "   Figure plotting lasted " + str(stopTime - startTime) + " s"

            
            
            
def make_figure_and_axes(plotter, gridData, colBarList  = [], lineAxisList = []):
    axList = []
    
    if isinstance(plotter, PlotterPhaseSpace):
        fig = plt.figure(figsize = plotter.fig_size)   
        axList.append( fig.add_axes([ 0 ,    0,   1 ,  1]) )
        draw_line_axes(fig, axList[-1], plotter, lineAxisList[0], gridData)
        draw_colorbars(fig, axList[-1], plotter, colBarList[0],  lineAxisList[0], )        
        
        
    if isinstance(plotter, Plotter2D):
        yRatio = 1
        if plotter.auto_aspect_ratio:
            yRatio =  1.0*( max(plotter.y_lim) - min(plotter.y_lim) ) / ( max(plotter.x_lim) - min(plotter.x_lim) ) 
            plotter.fig_size[0] = plotter.fig_size[1]/yRatio
        fig = plt.figure(figsize = plotter.fig_size) 
        axList.append( fig.add_axes([ 0 ,    0,   1 ,  1]) )
        draw_line_axes(fig, axList[-1], plotter, lineAxisList[0], gridData)
        draw_colorbars(fig, axList[-1], plotter,  colBarList[0],  lineAxisList[0])        


    
    if isinstance(plotter, MultiPlot):
        
        figWidth        = plotter.fig_height #TODO: must determine width of widest column here!!!!
        plotter.fig_size = [ figWidth , plotter.fig_height] 
        
        fig = plt.figure(figsize = plotter.fig_size) 

        
        for j in range(len(plotter.plotters)):
            plot = plotter.plotters[j]
            if np.sum(plotter.grid) <= j:
                return fig, axList
            row = 0
            col = 0
            currentJ = j
            for i in range(len(plotter.grid)):
                if currentJ < plotter.grid[i]:
                    col = currentJ
                    break
                else:
                    row +=1
                    col = 0
                    currentJ -= plotter.grid[i] 
                    
        
                
                
            yStart  = 1.0 - plotter.axisSpacingY/plotter.fig_height*row - (1 - plotter.axisSpacingY/plotter.fig_height*(len(plotter.grid) - 1))  /  len(plotter.grid)  *  row 
            yHeight = (1.0 - plotter.axisSpacingY/plotter.fig_height*(len(plotter.grid) -1))/len(plotter.grid)
            yRatio  = 1.0
            
            
            xWidth  = 1
            
            if isinstance(plot, Plotter2D):
                if plot.auto_aspect_ratio:
                    xWidth = yHeight / ( 1.0*( max(plot.y_lim) - min(plot.y_lim) ) / ( max(plot.x_lim) - min(plot.x_lim) ) )
            elif isinstance(plot, PlotterPhaseSpace):
                xWidth = float(plot.fig_size[0])/plot.fig_size[1] * yHeight 

                
            if col == 0:
                xStart = 0.
            else:
                xStart = plotter.axisBounds[-1][2]
                
            axList.append( fig.add_axes([ xStart ,    yStart,   xWidth ,     yHeight]) )
            xEnd = axList[-1].get_position().x1 +  (plotter.axisSpacingX + plot.colorbarWidth*(len(colBarList[j]) + len(lineAxisList[j])) + plot.colorbarSpacing * np.max( len(colBarList[j]) + len(lineAxisList[j]) , 0))/figWidth
            plotter.axisBounds.append( [axList[-1].get_position().x0, axList[-1].get_position().y0,   xEnd,  axList[-1].get_position().y1 ]  )
            
            draw_line_axes(fig, axList[-1], plot, lineAxisList[j], gridData)
            draw_colorbars(fig, axList[-1], plot,  colBarList[j], lineAxisList[j])        
                
    return fig, axList        
        
        

def check_plot_requests(plot):
    """
    Helper method that checks if there are any loaded Particles or Field objects in the given plotter object
    
    Parameters
    ----------
    plot: Plotter object
        Object that might contain loaded Particles and/or Field objects

    Returns
    -------
    True if there is any Particles or Field object loaded. Else: False   
    
    """
    if isinstance(plot, MultiPlot):
        for plotter in plot.plotters:
            for ptcl in plotter.particles:
                if ptcl.loaded:
                    return True
            if isinstance(plotter, Plotter2D):
                for fld in plotter.fields:
                    if fld.loaded:
                        return True


    else:
        for ptcl in plot.particles:
            if ptcl.loaded:
                return True
            
        if isinstance(plot, Plotter2D):
            for fld in plot.fields:
                if fld.loaded:
                    return True
                            
    
    return False




    





