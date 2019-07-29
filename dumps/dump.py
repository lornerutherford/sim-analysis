# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:12:26 2018

@author: Paul Scherkl
"""

class Dump(object):
    """
    class defines the common structure of all dump objects (they inherit those properties)
    
    """   
    def __init__(self, name = None, index = None, plane = None, colormap = None, z_order = None, file_kind = None, plot_data = None,export = None):
        self.name          = name
        self.file_kind     = file_kind
        self.index         = index
        
        self.load          = 0
        self.loaded        = 0
        
        self.plane         = plane
        
        
        self.plot_data     = plot_data
        self.z_order       = z_order
        
        self.show_colorbar  = None
        self.clip_min       = None
        self.clip_max       = None

        self.export         = export
        
        self.lines = []

        import colormaps as customColMaps
        from matplotlib import pyplot as plt


        if colormap is not None:
            self.colormap = plt.cm.get_cmap(colormap)
        else:
            self.colormap     = colormap

        




        
        
        
    
    
    