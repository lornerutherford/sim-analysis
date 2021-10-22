# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 17:11:56 2018

@author: P. Scherkl
"""

class Line(object):
    """
    class defines the structure of all line operations
    """
    
    def __init__(self, axis = None,  x_range = None, y_range = None, z_range = None, show_range = None, operation = None, tick_min = None, tick_max = None,\
                 invert_axis = None, show_axis = None, color = None, force_color = None, z_order = None, export = None, plot_data = None, fill = None):
        
        self.axis = axis
        
        self.show_axis   = show_axis
        
        self.x_range = x_range if isinstance(x_range, (float, int)) or (isinstance(x_range, (list, tuple)) and len(x_range) == 2) or x_range is None else x_range[0] 
        self.y_range = y_range if isinstance(y_range, (float, int)) or (isinstance(y_range, (list, tuple)) and len(y_range) == 2) or y_range is None else y_range[0] 
        self.z_range = z_range if isinstance(z_range, (float, int)) or (isinstance(z_range, (list, tuple)) and len(z_range) == 2) or z_range is None else z_range[0] 
        self.show_range = show_range
        
        self.operation   = operation
        
        self.tick_min = tick_min
        self.tick_max = tick_max
        self.invert_axis = invert_axis

        self.color    = color
        self.force_color = force_color 
        self.z_order  = z_order
        self.line_style = "-"
        self.line_width = 1

        self.export = export
        self.plot_data = plot_data
        self.fill = fill


def plot_lines(ax, obj, gridData, plotter ):
    from dumps import Particles, Field
    from utils.miscUtils import export
    import numpy as np
    
    if obj.lines is not None: 
        
        lineIDs =  set( line.quantity for line in obj.lines) if isinstance(obj, Particles) else set( str(line.axis) + "," + obj.kind + "," + str(line.component) + "," + str(line.plane) for line in obj.lines)       #group all lines with similar settings
        

        for ID in lineIDs:
            axLine  = None
            counter = 0
            for line in obj.lines:
                x = y =  lineBounds = 0
                
                
                if not line.plot_data: continue
                
                if isinstance(obj, Field): 
                    if not ID == str(line.axis) + "," + obj.kind + "," + str(line.component) + "," + str(line.plane): continue
                    x,y, lineBounds = get_line_data_field(line, obj, gridData)
                    
                
                if isinstance(obj, Particles) :
                    if not ID == line.quantity: continue
                    x,y, lineBounds = get_line_data_particles(line, obj, gridData)
                if x is None: continue
                
                cellSizeX = 1.0
                cellSizeY = 1.0
                if "cellSize" in gridData:
                    cellSizeX = gridData["cellSize"][0] if line.plane[0] == "x" else gridData["cellSize"][1] if line.plane[0] == "y" else gridData["cellSize"][2]
                    cellSizeY = gridData["cellSize"][0] if line.plane[1] == "x" else gridData["cellSize"][1] if line.plane[1] == "y" else gridData["cellSize"][2]
            
                if line.axis == line.plane[0]:
                    axLine = ax.twinx() if counter == 0 else axLine
                    axLine.plot(x , y , color = line.color, zorder = line.z_order, ls = line.line_style , lw = line.line_width)

                    if line.fill != None:
                        if (isinstance(line.fill, (list,tuple)) and (len(line.fill) == 2) and isinstance(line.fill[1], float) and (line.fill[0] == "above" or "below")):
                            
                            if line.fill[0] == "above":
                                axLine.fill_between(x, y, line.fill[1], where = y >= line.fill[1], alpha = 0.1, color = line.color, zorder = line.z_order)
                            elif line.fill[0] == "below":
                                axLine.fill_between(x, y, line.fill[1], where = y <= line.fill[1], alpha = 0.1, color = line.color, zorder = line.z_order)
                        
                        else:
                            print ("\n(!) Warning: fill: expected format is [\"above\", float] or [\"below\", float]. Ignored")
                       
                    if line.export:
                        export(np.column_stack( (x - 0.5*cellSizeX,y) ), line, plotter)
                    
                    axLine.set_ylim(line.tick_min, line.tick_max)
                    
                    axLine.spines['right'].set_visible(False)
                    axLine.spines['left'].set_visible(False)
                    axLine.invert_yaxis() if counter == 0 and line.invert_axis else None
                    axLine.set_yticks([])
                    
                else:
                    import matplotlib.pyplot as plt
                    axLine = ax.twiny() if counter == 0 else axLine
                    
                    def trafo(x):
                        a = b = 0
                        if line.axis == "x":
                            a = 0
                            b = gridData["boxSize"][0]
                        else:
                            idx = 1 if line.axis == "y" else 2
                            a = -0.5 * gridData["boxSize"][idx]
                            b =  0.5 * gridData["boxSize"][idx]

                        c, d = ax.get_ylim()
                        return (c-d)/(a-b)*x + (c-a*d/b)/(1-a/b)

                    axLine.plot(x, trafo(y)-0.5*cellSizeY, color = line.color, zorder = line.z_order, ls = line.line_style , lw = line.line_width )
                    if line.export:
                        export(np.column_stack(( x,trafo(y)-0.5*cellSizeY )), line, plotter)
                    
                    axLine.set_xlim(line.tick_min, line.tick_max)
                                        
                    axLine.spines['top'].set_visible(False)
                    axLine.spines['right'].set_visible(False)
                    axLine.spines['left'].set_visible(False)
                    axLine.spines['bottom'].set_visible(False)
                    axLine.set_xticks([])
                    
                    axLine.invert_xaxis() if counter == 0 and not line.invert_axis else None
                    
                axLine.patch.set_visible(False)
                if line.show_range: plot_line_bounds(ax, obj.plane, lineBounds, line.color, gridData)
                counter += 1
                
                
                
                
                
def plot_line_bounds(axis, plane, lineBounds, color, gridData):
    import matplotlib.patches as patches   
    import dumps.dumpUtils.fieldUtils as fU
    xMin = lineBounds[0][0] if plane[0] == "x" else lineBounds[1][0] if plane[0] == "y" else lineBounds[2][0]
    xMax = lineBounds[0][1] if plane[0] == "x" else lineBounds[1][1] if plane[0] == "y" else lineBounds[2][1]
    yMin = lineBounds[0][0] if plane[1] == "x" else lineBounds[1][0] if plane[1] == "y" else lineBounds[2][0]
    yMax = lineBounds[0][1] if plane[1] == "x" else lineBounds[1][1] if plane[1] == "y" else lineBounds[2][1]
    xMin =     fU.get_position_from_cellIndex(xMin,  plane[0], gridData)
    xMax =     fU.get_position_from_cellIndex(xMax,  plane[0], gridData)
    yMin =     fU.get_position_from_cellIndex(yMin,  plane[1], gridData)
    yMax =     fU.get_position_from_cellIndex(yMax,  plane[1], gridData)

    axis.add_patch( patches.Rectangle(      (xMin, yMin),  xMax - xMin, yMax - yMin,    alpha=0.5  , facecolor = color, zOrder = 10 ))
    
    
    
    
def split_axis_directions(lines):
    axisListX = []
    axisListY = []
    for key in lines:
        axis  =  key.split(",")[1].split(",")[0]
        plane =  key.split(",")[2].split(",")[0]
        if axis == plane[0]:
            axisListX.append({key:lines[key]})
        else:
            axisListY.append({key:lines[key]})
    return axisListX, axisListY






def get_line_data_particles(line, ptcl, gridData):
    """
    Function extracts Particles values for requested line tool. 
    Returns projection as array
    """
    import numpy as np
    import dumps.dumpUtils.particlesUtils as pU
    
    xMin= xMax= yMin= yMax= zMin= zMax = 0
    if line.x_range is None and line.y_range is None and line.z_range is None: # default setup, select all particles within box
        xMax = gridData["boxSize"][0] 
        yMin = -0.5*gridData["boxSize"][1] 
        yMax =  0.5*gridData["boxSize"][1] 
        zMin = -0.5*gridData["boxSize"][2] 
        zMax =  0.5*gridData["boxSize"][2] 
    else:
        xRange = 0 if line.x_range is None else line.x_range
        yRange = 0 if line.y_range is None else line.y_range
        zRange = 0 if line.z_range is None else line.z_range
        
        xMin =  xRange if isinstance(xRange, (int, float)) else np.min(xRange)
        xMax =  xRange if isinstance(xRange, (int, float)) else np.max(xRange)
        
        if np.abs(xMax-xMin) < line.bin_size:
            if xMax + line.bin_size < gridData["boxSize"][0]:
                xMax += line.bin_size
            else:
                xMin -= line.bin_size
        
        
        yMin =  yRange if isinstance(yRange, (int, float)) else np.min(yRange)
        yMax =  yRange if isinstance(yRange, (int, float)) else np.max(yRange)
        if np.abs(yMax-yMin) < line.bin_size:
            if yMax + line.bin_size < -0.5*gridData["boxSize"][1]:
                yMax += line.bin_size
            else:
                yMin -= line.bin_size
        
        zMin =  zRange if isinstance(zRange, (int, float)) else np.min(zRange)
        zMax =  zRange if isinstance(zRange, (int, float)) else np.max(zRange)
        if np.abs(zMax-zMin) < line.bin_size:
            if zMax + line.bin_size < -0.5*gridData["boxSize"][2]:
                zMax += line.bin_size
            else:
                zMin -= line.bin_size
        
    lineBounds= [[xMin, xMax], [yMin, yMax], [zMin, zMax]]

    if line.axis == "x":
        lineX = np.arange(xMin, xMax + line.bin_size , line.bin_size)
        lineY = pU.get_binned_quantity(line.axis, lineX, line.bin_size, line.quantity, ptcl)
        
    elif line.axis == "y":
        lineY = np.arange(yMin, yMax + line.bin_size , line.bin_size)
        lineX = pU.get_binned_quantity(line.axis, lineY, line.bin_size, line.quantity, ptcl)
        
    elif line.axis == "z":
        lineY = np.arange(zMin, zMax + line.bin_size , line.bin_size)
        lineX = pU.get_binned_quantity(line.axis, lineY, line.bin_size, line.quantity, ptcl)
    
    
    return lineX, lineY,lineBounds




def get_line_data_field(line, field, gridData):
    """
    Function extracts field values for requested line tool. 
    First, identify the cell indices from position values provided by user, then slice field matrix 
    Sliced matrix then gets processed and projected to requested axis
    Returns projection as array
    """
    
    import numpy as np
    import dumps.dumpUtils.fieldUtils as fU

    xMin= xMax= yMin= yMax= zMin= zMax = 0
    if line.x_range is None and line.y_range is None and line.z_range is None: # default setup, produce line along full x axis centered on y=z=0
        xMax = gridData["numCells"][0] - 1
        yMin = yMax = fU.get_cellIndex_from_position(0,  "y", gridData)
        zMin = zMax = fU.get_cellIndex_from_position(0,  "z", gridData)
        
    else: # at least one direction is requested by user
        xRange = 0 if line.x_range is None else line.x_range
        yRange = 0 if line.y_range is None else line.y_range
        zRange = 0 if line.z_range is None else line.z_range

        xMin =  fU.get_cellIndex_from_position(xRange,  "x", gridData) if isinstance(xRange, (int, float)) else fU.get_cellIndex_from_position(np.min(xRange),  "x", gridData)
        xMax =  fU.get_cellIndex_from_position(xRange,  "x", gridData) if isinstance(xRange, (int, float)) else fU.get_cellIndex_from_position(np.max(xRange),  "x", gridData)
        if xMin == xMax:
            if xMax < gridData["numCells"][0]: 
                xMax += 1
            else:
                xMin -= 1
        
        yMin =  fU.get_cellIndex_from_position(yRange,  "y", gridData) if isinstance(yRange, (int, float)) else fU.get_cellIndex_from_position(np.min(yRange),  "y", gridData)
        yMax =  fU.get_cellIndex_from_position(yRange,  "y", gridData) if isinstance(yRange, (int, float)) else fU.get_cellIndex_from_position(np.max(yRange),  "y", gridData)
        if yMin == yMax:
            if yMax < gridData["numCells"][1]: 
                yMax += 1
            else:
                yMin -= 1


        zMin =  fU.get_cellIndex_from_position(zRange,  "z", gridData) if isinstance(zRange, (int, float)) else fU.get_cellIndex_from_position(np.min(zRange),  "z", gridData)
        zMax =  fU.get_cellIndex_from_position(zRange,  "z", gridData) if isinstance(zRange, (int, float)) else fU.get_cellIndex_from_position(np.max(zRange),  "z", gridData)
        if zMin == zMax:
            if zMax < gridData["numCells"][2]: 
                zMax += 1
            else:
                zMin -= 1
    
    lineBounds= [[xMin, xMax], [yMin, yMax], [zMin, zMax]]
    

    
    if line.component < -1 or line.component > np.shape(field.fieldMatrix)[3] - 1:
        print ("\n(!) Warning: requested line component " + str(line.component) + " out of range [-1, " + str(np.shape(field.fieldMatrix)[3] - 1) +"] for given field " + field.name + ", ignored")
        return None, None, None

    fldMatrix = field.fieldMatrix if line.component is not -1 else np.sqrt( np.sum( field.fieldMatrix[:, :, :, i]**2 for i in range(3)) )
    lineY = lineX = 0
    if line.axis == "x":
        if xMax - xMin <= 1:
            print ("\n(!) Warning: line axis: x, but requested extent in x <= 1. Ignored")
            return None, None, None

        if line.operation == "mean":
            lineY = np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 2) if line.component > -1 else np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 2)
            lineY = np.mean(lineY, axis = 1)

        elif line.operation == "sum":
            lineY = np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 2) if line.component > -1 else np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 2)
            lineY = np.sum(lineY, axis = 1)
        lineX = np.linspace(fU.get_position_from_cellIndex(xMin, "x", gridData), fU.get_position_from_cellIndex(xMax, "x", gridData), num=len(lineY))
        
        
    if line.axis == "y":
        if yMax - yMin <= 1:
            print ("\n(!) Warning: line axis: y, but requested extent in y <= 1. Ignored")
            return None, None, None
        
        if line.operation == "mean":
            lineY = np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 2) if line.component > -1 else np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 2)
            lineY = np.mean(lineY, axis = 0)
            
        elif line.operation == "sum":
            lineY = np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 2) if line.component > -1 else np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 2)
            lineY = np.sum(lineY, axis = 0)
        lineX = np.linspace(fU.get_position_from_cellIndex(yMin, "y", gridData), fU.get_position_from_cellIndex(yMax, "y", gridData), num=len(lineY))
        
        
    if line.axis == "z":
        if zMax - zMin <= 1:
            print ("\n(!) Warning: line axis: z, but requested extent in z <= 1. Ignored")
            return None, None, None
        
        if line.operation == "mean":
            lineY = np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 0) if line.component > -1 else np.mean(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 0)
            lineY = np.mean(lineY, axis = 0)
            
        elif line.operation == "sum":
            lineY = np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax, line.component], axis = 0) if line.component > -1 else np.sum(fldMatrix[xMin:xMax, yMin:yMax, zMin:zMax], axis = 0)
            lineY = np.sum(lineY, axis = 0)
        lineX = np.linspace(fU.get_position_from_cellIndex(zMin, "z", gridData), fU.get_position_from_cellIndex(zMax, "z", gridData), num=len(lineY))
    

    if line.calculus != None:

        if line.calculus == "integrate":
            # calculate cumulative trapezoidal integral, in negative <axis> direction (usually box front to back)
            from scipy.integrate import cumulative_trapezoid as ct
            lineY = -1.*(ct(lineY[::-1], lineX[::-1], axis=0, initial=lineY[-1]))[::-1]
            
        
        elif line.calculus == "cumsum":
            # calculate cumulative sum of values, in negative <axis> direction (usually box front to back)
            # (this is similar to integration when additionally normalising with the cell size in <axis> direction, but not equal.
            # for calculating, e.g., the electrostatic potential from an electric field line, "integrate" is more accurate (but requires scypi))
            lineY = (np.cumsum(lineY[::-1], axis=0, dtype=np.float32))[::-1]

        elif line.calculus == "differentiate":
            # calculate second order accurate central differences, in negative <axis> direction (usually box front to back)
            lineY = -1.*np.gradient(lineY, lineX, axis = 0, edge_order = 1)

        else:
            print ("\n(!) Warning: calculus: unrecognised parameter" + str(line.calculus) + ". Ignored\nvalid options are \"integrate\" or \"differentiate\"")


    if line.normalize != None:        
        if isinstance(line.normalize, float):
            lineY = lineY * line.normalize

        else:
            print ("\n(!) Warning: normalize: " + str(line.normalize) + " is not a float. Ignored")

    
    if line.gauge != None:
        if isinstance(line.gauge, float):
            lineY = lineY - line.gauge
        
        elif line.gauge == "min":
            lineY = lineY - np.min(lineY)

        elif line.gauge == "max":
            lineY = lineY - np.max(lineY)

        else:
            print ("\n(!) Warning: gauge: " + str(line.gauge) + " is neither a float, nor \"min\" or \"max\". Ignored")


    if field.plane[0] == line.axis: 
        return lineX, lineY, lineBounds 
    else:
        return lineY, lineX, lineBounds








