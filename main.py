# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl


picViz main file. 
This file sets up the code and controls data processing
"""

#### for use on headless systems (e.g. cluster) uncomment the two following lines


import inspect
import matplotlib
matplotlib.use('agg')





def default_style():
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    matplotlib.rcParams['mathtext.fontset'] = 'custom'
    matplotlib.rcParams['font.sans-serif'] = "DejaVu Sans"
    matplotlib.rcParams['mathtext.cal'] = 'DejaVu Sans'
    matplotlib.rcParams['mathtext.it'] = 'DejaVu Sans:italic'
    matplotlib.rcParams['mathtext.rm'] = 'DejaVu Sans'
    matplotlib.rcParams['text.usetex'] = False



class picVIZ(object):
    """Top level class setting up and executing the main program""" 
    
    
    def __init__(self, pathToData, dumpNumbers, outPath = "", style = "default", isHeadless = 0):
        """

        Parameters
        ----------
        pathToData: string, required
            Points to the folder where simulated files are located
            
        dumpNumbers: list, required
            The dumps that will be loaded and processed
            
        style: string
            Path/filename of matplotlib style file applied to all plots
            
        isHeadless: bool, optional
            If set to 0, picViz can run on systems without monitor (e.g. clusters)
            
        outPath: string
            Directory (will be created if not present) where picViz output will be stored
            
        Returns
        -------
        Object of class picVIZ        
            
        """

        if isHeadless:
            matplotlib.use('Agg')
            
            
        if style.lower().find("default") == -1:
            try:
                matplotlib.style.use(style)
            except:
                default_style()
        else:
            default_style()
            
            
            
            
        import utils.mainUtils
        utils.mainUtils.print_start_message()
        
        self.pathToData   = pathToData
        self.outPath      = outPath if len(outPath)> 0 else pathToData
        
        
        self.dumpNumbers  = dumpNumbers
    
        self.fldIndex     = 0
        self.ptclIndex    = 0
        self.globalPlotterList    = []
        self.globalAnalyzerList   = []


        
        
    def execute(self, print_progress = False, print_metaData = False, print_gridData = False):
        """
        Central function. Iterates all dumpNumbers, calls loading, processing and plotting routines
        
        
        Parameters
        ----------
        print_progress: bool, optional
            Switch on/off printing of general progress information
            
        print_metaData: bool, optional
            Switch on/off printing of meta data
            
        print_gridData: bool, optional
            Switch on/off printing of grid data
            
            
        """
        
        from plotter.figureHandler          import make_plots
        from dataAnalyzer.analyzerHandler   import analyze_data
        from dataReader.readerUtils         import set_load_switches,get_meta_data, load_data
        from utils                          import mainUtils
        
        
        globalPlotterList, globalAnalyzerList = set_load_switches(self.globalPlotterList, self.globalAnalyzerList)
        
        
        get_meta_data(print_metaData, self.pathToData, globalPlotterList, globalAnalyzerList)
        analDataList = [[] for i in range(len(globalAnalyzerList))]
        
        for dumpNumber in self.dumpNumbers:         # start main loop iterating all dump numbers

            print ("\n\n       ----- Process dump " + str( dumpNumber) + " -----\n" )
            
            # load particle and field files, collect grid information

            tmpPtclObjs, tmpFldObjs, tmpGridData = load_data(print_progress, print_gridData, self.pathToData,  dumpNumber, globalPlotterList, globalAnalyzerList )

            
            #analyze loaded data
            tmpAnalyzerList = mainUtils.set_analyzer_copies(globalAnalyzerList, tmpPtclObjs, tmpFldObjs)
            analDataList    = analyze_data(tmpAnalyzerList, tmpGridData, dumpNumber, dumpNumber == self.dumpNumbers[0], analDataList)


            #make figures
            tmpPlotterList = mainUtils.setup_plotter_copies(globalPlotterList, tmpPtclObjs, tmpFldObjs) #TODO: add analyzer plotter 
            make_plots(tmpPlotterList, tmpGridData, dumpNumber)    #TODO: add analyzer plotter 
            
        
        
        print ("\npicViz has finished. Great Success!")
        



    def add_particles(self, species_name, plane = "xy", show_ratio = 1., opacity = 1., marker_size = 2, \
                      color = None, plot_data = 1,  z_order = 2, file_kind = "vsim", export = 0 ):
        """
        Generates new Particles object
        
        
        Parameters
        ----------
        species_name: string, required
            Name of particle species. 
            
        plane: string
            Defines Field plane to be plotted. Can be "xy", "yx", "xz", "zx", "yz" or "zy"
        
        show_ratio: float, 1 >= showratio > 0
            Defines ratio of particles shown in plots. Does not affect statistical information
            
        opacity: float, 1 >= opacity >= 0
            Defines overall opacity for particles in plots
            
        marker_size: float, > 0
            Defines size of scatter dots
        
        plot_data: bool
            Defines if data is plotted. Associated Lines may still be plotted
        
        color: string or list with 3 to 4 entries
            Color of dots
            
        z_order: int > 0
            Defines position of Particles within plot. Higher values correspond to front layers
        
        file_kind: string
            Defines which file structure is used for the loading routine. Currently, only "vsim" is implemented
            
        export: bool
            Dump plotted data to txt file
    
        Returns
        -------
        Particles object that allows to set up and manipulate        
        """

        from dumps  import Particles

        if color is None:
            import random 
            color= [random.random(), random.random(), random.random()]

        
        newParticlesObj = Particles(species_name, self.ptclIndex, plane = plane, z_order = z_order, \
                                    show_ratio = show_ratio, opacity = opacity, marker_size = marker_size, color = color, \
                                    plot_data = plot_data, file_kind = file_kind, export=export)
        self.ptclIndex += 1
        
        
        return newParticlesObj
        
    
        
    
    
    def add_field(self, species_name, kind = None, component = -1, plane = "xy",  plane_offset = 0, project = 0, \
                  opacity = 1., colormap = "Reds",  clip_min = None, clip_max = None, plot_data = 1, show_colorbar = 1,\
                  z_order = 1, file_kind = "vsim",export = 0):
        
        """
        Generates new Field object
        
        
        Parameters
        ----------
        species_name: string, required
            Name of field species. 
        
        kind: string
            treats field as if it was of a certain kind. can be electric, magnetic, currdens or chargedens
            
        component: int
            Defines field component that is shown. 
            component >= 0 directly selects the component from given field matrix
            component = -1: geometric sum of all field components
            component = -2: geometric sum of transverse field components (if applicable)
            
            
        plane: string
            Defines Field plane to be plotted. Can be "xy", "yx", "xz", "zx", "yz" or "zy"

        
        plane_offset: float
            Defines position of requested plane on third axis (e.g. for xy plane, planeOffset moves the plane in z direction)

        project: int
            Projects field matrix to plane defined in plotter.             
            if =1: projection sums all values per cell column
            if =2: projection averages all values per cell column 
            
        opacity: float, 1 >= opacity >= 0
            Defines overall opacity for particles in plots
            
        colormap: string
            Name of matplotlib colormap
            
        clip_min: float
            Defines mininmal value for clipping of field values
            
        clip_max: float
            Defines maximal value for clipping of field values
            
        plot_data: bool
            Defines if data is plotted. Associated Lines may still be plotted
            
        show_colorbar: bool
            Defines if colorbar shall be shown in plot
            
        z_order: int > 0
            Defines position of field within plot. Higher values correspond to front layers
            
        file_kind: string
            Defines which file structure is used for the loading routine. Currently, only "vsim" is implemented

        export: bool
            Dump plotted data to txt file
    
        Returns
        -------
        Field object that allows to set up and manipulate        
        """
        
        from dumps import Field
        
        if len(plane) is not 2:
            print ("\n(!) Error in line " + str(inspect.currentframe().f_back.f_lineno) +  ": Invalid plane specified, use default \"xy\"")
            plane = "xy"


        if clip_min is not None and clip_max is not None:
            dummy = [clip_min, clip_max]
            clip_min = min(dummy)
            clip_max = max(dummy)


        newFieldObj = Field(species_name, index = self.fldIndex, kind = kind, component = component, plane=plane,  plane_offset=plane_offset,\
                            project = project, opacity = opacity, colormap = colormap, clip_min = clip_min, clip_max = clip_max,  show_colorbar = show_colorbar,\
                            plot_data =plot_data,  z_order = z_order, file_kind = "vsim", export=export)
        self.fldIndex += 1
        return newFieldObj
        
        

#        
    def add_2D_plot(self, particles = [], fields = [], plane = "xy",  plane_offset = 0, fig_size = [8,6], x_lim = [], y_lim = [], auto_aspect_ratio = True, show_sim_progress = 0, make_fig = 1, save_fig = 1, dpi = 500):
        """
        Generates new 2D plot object
        
        
        Parameters
        ----------
        particles: list, optional
            list of Particles objects that will be processed in this plot\\

            
        fields: list, optional
            list of Field objects that will be processed in this plot\\

            
        plane: string
            Defines Field plane to be plotted. Can be "xy", "yx", "xz", "zx", "yz" or "zy"
            Overwrites plane settings for all Field objects within this plot
        
        plane_offset: float
            Defines position of requested plane on third axis (e.g. for xy plane, planeOffset moves the plane in z direction)
            Overwrites plane settings for all Field objects within this plot
            
        fig_size: tuple or list with 2 entries
            Defines figure size in inches
        
        x_lim: tuple or list with 2 entries
            Defines range of shown x-axis in plot
            
        y_lim: tuple or list with 2 entries
            Defines range of shown y-axis in plot
        
        auto_aspect_ratio: bool
            Determines if aspect ratio is determined automatically (from passed axes limits or grid sizes) or is given by figSize.
            If True, the x-component of figSize will be set automatically
        
        show_sim_progress: string
            Shows the simulation step as time (show_sim_progress =  "t") or lenght (show_sim_progres = "x")
            Switch off with show_sim_progress = 0
        
        make_fig: bool
            defines if Plot shall be computed or not
        
        save_fig: bool or int
            defines if plot shall be saved or not
            use this number to also define the number of digits or leading zeros in the numbering system. (1: 1, 2: 01, 3: 001, 4: 0001 etc)
            
        dpi: float
            defines plot DPI
        
        Returns
        -------
        2D plot object that allows to set up and manipulate the output        
        """
        from plotter  import Plotter2D
        from dumps    import Particles, Field
        from utils.miscUtils import copy_object
        
        if plane is not None:
            if len(plane) is not 2:
                print ("\n(!) Error in line " + str(inspect.currentframe().f_back.f_lineno) +  ": Invalid plane specified, use default \"xy\"")
                plane = "xy"
            
            

        localPtclObj = []
        for globalPtclObj in particles:
            localPtclObj.append( copy_object(globalPtclObj, Particles() ) )
            localPtclObj[-1].index = self.ptclIndex
            self.ptclIndex += 1
            
        localFldObj = []
        for globalFlObj in fields:
            localFldObj.append( copy_object(globalFlObj, Field() ) )
            localFldObj[-1].index = self.fldIndex
            self.fldIndex += 1

        newPlotter         = Plotter2D( particles = localPtclObj, fields = localFldObj, plane= plane,  plane_offset=plane_offset, fig_size=fig_size, x_lim=x_lim, y_lim=y_lim,\
                                       auto_aspect_ratio=auto_aspect_ratio, make_fig=make_fig, save_fig=save_fig, show_sim_progress = show_sim_progress, dpi = dpi)
        newPlotter.outPath = self.outPath
        set_plotter_defaults(newPlotter)
        
        self.globalPlotterList.append( newPlotter )
        return  newPlotter
    
    
     

    def add_phasespace_plot(self, particles = [], direction = "x", fig_size = [5,5], x_lim = [], y_lim = [], show_sim_progress = 0, make_fig = 1, save_fig = 1, dpi = 500):
        """
        Generates new phase space plot object
        
        
        Parameters
        ----------
        particles: list, optional
            list of Particles objects that will be processed in this plot
            
        
        direction: string
            Defines plane of requested phase space. Can be x, t,y, or z
            

        fig_size: tuple or list with 2 entries
            Defines figure size in inches
        
        x_lim: tuple or list with 2 entries
            Defines range of shown x-axis in plot
            
        y_lim: tuple or list with 2 entries
            Defines range of shown y-axis in plot
        
        show_sim_progress: string
            Shows the simulation step as time (show_sim_progress =  "t") or lenght (show_sim_progres = "x")
            Switch off with show_sim_progress = 0
            
        make_fig: bool
            defines if Plot shall be computed or not
        
        save_fig: bool
            defines if plot shall be saved or not
            
        dpi: float
            defines DPI of plot
        
        Returns
        -------
        Phase space object that allows to set up and manipulate the output        
        """
        from plotter import PlotterPhaseSpace
        from dumps   import Particles
        from utils.miscUtils import copy_object
        
            
        localPtclObj = []
        for globalPtclObj in particles:
            localPtclObj.append( copy_object(globalPtclObj, Particles() ) )
            localPtclObj[-1].index = self.ptclIndex
            self.ptclIndex += 1
            
        newPlotter         = PlotterPhaseSpace( particles=localPtclObj, direction=direction, fig_size=fig_size, x_lim=x_lim, y_lim=y_lim, show_sim_progress=show_sim_progress,make_fig=make_fig, save_fig=save_fig , dpi = dpi )
        newPlotter.outPath = self.outPath
        set_plotter_defaults(newPlotter)
            
        
        self.globalPlotterList.append( newPlotter )
        return newPlotter
    
    
    
    
    def add_hist_plot(self, particles = [], quantx ="e", bin_size = 0.2, log_x = 0, log_y = 0, fig_size = [5,5], x_lim = [], y_lim = [],  show_sim_progress = 0, make_fig = 1, save_fig = 1, dpi = 300):
        
        from plotter import PlotterHist
        from dumps   import Particles
        from utils.miscUtils import copy_object
        
        localPtclObj = []
        for globalPtclObj in particles:
            localPtclObj.append( copy_object(globalPtclObj, Particles() ) )
            localPtclObj[-1].index = self.ptclIndex
            self.ptclIndex += 1
            
        newPlotter         = PlotterHist( particles=localPtclObj, quantx=quantx, bin_size = bin_size, log_x=log_x, log_y = log_y,  fig_size=fig_size, x_lim=x_lim, y_lim=y_lim, show_sim_progress=show_sim_progress,make_fig=make_fig, save_fig=save_fig , dpi = dpi )
        newPlotter.outPath = self.outPath
        set_plotter_defaults(newPlotter)
        
        self.globalPlotterList.append( newPlotter )
        return newPlotter


    def add_multi_plot(self, plot_list = [], grid = [], fig_height = 6, make_fig = 1, save_fig = 1, dpi = 500, axisSpacingX = 1.4,axisSpacingY = 1.1):
        """
        Generates new multiplot object
        
        
        Parameters
        ----------
        plot_list: list, required
            list containing all defined obecjts of type Plot to be included in the multi plot
            
        grid: list
            Shape of multiplot matrix. Each entry defines the number of plots per row.  If empty, all plots will be in the same row
            
        fig_height: float
            Defines figure height in inches. Width is determined by individual plot widths
        
        make_fig: bool
            defines if plot shall be computed or not
        
        saveFig: bool
            defines if plot shall be saved or not
            
        Returns
        -------
        Multiplot object that allows to set up and manipulate the output        
            
        """

        from plotter  import Plotter2D, PlotterPhaseSpace, MultiPlot, PlotterHist
        from utils.miscUtils import copy_object

        if not grid:
            grid = [len(plot_list)]
        temp_plotList = []
        
        for plotter in plot_list:
            if isinstance(plotter, Plotter2D):
                temp_plotList.append( copy_object(plotter, Plotter2D() ) )
                for fld in plotter.fields:
                    fld.index = self.fldIndex
                    self.fldIndex += 1

            elif isinstance(plotter, PlotterPhaseSpace):
                temp_plotList.append( copy_object(plotter, PlotterPhaseSpace() ) )
                
            elif isinstance(plotter, PlotterHist):
                temp_plotList.append( copy_object(plotter, PlotterHist() ) )
            for ptcl in plotter.particles:
                ptcl.index = self.ptclIndex
                self.ptclIndex += 1

                
        newPlotter         = MultiPlot( plotters =temp_plotList, fig_height=fig_height,  grid=grid, make_fig=make_fig, save_fig=save_fig , dpi = dpi , axisSpacingX = axisSpacingX, axisSpacingY = axisSpacingY)
        newPlotter.outPath = self.outPath
        self.globalPlotterList.append( newPlotter )
        return newPlotter
        



    


    def add_particles_analyzer(self, particles = [], quantityList = [], bin_size = 0.1, print_data = True, save_txt = True, save_summary_txt = True, file_name = None, use_existing_file = False, headers = 1):
        """
        Generates new ParticlesAnalyzer object
        
        
        Parameters
        ----------
        particles: list
            list of Particles objects that will be processed 
            
        quantityList: list 
            List of strings with quantities to be calculated
            The quantity of the Particles species that will be displayed. Can be any Particles property (x,y,z, px, py, pz, t, e, etrans, .., mean values calculated) and any string of the following list:
                q : charge
                i : mean current
                ipeak : peak current, uses bin_size
                widthx, widthxmax,widthy, widthymax, widthz, widthzmax: r.m.s or maximum width in given direction
                posx, posxlab, posy, posz: mean position of beam in given direction
                divy, divz : r.m.s divergence
                emity, emitydisp, emitz, emitzdisp: emittance in given direction. "disp" adds dispersion term
                emax : max energy of Particles
                espread: relative r.m.s energy spread
                edev: r.m.s energy spread
                etotal: total kinetic beam energy in J
                gamma: mean gamma factor
                b5: 5D brightness , uses bin_size
                b6, b601, b6001 : 6D brightness. numbers at the end correspond to the fraction of the bandwidth factor applied to formula, uses bin_size
                twissay, twissby, twissgy, twissaz, twissbz, twissgz: twiss parameters
        
        
        
        print_data: bool
            Print data to terminal
            
        save_txt: bool
            Save data to txt file
            
        save_summary_txt: bool
            Save data printed to terminal into txt (overwrite old by restart of picViz)
            
        file_name: string
            prefix for analyzer output file names. If None, a generic string will be used
            
        use_existing_file: bool
            if true, picViz tries to add output data to an existing txt file. Otherwise, any existing file with identical name will be overwritten
            
        headers: int
            Change the headings of the txt file
                1 : Quantity and Units on one single line (default)
                2 : Quantity and Units on two separate lines
            
        Returns
        -------
        ParticlesAnalyzer object that controls statistical post-processing        
        """
        
        from dataAnalyzer import ParticlesAnalyzer
        from utils.miscUtils import copy_object
        from dumps import Particles
        

        localPtclObj = []
        for globalPtclObj in particles:
            localPtclObj.append( copy_object(globalPtclObj, Particles() ) )
            
        newAnalyzer         = ParticlesAnalyzer( localPtclObj, quantityList=quantityList, bin_size = bin_size, print_data=print_data, save_txt = save_txt, save_summary_txt = save_summary_txt, file_name = file_name, use_existing_file=use_existing_file, headers=headers )
        newAnalyzer.outPath = self.outPath
        self.globalAnalyzerList.append( newAnalyzer )
        return newAnalyzer


#
#
#    def add_field_analyzer(self, fields = []):
#        """
#        Generates new FieldAnalyzer object
#        
#        
#        Parameters
#        ----------
#        fields: list, optional
#            list of Field species that will be processed \\
#
#            
#        Returns
#        -------
#        FieldAnalyzer object that controls statistical post-processing        
#        """
#        newAnalyzer         = FieldAnalyzer( fields, self.fieldObjList )
#        newAnalyzer.outPath = self.outPath
#        self.globalAnalyzerList.append( newAnalyzer )
#        return newAnalyzer
#



def set_plotter_defaults(plotter):
    plotter.tickSize        = 15
    plotter.labelSize       = 18
    plotter.colorbarWidth   = 0.1
    plotter.colorbarSpacing = 1.7
    plotter.labelSpacing    = 70
    plotter.labelSpacingX   = 40
    plotter.labelSpacingY   = 55
    

