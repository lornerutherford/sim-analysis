# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""
from dump import Dump
from plotter import Line
import numpy as np

class Particles(Dump):
    """
    Class containing the particle data 
    
    
    Main attributes
    ---------------
    - x, y, z : 1darrays 
                contain the Cartesian positions of the macroparticles [um]
                
    - uz, uy, uz : 1darrays  
                contain the unitless momenta(i.e. px/mc, py/mc, pz/mc)
                
    - E, Ex, Ey, Ez : 1darrays  
                contain the Energies(in certain directions) [MeV]
    
    
    Utility attributes
    ---------------
    -name : string
                name of particle speciess
    
    -loaded : bool 
                defines if file is processed lateron or ignored 
    
    """   
    
    
    def __init__(self, name = None, index= None,  plane = None, show_ratio = None, opacity =None, z_order = None, marker_size = None, color = None, file_kind = None, plot_data = None):
        
        
        Dump.__init__(self, name = name, index = index, plane =plane, z_order=z_order, file_kind = file_kind, plot_data = plot_data)
        

        self.numPtclsInMacro = None
        self.X      = None
        self.Y      = None
        self.Z      = None
        self.PX     = None   
        self.PY     = None
        self.PZ     = None
        self.Tag    = None
        self.Weight = None
        self.YP     = None
        self.ZP     = None
        self.T      = None
        self.E      = None
        self.EX     = None  
        self.EY     = None  
        self.EZ     = None
        self.Etrans = None
        
        self.show_ratio  = show_ratio
        self.opacity    = opacity
        self.marker_size = marker_size
        self.color      = color
        
        self.cutList = None
        
        
        self.colorCode         = None
        self.colorCodeQuantity = None
        
        self.transparancyCodeQuantity = None
        self.transparencyClipMin      = None
        self.transparencyClipMax      = None
        self.transparencyReverse      = None
        
        self.trans_clip_min = None
        self.trans_clip_max = None


    def color_code(self, quantity, colormap = "inferno", show_colorbar = True, clip_min = None, clip_max = None):
        """
        Applies color coding of all particles depending on chosen quantity 
        
        Parameters
        ----------
        quantity: string
            Name of the requested quantity. Can be X, Y, Z, PX, PY, PZ, YP, ZP, T, Tag, Weight, E, Ex, Ey, Ez, Etrans [lower case works as well]
        
        colormap: string
            Name of matplotlib colormap
            
        show_colorbar: bool
            Defines if colorbar shall be shown in plot
        
        clip_min: float
            Defines mininmal value for clipping 
            
        clip_max: float
            Defines maximal value for clipping 
        """
        
        
        from matplotlib import pyplot as plt
        self.colormap          = plt.cm.get_cmap(colormap)
        self.colorCode         = 1
        self.show_colorbar      = show_colorbar
        self.colorCodeQuantity = quantity.lower()
        
        if clip_min is not None and clip_max is not None:
            dummy = [clip_min, clip_max]
            self.clip_min = min(dummy)
            self.clip_max = max(dummy)
        else:
            self.clip_min = clip_min
            self.clip_max = clip_max
            
    
    def transparency_code(self, quantity, trans_clip_min = None, trans_clip_max = None, reverse = 0):
        
        """
        Applies transparency coding of all particles depending on chosen quantity. 
        The coding is applied linearly within the min/max values of the quantity or is clipped by clip_min, clip_max
        Lower values correspond to more transparency.
        
        Parameters
        ----------
        quantity: string
            Name of the requested quantity. Can be X, Y, Z, PX, PY, PZ, YP, ZP, T, Tag, Weight, E, Ex, Ey, Ez, Etrans [lower case works as well]
        
        trans_clip_min: float
            Defines mininmal value for transparency clipping ( e.g. vals < clip_min will be treated as if they equal clip_min )
            
        trans_clip_max: float
            Defines maximal value for transparency clipping ( e.g. vals > clip_max will be treated as if they equal clip_max )
            
        reverse: bool
            If True, higher values correspond to more transparency and vice versa
        
        """
        
        import colormaps as customColMaps
        from matplotlib import pyplot as plt
        
        self.colorCode         = 1
        self.transparancyCodeQuantity = quantity.lower()
        self.transparencyReverse = reverse
        if trans_clip_min is not None and trans_clip_max is not None:
            dummy = [trans_clip_min, trans_clip_max]
            self.trans_clip_min = min(dummy)
            self.trans_clip_max = max(dummy)
        else:
            self.trans_clip_min = trans_clip_min
            self.trans_clip_max = trans_clip_max


    
    def cut(self, quantity, val1, val2):        
        """
        Removes all single particles with given quantity outside of interval given by val1 and val2
        
        Parameters
        ----------
        quantity: string
            Name of the requested quantity. Can be X, Y, Z, PX, PY, PZ, YP, ZP, T, Tag, Weight, E, Ex, Ey, Ez, Etrans [lower case works as well]
        
        val1: float
            First interval boundary for requested cut
            
        val2: float
            Second interval boundary for requested cut

        """
        if self.cutList is None:
            self.cutList = []
        self.cutList.append( [quantity.lower(), min((val1,val2)), max((val1,val2))] )




    def addLine(self, axis = "x", quantity = None, bin_size = 0.2, x_range = None, y_range = None, z_range = None, show_range = 0, \
                operation = "mean", tick_min = None, tick_max = None, color = None, force_color= 0, invert_axis = 0, show_axis = 1, z_order = 3):
        """
        Interface for Line operations on Particles dumps. 
        User can define line or volume from which to extract data by using range-variables
        Creates new axis including ticks and labels on bottom or right hand side of figure
        
        
        Parameters
        ----------
        
        axis: string
            Defines main-axis of Line. Can be "x", "y" or "z"
        
        quantity: string
            The quantity of the Particles species that will be displayed. Can be any Particles property (will show it's mean) and any string of the following list:
                q : charge
                i : current
                widthx, widthxmax,widthy, widthymax, widthz, widthzmax: r.m.s or maximum width in given direction
                posx, posxlab, posy, posz : mean position of beam in given direction
                divy, divz : r.m.s divergence
                emity, emitydisp, emitz, emitzdisp: emittance in given direction. "disp" refers to dispersion term
                emax : max energy of Particles
                espread: relative r.m.s energy spread
                edev: r.m.s energy spread
                etotal: total kinetic beam energy in J
                gamma: mean gamma factor
                b5: 5D brightness
                b6, b601, b6001 : 6D brightness. numbers at the end correspond to the fraction of the bandwidth factor applied to formula
                twissay, twissby, twissgy, twissaz, twissbz, twissgz: twiss parameters
    
        bin_size: float
            Binning of the requested quantity [um] along axis
            
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

        tick_min: float
            Defines mininmal value for Line axis tick labels
            
        tick_max: float
            Defines maximal value for Line axis tick labels
            
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
            
        Returns
        -------
        Line object that controls line plotting    
        """
        
        if color is None:
            import random 
            color= [random.random(), random.random(), random.random()]
        
        if tick_min is not None and tick_max is not None:
            dummy = [tick_min, tick_max]
            tick_min = min(dummy)
            tick_max = max(dummy)
            
        
        newLineObj = ParticlesLine(quantity = quantity, bin_size = bin_size, axis = axis, x_range = x_range, y_range = y_range, z_range = z_range, \
                                   show_range = show_range, operation = operation, tick_min = tick_min, tick_max = tick_max, color = color, force_color = force_color, invert_axis = invert_axis,\
                                   show_axis = show_axis, z_order=z_order)
                
        if self.lines is None:
            self.lines = []
        self.lines.append( newLineObj ) # add new entry for particles. add the object. load switch is off, will be enabled if this object is used in any plotter or analyzer
        return newLineObj



