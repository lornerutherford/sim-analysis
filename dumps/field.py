# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""
from .dump import Dump
import colormaps as customColMaps
from matplotlib import pyplot as plt
from plotter import Line
import numpy as np

class Field(Dump):
    """
    Class containing the field data 
    """
        
    def __init__(self, name = None, index= None, kind = None, component = None, plane= None, plane_offset= None, project = None, opacity = None, colormap = None, \
                 clip_min = None, clip_max = None, show_colorbar = None, z_order = None, file_kind = None, plot_data = None, export = None):
        
        """
        Parameters
        ----------
        
        
        
        """   
        Dump.__init__(self, name =name, index = index, plane=plane, colormap = colormap, z_order = z_order, file_kind=file_kind, plot_data = plot_data, export = export)

        
        self.fieldMatrix      = None
        
        if kind is not None:
            self.kind = kind
            
        self.kind         = kind
        self.component    = component
        self.plane_offset = plane_offset
        self.project      = project
        
        self.opacity      = opacity
        
        
        self.show_colorbar = show_colorbar
    
        self.clip_min = clip_min
        self.clip_max = clip_max
    
        

    def addLine(self, component = 0, axis = "x", x_range = None, y_range = None, z_range = None, show_range = 0,\
                operation = "mean", calculus = None, normalize = None, gauge = None,\
                tick_min = None, tick_max = None, color = None, force_color = 0, invert_axis = 0,\
                show_axis = 1, z_order = 3, export = 0, plot_data = 1, fill = None):
        """
        Interface for Line operations on Field dumps
        User can define line or volume from which to extract data by using range-variables
        Creates new axis including ticks and labels on bottom or right hand side of figure
        
        Parameters
        ----------
            
        component: int
            Defines Field component applied to Line. 
            component >= 0 directly selects the component from associated field matrix
            component = -1: geometric sum of all field components
        
        axis: string
            Defines main-axis of Line. Can be "x", "y" or "z"
            
        x_range: float or list with 2 entries
            Defines range in x-direction to extract data for line
            
        y_range: float or list with 2 entries
            Defines range in y-direction to extract data for line
        
        z_range: float or list with 2 entries
            Defines range in z-direction to extract data for line
            
        show_range: bool
            Highlights the area (defined by x/y/z_range) containing Line data with a colored rectangle/line
        
        operation: string
            When the ranges define a plane or volume, their values are processed based on the operation variable
            Can be "mean" for average or "sum" for sum

        calculus: string
            Performs an additional calculus operation on the generated line, e.g. for calculating the electrostatic potential from an electric field.
            Can be 
                "cumsum"        - cummulative sum of all values along line (front to back)
                "integrate"     - cummulative integral of all values along line (front to back)
                "differentiate" - gradient of the line
        
        normalize: float
            Applies a factor to the line, can be used for normalization.
        
        gauge: string ot float
            Applies an offset to the line, i.e. shifting the zero crossing of the line. Useful in combination with calculus operations to provide a gauge.
            Can be "min" or "max" or an arbitrary float

        tick_min: float
            Defines mininmal value for Line axis tick labels
            
        tick_max: float
            Defines maximal  value for Line axis tick labels
        
        color: string or list with 3 or 4 entries
            Defines color of Line and corresponding axis
            
        force_color, bool
            Assign the chosen color even if other lines with same quantity are plotted (normally, lines with identical properties are grouped and get same color)
         
        invert_axis: bool
            Inverts axis, i.e. flips plotting direction
            
        show_axis: bool
            Show or hide additional axis

        z_order: int > 0
            Defines position of field within plot. Higher values correspond to front layers
            
        export: bool
            Dump plotted data to txt file
            
        plot_data: bool
            Plot data or not

        fill: [<option>, <threshold>]
            Generates a shaded area between the line and <treshold>, according to <option>
            <option> accepts "above" or "below" for filling the area between the line and an absolute threshold,
            or "above_min" or "below_max" for thresholds relative to the global minimum or maximum value of the line.
            <threshold> must be float.

        Returns
        -------
        Line object that controls line plotting with Field objects 
        """
        
        if color is None:
            import random 
            color= [random.random(), random.random(), random.random()]

        if tick_min is not None and tick_max is not None:
            dummy = [tick_min, tick_max]
            tick_min = min(dummy)
            tick_max = max(dummy)
      
        newLineObj = FieldLine(component = component,  axis = axis, x_range = x_range, y_range = y_range, z_range = z_range, \
                               show_range = show_range, operation = operation,\
                               calculus = calculus, normalize = normalize, gauge = gauge,\
                               tick_min = tick_min, tick_max = tick_max,\
                               color = color, force_color= force_color, invert_axis= invert_axis, show_axis = show_axis,\
                               z_order = z_order, export = export, plot_data = plot_data, fill = fill)
                
        if self.lines is None:
            self.lines = []
        self.lines.append( newLineObj ) # add new entry for particles. add the object. load switch is off, will be enabled if this object is used in any plotter or analyzer
        return newLineObj



class FieldLine(Line):
    """
    Class containing line operations dedicated to Field objects 
    """
    
    def __init__(self, component = None, axis = None,  x_range = None, y_range = None, z_range = None, show_range = None, \
                 operation = None, calculus = None, normalize = None, gauge = None,\
                 tick_min = None, tick_max = None,  color = None, force_color = None, invert_axis = None, \
                 show_axis = None,z_order = None, export = None, plot_data = None, fill = None):
        
        Line.__init__(self, axis = axis, x_range = x_range, y_range = y_range, z_range = z_range, \
                      show_range = show_range, operation = operation, tick_min = tick_min, tick_max = tick_max, \
                      color = color, force_color = force_color, invert_axis =invert_axis, show_axis = show_axis, z_order = z_order,\
                      export = export, plot_data = plot_data, fill = fill)

        self.component = component
        self.calculus = calculus
        self.normalize = normalize
        self.gauge = gauge


def plot_field(ax, plotter, field, gridData):
    from dumps.dumpUtils.fieldUtils import get_field_plane, get_field_extent
    from utils.miscUtils import export

    currentPlane   = get_field_plane(field, gridData)
    xRange, yRange = get_field_extent( field, gridData)
    
    
    ax.imshow(currentPlane, cmap = field.colormap, vmin=field.clip_min, vmax = field.clip_max,  aspect='auto', origin='lower', \
              alpha = field.opacity, extent=[np.min(xRange), np.max(xRange), np.min(yRange), np.max(yRange)], zorder = field.z_order)
            
    if field.export:
        export(currentPlane, field, plotter)
#        meta = {"cmap": field.colormap, "extent": [np.min(xRange), np.max(xRange), np.min(yRange), np.max(yRange)] , "vmin:": field.clip_min,"vmax:": field.clip_max }
#        export(meta, field, plotter, prefix = "meta")
        
        
#        export(np.column_stack(particles.X ,particles.Y ,particles.Z ,particles.PX ,particles.PY ,particles.PZ ,particles.Tag ,particles.Weight, particles.E), particles, plotter, prefix = "all")








