# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:40:16 2018

@author: Paul Scherkl
"""


from utils.miscUtils import copy_object

import numpy as np

def empty(field):
    """ deletes complete field matrix """
    field.loaded       = 0
    field.fieldMatrix  = None


def get_cellIndex_from_position(position, direction, gridData):
    """
    Returns the cell index corrsponding to a given position. Uses the default picViz coordinate system
    """
    
    dirIdx = 0 if direction == "x" else 1 if direction == "y" else 2
    idx = 0
    
    if direction == "x":
        idx = int(float(position) / gridData["cellSize"][0])
    else:
        idx = int(gridData["numCells"][dirIdx]/2.) + int(float(position) / gridData["cellSize"][dirIdx])
        
    idx = 0 if idx < 0 else idx
    idx = gridData["numCells"][dirIdx]  if idx > gridData["numCells"][dirIdx] else idx
    return idx
 

def get_position_from_cellIndex(index,  direction, gridData):
    dirIdx = 0 if direction == "x" else 1 if direction == "y" else 2
    pos = 0
    if direction == "x":
        pos = gridData["cellSize"][0]*index
    else:
        pos = gridData["cellSize"][dirIdx]*index - gridData["numCells"][dirIdx]*gridData["cellSize"][dirIdx]/2.
        
    return pos
        


    
def get_field_extent(fld, gridData):
    plane = fld.plane
    
    xRange = []
    if plane == "xy":
        xRange = [0,  gridData["numCells"][0] * gridData["cellSize"][0]  ]
        yRange = [-1.*gridData["numCells"][1] * gridData["cellSize"][1]/2.0 ,  gridData["numCells"][1] * gridData["cellSize"][1]/2.0 ]
        
    elif plane == "yx":
        yRange = [0,  gridData["numCells"][0] * gridData["cellSize"][0]  ]
        xRange = [-1.*gridData["numCells"][1] * gridData["cellSize"][1]/2.0 ,  gridData["numCells"][1] * gridData["cellSize"][1]/2.0  ]
        
    elif plane == "xz":
        xRange = [0,  gridData["numCells"][0] * gridData["cellSize"][0]  ]
        yRange = [-1.*gridData["numCells"][2] * gridData["cellSize"][2]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][2]/2.0  ]
        
    elif plane == "zx":
        yRange = [0,  gridData["numCells"][0] * gridData["cellSize"][0]  ]
        xRange = [-1.*gridData["numCells"][2] * gridData["cellSize"][2]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][2]/2.0   ]
        
    elif plane == "yz":
        xRange = [-1.*gridData["numCells"][1] * gridData["cellSize"][1]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][1]/2.0   ]
        yRange = [-1.*gridData["numCells"][2] * gridData["cellSize"][2]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][2]/2.0   ]
        
    elif plane == "zy":
        yRange = [-1.*gridData["numCells"][1] * gridData["cellSize"][1]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][1]/2.0   ]
        xRange = [-1.*gridData["numCells"][2] * gridData["cellSize"][2]/2.0 ,  gridData["numCells"][2] * gridData["cellSize"][2]/2.0   ]
        
    return xRange, yRange




def get_field_plane(fld, gridData, component = None):
    plane = fld.plane
    planeOffset = fld.plane_offset

    
    comp = component if component is not None else fld.component
    if comp < -1 or comp > np.shape(fld.fieldMatrix)[3] - 1:
        print ("\n(!) Warning: requested Field component " + str(comp) + " out of range [-2, " + str(np.shape(fld.fieldMatrix)[3] - 1) +"] for given Field " + fld.name + ", ignored")
        shp = np.shape(fld.fieldMatrix)
        return np.zeros(  (shp[0], shp[1], shp[2])   )
    
    matrix = 0    
    if comp > -1:
        matrix = fld.fieldMatrix
    else:
        shp = np.shape(fld.fieldMatrix)
        matrix = np.zeros(  (shp[0], shp[1], shp[2])   )
        for i in range( len( fld.fieldMatrix[0,0,0] )):
            if comp == -2 and i == 0:
                continue
            matrix += fld.fieldMatrix[:, :, :, i]**2 
        matrix = np.sqrt(matrix)
    
    
    
    if plane == "xy":
         if fld.project == 1:
             return np.transpose(np.sum( matrix[:, :, :, comp], axis = 2))
         elif fld.project == 2:
             return np.transpose(np.mean( matrix[:, :, :, comp], axis = 2))
         elif fld.project == 0:
             zPos = int( (gridData["numCells"][2])/2. + 1 + int(planeOffset/gridData["cellSize"][2]))
             if comp > -1:
                 return np.transpose(matrix[:, :, zPos , comp])
             else:
                 return np.transpose(matrix[:, :, zPos])

    if plane == "yx":
         if fld.project == 1:
             return np.sum( matrix[:, :, :, comp], axis = 2)
         elif fld.project == 2:
             return np.mean( matrix[:, :, :, comp], axis = 2)
         elif fld.project == 0:
             zPos = int( (gridData["numCells"][2])/2. + 1 + int(planeOffset/gridData["cellSize"][2]))
             if comp > -1:
                 return matrix[:, :, zPos , comp]
             else:
                 return matrix[:, :, zPos]


    if plane == "xz":
         if fld.project == 1:
             return np.transpose(np.sum( matrix[:, :, :, comp], axis = 0))
         elif fld.project == 2:
             return np.transpose(np.mean( matrix[:, :, :, comp], axis = 0))
         elif fld.project == 0:
             yPos = int( (gridData["numCells"][1])/2. + 1 + int(planeOffset/gridData["cellSize"][1]))
             if comp > -1:
                 return np.transpose(matrix[:, yPos, : , comp])
             else:
                 return np.transpose(matrix[:, yPos, :])

    if plane == "zx":
         if fld.project == 1:
             return np.sum( matrix[:, :, :, comp], axis = 0)
         elif fld.project == 2:
             return np.mean( matrix[:, :, :, comp], axis = 0)
         elif fld.project == 0:
             yPos = int( (gridData["numCells"][1])/2. + 1 + int(planeOffset/gridData["cellSize"][1]))
             if comp > -1:
                 return matrix[:, yPos, : , comp]
             else:
                 return matrix[:, yPos, :]



    if plane == "yz":
         if fld.project == 1:
             return np.transpose(np.sum( matrix[:, :, :, comp], axis = 1))
         elif fld.project == 2:
             return np.transpose(np.mean( matrix[:, :, :, comp], axis = 1))
         elif fld.project == 0:
             xPos = int( (gridData["numCells"][0])/2. + 1 + int(planeOffset/gridData["cellSize"][0]))
             if comp > -1:
                 return np.transpose(matrix[xPos, :, : , comp])
             else:
                 return np.transpose(matrix[xPos, :, :])


    if plane == "zy":
         if fld.project == 1:
             return np.sum( matrix[:, :, :, comp], axis = 1)
         elif fld.project == 2:
             return np.mean( matrix[:, :, :, comp], axis = 1)
         elif fld.project == 0:
             xPos = int( (gridData["numCells"][0])/2. + 1 + int(planeOffset/gridData["cellSize"][0]))
             if comp > -1:
                 return matrix[xPos, :, : , comp]
             else:
                 return matrix[xPos, :, :]
        
    
    

    