# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 13:44:21 2018

@author: Paul Scherkl
"""
import numpy as np
from .plotStyleUtils import get_label_from_key, get_unit_from_component, get_figure_labels, set_axis_label, get_axis_ticks








def draw_line_axes(fig, axMain, plotter, lineAxisList, gridData):
    
    from plotter.lines import split_axis_directions
    lineAxesX, lineAxesY = split_axis_directions(lineAxisList)
            
    def format_line_axis(axis, key, data, kind = "vert"):
        """ helper function to format axis color, labels, ticks"""

        axis.yaxis.tick_right()                  if kind == "vert" else None
        axis.spines['right'].set_color(data[3])  if kind == "vert" else axis.spines['top'].set_color(data[3])
        axis.spines['left'].set_visible(False)   if kind == "vert" else axis.spines['bottom'].set_visible(False)
        
        ticks = tickLabels = power = 0
        if kind == "vert":
            trans = axis.transAxes.transform([(0,0), (1,1)])
            x = axis.get_figure().get_dpi() / (trans[1,0] - trans[0,0])/72
            axis.yaxis.set_label_coords( (plotter.labelSpacing + 15 )*x, 0.5)

            targetAxis  =  key.split(",")[1].split(",")[0]
            plane =  key.split(",")[2].split(",")[0]
            

            if targetAxis == plane[0]: # Line axis equals xAxis of plotter
                
                ticks, tickLabels, power = get_axis_ticks(data[0], data[1]) 
                set_axis_label(axis, key, power, plotter.labelSize, color = data[3])
                
            
            if targetAxis not in plane:  # Line axis is neither x nor y axis of field -> create new axis 
                if targetAxis == "x":
                    minVal = 0
                    maxVal = gridData["boxSize"][0]
                else:
                    idx = 1 if targetAxis == "y" else 2
                    minVal = -0.5 * gridData["boxSize"][idx]
                    maxVal =  0.5 * gridData["boxSize"][idx]
                
                ticks = np.linspace(minVal, maxVal, 6, dtype = int)
                tickLabels = ticks
                axis.set_ylabel("$"+targetAxis+"$ ($\mathrm{\mu m}$)", size = plotter.labelSize, color = data[3])
                
        else:
           ticks, tickLabels, power = get_axis_ticks(data[0], data[1]) 
           set_axis_label(axis, key, power, plotter.labelSize, color = data[3], kind = "x")
        if np.max(ticks) == np.min(ticks):
            tickLabels = ["", "0", ""]
            ticks = [-1, 0,1]
        axis.set_ylim(np.min(ticks), np.max(ticks)) if kind == "vert" else axis.set_xlim(np.min(ticks), np.max(ticks))
        axis.invert_xaxis()    if kind is not "vert" and not data[5] else None
        axis.set_yticks(ticks) if kind == "vert" else axis.set_xticks(ticks) 
        axis.set_xticks([])    if kind == "vert" else axis.set_yticks([]) 
        axis.set_yticklabels( tickLabels )  if kind == "vert" else axis.set_xticklabels( tickLabels ) 
        ticklines = axis.get_yticklines()   if kind == "vert" else axis.get_xticklines()
        [tick.set_color(data[3]) for tick in ticklines]
        ticklabels = axis.get_yticklabels() if kind == "vert" else axis.get_xticklabels()
        [label.set_fontsize(plotter.tickSize) for label in ticklabels]
        [label.set_color(data[3]) for label in ticklabels]
        
                    

    axPos = axMain.get_position()
    figWidth = fig.get_figwidth() 
    
    for i in range(len(lineAxesX)):

        axisData = lineAxesX[i][list(lineAxesX[i].keys())[0] ]
        start = axPos.x1 + (i*(plotter.colorbarSpacing)/figWidth  )
        end   = 0.001/figWidth    
        axis = fig.add_axes([ start ,    axPos.y0,   end ,     axPos.height])
        
        format_line_axis(axis, list(lineAxesX[i].keys())[0], axisData)
        if axisData[5]: 
            axis.invert_yaxis()
      
    numLineAxes = len(lineAxesX)
    counterTop = 0
    counter = 0

    for i in range(len(lineAxesY)):
        # axisData = lineAxesY[i].items()[0]
        axisData = lineAxesY[i][list(lineAxesY[i].keys())[0] ]
        # key  = axisData[0]
        key  = list(lineAxesY[i].keys())[i]
        # data = axisData[1]
        data = axisData

        figHeight = fig.get_figheight() 
        

        startX = axPos.x1 + ((counter + numLineAxes)*(plotter.colorbarSpacing)/figWidth  )
        startY = axPos.y1 + ((counterTop + 1)*(plotter.colorbarSpacing * 0.5)/figHeight  )
        endX   = 0.001/figWidth 
        endY   = 0.001/figHeight   

        targetAxis  =  key.split(",")[1].split(",")[0]
        plane =  key.split(",")[2].split(",")[0]

        if targetAxis == plane[1]: # Line axis equals left yAxis of field
            axMain.spines['left'].set_color(data[3])       
            [tick.set_color(data[3]) for tick  in axMain.get_yticklines() ]
            [label.set_color(data[3])  for label in axMain.get_yticklabels()]
            axMain.yaxis.label.set_color(data[3])
        else:
            axisRight = fig.add_axes([ startX ,    axPos.y0,   endX ,     axPos.height])
            format_line_axis(axisRight, key, data, kind = "vert")
            counter += 1
            
        counterTop += 1
        
        axisTop   = fig.add_axes([ axPos.x0, startY, axPos.width,  endY])
        format_line_axis(axisTop,   key, data, kind = "hor")






def draw_colorbars(fig, axMain, plotter, colorBarList, lineAxisList):
  
    numLineAxes = sum( [(key.split(",")[1].split(",")[0] is not key.split(",")[2].split(",")[0][1]) for key in lineAxisList] )

    
                                                                           
    axList = []
    axPos = axMain.get_position()
    
    figWidth = fig.get_figwidth() 


    numColbars = len(colorBarList)
    for i in range(numColbars):
        start = axPos.x1 + ( (0.1  +  (i + numLineAxes)*(plotter.colorbarWidth + plotter.colorbarSpacing))/figWidth  )
        end   = plotter.colorbarWidth/figWidth
        axis = fig.add_axes([ start ,    axPos.y0,   end ,     axPos.height])
        axList.append( axis )
        
    def fillColbars(axis, colbarInfo):
        """ helper function to format colorbar ticks, labels, colormap etc"""
        import matplotlib.pyplot as plt
        minVal = colbarInfo[0]
        maxVal = colbarInfo[1]
        ticks, tickLabels, power = get_axis_ticks(minVal, maxVal)
        sm = plt.cm.ScalarMappable(cmap= colbarInfo[3], norm=plt.Normalize(vmin=np.min(ticks), vmax=np.max(ticks)))
        sm._A = []
        cbar  = fig.colorbar(sm, cax = axis, orientation='vertical')   
        cbar.set_alpha(1)
        
        cbar.set_ticks(ticks)
        axis.set_yticklabels( tickLabels )
        for label in axis.get_yticklabels():
            label.set_fontsize(plotter.tickSize )

        set_axis_label(axis, key, power, plotter.labelSize)
        trans = axis.transAxes.transform([(0,0), (1,1)])
        x = axis.get_figure().get_dpi() / (trans[1,0] - trans[0,0])/72
        axis.yaxis.set_label_coords( plotter.labelSpacing*x, 0.5)

    if colorBarList: 
        counter = 0
        for key in colorBarList:     # separate into Fields and Particles to make Fields always appear first (style issue only)
            if len( key.split(",") )> 1:
                axis = axList[counter]
                fillColbars(axis, colorBarList[key])
                counter += 1    
        for key in colorBarList:
            if len( key.split(",") ) == 1:
                axis = axList[counter]
                fillColbars(axis, colorBarList[key])
                counter += 1    
        
          
    
    
    
    
    
    
    
                    
            
    
    
def get_axis_list(plot, gridData):
    """
    Checks all dump objects stored in Plotter object for requested Line axes
            
        
    Returns
    -------
    # list (min, max, bool, color)
    
    """
    def assign_vals(line, data):
        """ helper function"""
        line.tick_min = data[0]
        line.tick_max = data[1]
        if not line.force_color:
            line.color    = data[3]
        line.invert_axis =  int(data[5])
        

    outputList = {}
    if hasattr(plot, 'fields'):
        for fld in plot.fields:
            for line in fld.lines:
                line.plane = fld.plane
                outputList = find_common_plot_settings(line, outputList, gridData=gridData, field = fld)
                
        for key in outputList:
            for fld in plot.fields:
                for line in fld.lines:
                    if key.split(",")[1] == str(line.axis) and key.split(",")[2] == str(fld.plane) and key.split(",")[3] == str(fld.kind) and key.split(",")[4] == str(line.component) :
                        assign_vals(line, outputList[key])
                        if line.force_color:  outputList[key][3] = line.color

    if hasattr(plot, 'particles'):

        for ptcl in plot.particles:
            for line in ptcl.lines:
                line.plane = ptcl.plane
                outputList = find_common_plot_settings(line, outputList, particles = ptcl, gridData = gridData)
                
        for key in outputList:
            for ptcl in plot.particles:
                for line in ptcl.lines:
                    if key.split(",")[1] == line.axis  and key.split(",")[2] == ptcl.plane and key.split(",")[3] == line.quantity:
                        assign_vals(line, outputList[key])
                        if line.force_color:  outputList[key][3] = line.color

    return outputList    
       



def get_colorbar_list(plot, gridData):
    """
    Checks all dump objects stored in Plotter object for requested colorbars
    
    Parameters
    ----------
    plot: Plotter2D or PlotterPhaseSpace
        Object that might contain loaded Particles and/or Field objects
        
        
    Returns
    -------
    # list (min, max, bool, colormap)
    
    """
    
    def assign_vals(obj, data):
        """ helper function"""
        obj.clip_min = outputList[key][0]
        obj.clip_max = outputList[key][1]
        obj.colormap = outputList[key][3]

    outputList = {}
    if hasattr(plot, 'fields'):
        for fld in plot.fields:
            if fld.plot_data:
                outputList = find_common_plot_settings(fld, outputList, plot = plot, gridData = gridData)
        for key in outputList:
            for fld in plot.fields:
                if key.split(",")[2] ==  fld.plane and key.split(",")[3].split(",")[0] == str(fld.kind) and key.split(",")[4].split(",")[0] == str(fld.component):
                    
                    assign_vals(fld, outputList[key])
    
    for ptcl in plot.particles:
        if ptcl.plot_data:
            outputList = find_common_plot_settings(ptcl, outputList)
    for key in outputList:
        for ptcl in plot.particles:
            if key.split(",")[3] == ptcl.colorCodeQuantity:
                assign_vals(ptcl, outputList[key])
    return outputList    







def find_common_plot_settings(obj, outputList, plot = None, gridData = None, field = None, particles = None):
    """
    Checks current object for requested colorbars
            
    Returns
    -------
    # list (min, max, bool, colormap)
    
    """
    from dumps   import Particles, Field, FieldLine, ParticlesLine
    from plotter.lines import get_line_data_field, get_line_data_particles
    from  dumps.dumpUtils.particlesUtils import get_particles_vector_from_string
    from  dumps.dumpUtils.fieldUtils import get_field_plane
    
    if (isinstance(obj, (Particles, Field)) and not obj.show_colorbar) or (isinstance(obj, (FieldLine, ParticlesLine)) and not obj.show_axis):
        return outputList
    
    
    currentKey = None
    if isinstance(obj, (Particles, Field)):
        if isinstance(obj, Particles):
            currentKey = "ptcl,0,0," + str( obj.colorCodeQuantity  )
        else:
            currentKey = "fld,0," + str(obj.plane) + "," + str(obj.kind) + "," + str(obj.component) 
            
    elif isinstance(obj, (FieldLine, ParticlesLine)):
        if isinstance(obj, FieldLine) :
            currentKey = "fldLine," +  str(obj.axis) + "," + str(field.plane) + "," + str(field.kind) + "," + str(obj.component) 
        else: 
            currentKey = "ptclLine," +  str(obj.axis) + "," + str(particles.plane) + "," + (obj.quantity) 
     
    if currentKey is not None:

        switchList = []
        if not currentKey in outputList:
            outputList[currentKey] = []

        minVal = 0
        maxVal = 0
        if isinstance(obj, (Particles, Field)):
            if obj.loaded:
                data = get_particles_vector_from_string(obj, currentKey.split(",")[-1]) if isinstance(obj, Particles) else get_field_plane(obj, gridData)
            else:
                data = [0,0]
        elif isinstance(obj, (FieldLine, ParticlesLine)):
                idx = 1 if obj.axis == obj.plane[0] else 0
                if (isinstance(obj, FieldLine) and not field.loaded) or  (isinstance(obj, ParticlesLine) and not particles.loaded): data = [0,0]
                else:  
                    data = get_line_data_field(obj, field, gridData)[idx] if isinstance(obj, FieldLine) else get_line_data_particles(obj, particles, gridData)[idx]
                    if data is None:
                        data = [0,0]
        userRequestSwitch = [0,0] # corresponds to min and max val. 0: no requested clip, 1 = requested clip
        if (isinstance(obj, (Particles, Field)) and obj.clip_min is None) or (isinstance(obj, (FieldLine, ParticlesLine)) and obj.tick_min is None):
            minVal = np.min(data)
        else:
            minVal = obj.clip_min if isinstance(obj, (Particles, Field)) else obj.tick_min
            userRequestSwitch[0] = 1
        if (isinstance(obj, (Particles, Field)) and obj.clip_max is None) or (isinstance(obj, (FieldLine, ParticlesLine)) and obj.tick_max is None):
            maxVal = np.max(data)
        else:
            maxVal = obj.clip_max if isinstance(obj, (Particles, Field)) else obj.tick_max
            userRequestSwitch[1] = 1
            
        entry3 = obj.colormap if isinstance(obj, (Particles, Field)) else obj.color if not obj.force_color else ""
        entry4 = int(obj.show_colorbar) if isinstance(obj, (Particles, Field)) else int(obj.show_axis)
        entry5 = 0 if isinstance(obj, (Particles, Field)) else int(obj.invert_axis)
        
        switchList = [minVal, maxVal, userRequestSwitch, entry3, entry4, entry5]

        if not outputList[currentKey]:
            outputList[currentKey] = switchList
        else:
            showEntry = np.max( ( int(outputList[currentKey][4]), entry4  )   )
            minVal = 0
            maxVal = 0
            userRequestSwitch = [0, 0]


            if outputList[currentKey][2][0] == 0 and switchList[2][0] == 0:
                minVal = min(outputList[currentKey][0], switchList[0])
                userRequestSwitch[0] = 0       
            if outputList[currentKey][2][1] == 0 and switchList[2][1] == 0:
                maxVal = max(outputList[currentKey][1], switchList[1])
                userRequestSwitch[1] = 0       
                
            
            if outputList[currentKey][2][0] == 1 and switchList[2][0] == 0:
                minVal  = outputList[currentKey][0]
                userRequestSwitch[0] = 1
            if outputList[currentKey][2][1] == 1 and switchList[2][1] == 0:
                maxVal  = outputList[currentKey][1]
                userRequestSwitch[1] = 1
                
                
            if outputList[currentKey][2][0] == 0 and switchList[2][0] == 1:
                minVal  = switchList[0]
                userRequestSwitch[0] = 1
                
            if outputList[currentKey][2][1] == 0 and switchList[2][1] == 1:
                maxVal  = switchList[1]
                userRequestSwitch[1] = 1
                 
            if outputList[currentKey][2][0] == 1 and switchList[2][0] == 1:
                minVal = min(outputList[currentKey][0], switchList[0])
                userRequestSwitch[0] = 1
                
            if outputList[currentKey][2][1] == 1 and switchList[2][1] == 1:
                maxVal = max(outputList[currentKey][1], switchList[1])
                userRequestSwitch[1] = 1
                
            outputList[currentKey] = [minVal, maxVal, userRequestSwitch, outputList[currentKey][3], showEntry, outputList[currentKey][5]]
                    
                
    return outputList
  
    
    
    
    