# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
picViz class for 2D real space plots (inherited from Plotter class)
provides framework to produce arbitrary plots for particle and field species

"""


from plot import Plotter
import numpy as np


class Plotter2D(Plotter):
    
    def __init__(self, particles = None, fields = None, plane = None, plane_offset = None, fig_size = None, x_lim = None, y_lim = None, auto_aspect_ratio =  None,  show_sim_progress = None, make_fig  = None, save_fig  = None, dpi = None):
        """
        
        Initializes Plotter2D object and creates local copies of global Particles and Field objects.
        
        Parameters
        ----------
            
     
        particles: list
            Global Particles objects.  
            
            
        fields: list
            Global Field objects.  
        
        plane: string
            Defines plane to be plotted. Can be "xy", "yx", "xz", "zx", "yz" or "zy"
        
        plane_offset: float
            Defines position of requested plane on third axis (e.g. for xy plane, plane_offset moves the plane in z direction)

        figSize: tuple or list with 2 entries
            Defines figure size in inches
        
        x_lim: tuple or list with 2 entries
            Defines range of shown x-axis in plot
            
        y_lim: tuple or list with 2 entries
            Defines range of shown y-axis in plot
        
        auto_aspect_ratio: bool
            Determines if aspect ratio is determined automatically or just given by figSize
            
            
        Returns
        -------
        Object of class Plotter2D     
            
        """
        
        Plotter.__init__(self, fig_size,  make_fig, save_fig, dpi)

        self.particles = particles
        self.fields  = fields

        self.auto_aspect_ratio = auto_aspect_ratio
        self.x_lim  = x_lim
        self.y_lim  = y_lim
        
        
        
        self.plane = plane.lower() if plane is not None else None
        self.plane_offset = plane_offset
        
        self.show_sim_progress = show_sim_progress
        
        self.tickSize        = None
        self.labelSize       = None
        self.labelSpacing    = None
        self.labelSpacingX   = None
        self.labelSpacingY   = None
        self.colorbarWidth   = None
        self.colorbarSpacing = None
        
        
        
        




def check_Plotter2D_axis_limits(plot, gridData):
    from plotter import MultiPlot

    if isinstance(plot, Plotter2D):
        check_axis_limits(plot, gridData)
    elif isinstance(plot, MultiPlot):
        for plotter in plot.plotters:
            if isinstance(plotter, Plotter2D):
                check_axis_limits(plotter, gridData)


def check_axis_limits(plot2D, gridData):
    if not plot2D.x_lim:

        if plot2D.plane == "xy" or plot2D.plane == "xz":
            plot2D.x_lim = (0, gridData["boxSize"][0])
        elif plot2D.plane == "yx" or plot2D.plane == "yz":
            plot2D.x_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
        elif plot2D.plane == "zx" or plot2D.plane == "zy":
            plot2D.x_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)
        else:
            if plot2D.fields:
                if plot2D.fields[0].plane == "xy" or plot2D.fields[0].plane == "xz":
                    plot2D.x_lim = (0, gridData["boxSize"][0])
                elif plot2D.fields[0].plane == "yx" or plot2D.fields[0].plane == "yz":
                    plot2D.x_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
                elif plot2D.fields[0].plane == "zx" or plot2D.fields[0].plane == "zy":
                    plot2D.x_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)
            else:
                for ptcl in plot2D.particles:
                    if ptcl.plane == "xy" or ptcl.plane == "xz":
                        plot2D.x_lim = (0, gridData["boxSize"][0])
                    elif ptcl.plane == "yx" or ptcl.plane == "yz":
                        plot2D.x_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
                    elif ptcl.plane == "zx" or ptcl.plane == "zy":
                        plot2D.x_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)
                
            
            
            


    if not plot2D.y_lim:

        if plot2D.plane == "yx" or plot2D.plane == "zx":
            plot2D.y_lim = (0, gridData["boxSize"][0])
        elif plot2D.plane == "xy" or plot2D.plane == "zy":
            plot2D.y_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
        elif plot2D.plane == "xz" or plot2D.plane == "yz":
            plot2D.y_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)
        else:

            if plot2D.fields:

                
                if plot2D.fields[0].plane == "yx" or plot2D.fields[0].plane == "zx":
                    plot2D.y_lim = (0, gridData["boxSize"][0])
                elif plot2D.fields[0].plane == "xy" or plot2D.fields[0].plane == "zy":
                    plot2D.y_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
                elif plot2D.fields[0].plane == "xz" or plot2D.fields[0].plane == "yz":
                    plot2D.y_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)
            else:
                for ptcl in plot2D.particles:

                    if ptcl.plane == "yx" or ptcl.plane == "zx":
                        plot2D.y_lim = (0, gridData["boxSize"][0])
                    elif ptcl.plane == "xy" or ptcl.plane == "zy":
                        plot2D.y_lim = (-gridData["boxSize"][1]/2., gridData["boxSize"][1]/2.)
                    elif ptcl.plane == "xz" or ptcl.plane == "yz":
                        plot2D.y_lim = (-gridData["boxSize"][2]/2., gridData["boxSize"][2]/2.)





    
    
                
def plotter2D_makeFigure(plotter, fig, ax, gridData):
    from dumps.field     import plot_field
    from dumps.particles import plot_particles
    from plotter.lines   import plot_lines
    from plotter.plotStyleUtils import show_sim_progress
    from plotter.plotStyleUtils import format_plotter_axes
    
    for field in plotter.fields:   
        if field.loaded:
            if field.plot_data: plot_field(ax, plotter, field, gridData)
            plot_lines(ax, field, gridData, plotter)
            
            
    for particles in plotter.particles:
        if particles.loaded:
            if particles.plot_data: plot_particles(ax, plotter, particles )
            plot_lines(ax, particles, gridData, plotter)
    
    format_plotter_axes(ax, plotter)        
    if plotter.show_sim_progress is not 0:
        show_sim_progress(ax, plotter, gridData, kind = plotter.show_sim_progress)
                
    
    
    
    
    
    
    
    
    

        