class ParticlesLine(Line):
    """
    Class containing line operations dedicated to Particles objects 
    """
    
    def __init__(self, quantity = None, bin_size = None, axis = None,  x_range = None, y_range = None, z_range = None, show_range = None, operation = None, \
                 tick_min = None, tick_max = None, color = None, force_color = None, invert_axis = None, show_axis = None, z_order = None):
        
        Line.__init__(self, axis = axis, x_range = x_range, y_range = y_range, z_range = z_range, show_range = show_range, operation = operation, \
                      tick_min = tick_min, tick_max = tick_max, color = color, force_color = force_color,invert_axis = invert_axis, show_axis = show_axis,z_order = z_order)
        
        self.quantity = quantity
        self.bin_size = bin_size




def plot_particles(ax, plotter, particles ): 
    from plotter import Plotter2D, PlotterPhaseSpace
    import matplotlib.colors as colors
    from dumps.dumpUtils.particlesUtils import get_particles_vector_from_string, get_phaseSpace_vectors, get_particles_plane
    
    if isinstance(plotter, PlotterPhaseSpace):
        xAxis, yAxis = get_phaseSpace_vectors(particles, plotter.direction)
    elif isinstance(plotter, Plotter2D):
        xAxis, yAxis = get_particles_plane(particles, plotter)

    delStep = int(1.0/particles.show_ratio)
    
    if particles.colorCode is None:
        ax.scatter(xAxis[0::delStep], yAxis[0::delStep], alpha = particles.opacity, zOrder = particles.z_order, \
                   edgecolor = "", facecolor = particles.color, s = particles.marker_size)   
        
    else:
        from matplotlib.colors import Normalize
        
        colorVec = [list(colors.to_rgba(particles.color))]*len(xAxis)   # start with the normal color 
        if particles.colorCodeQuantity is not None: 
            quantity = get_particles_vector_from_string(particles, particles.colorCodeQuantity)
            minVal = np.min( quantity ) if particles.clip_min is None else particles.clip_min
            maxVal = np.max( quantity ) if particles.clip_max is None else particles.clip_max
            norm = Normalize(minVal, maxVal,  clip=True)(quantity)    
            colorVec =  list(particles.colormap(norm))
     
        if particles.transparancyCodeQuantity is not None: 
            transquant = get_particles_vector_from_string(particles, particles.transparancyCodeQuantity)

            if transquant.size > 0 :

                minVal = np.min( transquant ) if particles.trans_clip_min is None else particles.trans_clip_min
                maxVal = np.max( transquant ) if particles.trans_clip_max is None else particles.trans_clip_max
                
                mapping = 1./(maxVal - minVal)*transquant - minVal/(maxVal - minVal)

                mapping = mapping if not particles.transparencyReverse else 1.0 - mapping
                
                colorVec = np.asarray(colorVec)
                colorVec[:,3] =  mapping

                colorVec[:,3][colorVec[:,3] < 0 ]     = 0.0
                colorVec[:,3][colorVec[:,3] > 1.0]    = 1.0

        ax.scatter(xAxis[0::delStep], yAxis[0::delStep],  c = colorVec[0::delStep], zOrder = particles.z_order,  edgecolor = "", s = particles.marker_size)   
       