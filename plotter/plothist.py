# -*- coding: utf-8 -*-
"""
Created on Sun Dec 02 13:30:54 2018

@author: Paul Scherkl
"""

from plot import Plotter
import numpy as np


class PlotterHist(Plotter):
    
    def __init__(self, particles = None, quantx =None, bin_size= None,  log_x = None, log_y = None, fig_size = None, x_lim = None, y_lim = None, show_sim_progress = None, make_fig  = None, save_fig  = None, dpi = None):

        Plotter.__init__(self, fig_size,  make_fig, save_fig, dpi)

        self.particles = particles
        self.quantx = quantx
        self.bin_size = bin_size
        self.log_x = log_x
        self.log_y = log_y
        
        self.x_lim  = x_lim
        self.y_lim  = y_lim
        
        
        
        
        self.show_sim_progress = show_sim_progress
        
        self.tickSize        = None
        self.labelSize       = None
        self.labelSpacing    = None
        self.labelSpacingX   = None
        self.labelSpacingY   = None
        self.colorbarWidth   = None
        self.colorbarSpacing = None
        
        
        
        


def plot_histogram(ax, plotter, ptcl):
    import scipy.constants as const
    
    from dumps.dumpUtils.particlesUtils import get_particles_vector_from_string
    xVec   =  get_particles_vector_from_string(ptcl, plotter.quantx)
    n, bins, patches = ax.hist(xVec, bins= int((np.max(xVec) -  np.min(xVec))/plotter.bin_size) , color=ptcl.color, weights =get_particles_vector_from_string(ptcl, "weight")* const.e *ptcl.numPtclsInMacro *1e12 )
    

    
    

def plotterhist_makeFigure(plotter, fig, ax, gridData):
    from plotter.plotStyleUtils import show_sim_progress
    from plotter.plotStyleUtils import format_plotter_axes
    
    for particles in plotter.particles:
        if particles.loaded:
            if particles.plot_data: plot_histogram(ax, plotter, particles )
    
    format_plotter_axes(ax, plotter)        
    
    
    if plotter.show_sim_progress is not 0:
        show_sim_progress(ax, plotter, gridData, kind = plotter.show_sim_progress)





def check_plotterhist_axis_limits(plot):
    from plotter import MultiPlot
    if isinstance(plot, PlotterHist):
        check_axis_limits(plot)
    elif isinstance(plot, MultiPlot):
        for plotter in plot.plotters:
            if isinstance(plotter, PlotterHist):
                check_axis_limits(plotter)



def get_histogram(ptcl, quantx, bin_size):
    from dumps.dumpUtils.particlesUtils import get_particles_vector_from_string
    import scipy.constants as const
    xVec   =  get_particles_vector_from_string(ptcl, quantx)
    if np.min(xVec) == np.max(xVec): return 0,0
    
    weights = get_particles_vector_from_string(ptcl, "weight")
    xAxis = np.linspace(np.min(xVec), np.max(xVec), ( np.max(xVec) -  np.min(xVec))/bin_size)
    yAxis = np.histogram(xVec,len(xAxis), weights = weights)
    yAxis = yAxis[0] * const.e *ptcl.numPtclsInMacro *1e12
    return xAxis, yAxis
    


def check_axis_limits(plot):
    from dumps.dumpUtils.particlesUtils import get_particles_vector_from_string


    xComp =  plot.quantx
    if not plot.x_lim:

        currentx_lim = []
        for ptcl in plot.particles:
            if ptcl.loaded:
                xVec = get_particles_vector_from_string(ptcl, xComp)
                minVal = np.min(xVec)
                maxVal = np.max(xVec)
                if not plot.x_lim:
                    minVal = minVal - (maxVal - minVal)*0.1
                    maxVal = maxVal + (maxVal - minVal)*0.1
                    
                    if not currentx_lim:
                        currentx_lim = [minVal, maxVal]
                    else: 
                        currentx_lim = [ np.min( (minVal, currentx_lim[0]) ), np.max( (maxVal, currentx_lim[1]) )]
        plot.x_lim = currentx_lim

    if not plot.y_lim:

        currenty_lim = []
        
        for ptcl in plot.particles:
            if ptcl.loaded:
                
                xVec, yVec = get_histogram(ptcl, plot.quantx,  plot.bin_size)
                if isinstance(xVec, (int, float)): 
                    ptcl.loaded = 0
                    continue
                minVal = np.min(yVec)
                maxVal = np.max(yVec)
                if not plot.y_lim:
                    minVal = minVal - (maxVal - minVal)*0.1
                    minVal = 0 if minVal < 0 else minVal
                    maxVal = maxVal + (maxVal - minVal)*0.1
                    if not currenty_lim:
                        currenty_lim = [minVal, maxVal]
                    else: 
                        currenty_lim = [ np.min( (minVal, currenty_lim[0]) ), np.max( (maxVal, currenty_lim[1]) )]
                        
        plot.y_lim = currenty_lim
   
