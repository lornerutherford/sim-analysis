# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""
import inspect

from .plot import Plotter
from plotter  import Plotter2D, PlotterPhaseSpace


class MultiPlot(Plotter):
    
    def __init__(self, plotters = None, fig_height = None, grid= None,  make_fig = None, save_fig = None, dpi = None, axisSpacingX = None, axisSpacingY = None):
        Plotter.__init__(self, [fig_height, fig_height],  make_fig, save_fig, dpi)
        # create local copies of plotter objects
        
        self.plotters = plotters 
        
       
        self.grid = grid
        self.fig_height = fig_height

        self.axisBounds = []
        
        self.axisSpacingX = axisSpacingX
        self.axisSpacingY = axisSpacingY
        
        
        


        
        
        
        