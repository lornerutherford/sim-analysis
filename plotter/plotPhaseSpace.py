# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
picViz class for phase space plots (inherited from Plotter class)
provides framework to produce arbitrary plots for particle species
"""

from plot import Plotter
from dumps.dumpUtils.particlesUtils import get_particles_vector_from_string
import numpy as np

class PlotterPhaseSpace(Plotter):
    """Class to control phase space plots"""
    
    def __init__(self, particles= None, direction = None, fig_size = None, x_lim = None, y_lim = None, show_sim_progress = None,  make_fig = None, save_fig = None, dpi = None):
        """
        
        Initializes PlotterPhaseSpace object and creates local copies of global Particles objects.
        
        Parameters
        ----------
            
        particles: list
            Local Particles objects.  

        fig_size: tuple or list with 2 entries
            Defines figure size in inches

        x_lim: tuple or list with 2 entries
            Defines range of shown x-axis in plot
            
        y_lim: tuple or list with 2 entries
            Defines range of shown y-axis in plot
            
        direction: string
            Defines plane of requested phase space. Can be x, t,y, or z
            
        Returns
        -------
        Object of class PlotterPhaseSpace     
            
        """
        Plotter.__init__(self, fig_size,  make_fig, save_fig, dpi)
        
        self.particles = particles
        
        self.direction = direction
        
        self.x_lim = x_lim
        self.y_lim = y_lim
        
        self.show_sim_progress = show_sim_progress


        self.tickSize        = None
        self.labelSize       = None
        self.labelSpacing    = None
        self.labelSpacingX   = None
        self.labelSpacingY   = None
        self.colorbarWidth   = None
        self.colorbarSpacing = None
        



def check_plotterPhaseSpace_axis_limits(plot):
    from plotter import MultiPlot
    if isinstance(plot, PlotterPhaseSpace):
        check_axis_limits(plot)
    elif isinstance(plot, MultiPlot):
        for plotter in plot.plotters:
            if isinstance(plotter, PlotterPhaseSpace):
                check_axis_limits(plotter)
    
    

     

def check_axis_limits(plot):
    xComp = ""
    yComp = ""
    if plot.direction == "x":
        xComp = "x"
        yComp = "e"
    elif plot.direction == "t":
        xComp = "t"
        yComp = "e"
    elif plot.direction == "y":
        xComp = "y"
        yComp = "yp"
    elif plot.direction == "z":
        xComp = "z"
        yComp = "zp"
    
    
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
                yVec = get_particles_vector_from_string(ptcl, yComp)
                minVal = np.min(yVec)
                maxVal = np.max(yVec)
                if not plot.y_lim:
                    minVal = minVal - (maxVal - minVal)*0.1
                    if (plot.direction == "x" or plot.direction == "t") and minVal < 0:
                        minVal = 0
                    maxVal = maxVal + (maxVal - minVal)*0.1
                    if not currenty_lim:
                        currenty_lim = [minVal, maxVal]
                    else: 
                        currenty_lim = [ np.min( (minVal, currenty_lim[0]) ), np.max( (maxVal, currenty_lim[1]) )]
        plot.y_lim = currenty_lim



def plotterPhaseSpace_makeFigure(plotter, fig, ax, gridData):
    from dumps.particles   import plot_particles
    from plotter.plotStyleUtils import  format_plotter_axes
    from plotter.lines   import plot_lines
    
    for particles in plotter.particles:
        if particles.loaded:
            if particles.plot_data: plot_particles(ax, plotter, particles )
            plot_lines(ax, particles,gridData, plotter)
          
    format_plotter_axes(ax, plotter)
    
    
    
    
    
    
    
    