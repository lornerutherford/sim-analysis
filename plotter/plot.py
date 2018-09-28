# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl

picViz plotter class

"""
import time

class Plotter(object):
    """
    class defines the common structure of all plotter objects (they inherit those propeties)
    """
    def __init__(self, figSize, makeFig, saveFig, dpi):
        
        self.fig_size = figSize
        self.outPath = None
        self.save_fig = saveFig
        self.make_fig = makeFig
        self.dpi  = dpi
        self.ID = time.time()
        
        
        