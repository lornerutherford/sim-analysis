# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:40:19 2018

@author: Paul Scherkl
"""

from dataAnalyzer    import ParticlesAnalyzer
from utils.miscUtils import copy_object
import numpy as np
import scipy.constants as const
       


def get_binned_quantity(axis, lineX, bin_size, quantity, ptclObj):
    from dumps.particles import Particles
    
    lineY = np.zeros(len(lineX))
    if ptclObj.loaded:
        for i in range(len(lineX)):
            x = lineX[i]
            localPtcl = copy_object(ptclObj, Particles())
            localPtcl.cut(axis, x, x + bin_size)
            make_particles_cuts(localPtcl)
            lineY[i] = get_quantity_from_string(localPtcl, quantity, bin_size,  line = 1)
    return lineY
    


def get_quantity_from_string(ptclObj, quantity, binSize, line = 0):

    
    if quantity.lower() == "q":
        return get_charge(ptclObj.Weight, ptclObj.numPtclsInMacro)
    
    elif quantity.lower() == "i":
        return np.mean(get_current(ptclObj.X, ptclObj.Weight, ptclObj.numPtclsInMacro, binSize)) if line == 0 else get_charge(ptclObj.Weight , ptclObj.numPtclsInMacro)* 1e-12 / (binSize*1e-6) * const.c 
    
    elif quantity.lower() == "ipeak":
        return get_current_peak(ptclObj.X, ptclObj.Weight, ptclObj.numPtclsInMacro, binSize) 
    
    elif quantity.lower() == "widthx":
        return get_rms(ptclObj.X, ptclObj.Weight)
    
    elif quantity.lower() == "widthxmax":
        return np.max(ptclObj.X) - np.min(ptclObj.X)
    
    elif quantity.lower() == "widthy":
        return get_rms(ptclObj.Y, ptclObj.Weight)
    
    elif quantity.lower() == "widthymax":
        return np.max(ptclObj.Y) - np.min(ptclObj.Y)
    
    elif quantity.lower() == "widthz":
        return get_rms(ptclObj.Z, ptclObj.Weight)
    
    elif quantity.lower() == "widthzmax":
        return np.max(ptclObj.Z) - np.min(ptclObj.Z)
    
    elif quantity.lower() == "posx":
        return get_mean(ptclObj.X, ptclObj.Weight)
    
    elif quantity.lower() == "posxlab":
       return get_mean(ptclObj.X, ptclObj.Weight) + ptclObj.xLab
    
    elif quantity.lower() == "posy":
        return get_mean(ptclObj.Y, ptclObj.Weight)
    
    elif quantity.lower() == "posz":
        return get_mean(ptclObj.Z, ptclObj.Weight)
    

    elif quantity.lower() == "divy":
        return get_rms(ptclObj.YP, ptclObj.Weight)
    
    elif quantity.lower() == "divz":
        return get_rms(ptclObj.ZP, ptclObj.Weight)
    
    elif quantity.lower() == "emity":
        return get_emittance(ptclObj, "y")
    
    elif quantity.lower() == "emitydisp":
        return get_emittance(ptclObj, "y", disp = 1)
    
    elif quantity.lower() == "emitz":
        return get_emittance(ptclObj, "z")
    
    elif quantity.lower() == "emitzdisp":
        return get_emittance(ptclObj, "z", disp = 1)
    
    elif quantity.lower() == "emax":
        return np.max(ptclObj.E)
    
    elif quantity.lower() == "edev":
        return get_rms(ptclObj.E, ptclObj.Weight)
    
    elif quantity.lower() == "espread":
        eMean = get_mean(ptclObj.E, ptclObj.Weight) 
        return get_rms(ptclObj.E, ptclObj.Weight) / eMean*100 if eMean is not 0 else 0
    
    elif quantity.lower() == "etotal":
        return  np.sum(ptclObj.E * 1e6  * ptclObj.Weight) * const.e * ptclObj.numPtclsInMacro
    
    elif quantity.lower() ==  "gamma":
        return get_mean(ptclObj.E, ptclObj.Weight)/const.value("electron mass energy equivalent in MeV"  )
    
    elif quantity.lower() == "b5":
        return get_5D_brightness(ptclObj, line, binSize)
    
    
    elif quantity.lower().find("b6") > -1:
        energySpreadUnitFactor = quantity.lower().split("b6")[1]
        energySpreadUnitFactor = 1e3 if energySpreadUnitFactor == "01" else 1e4 if energySpreadUnitFactor == "001" else 1e2 
        energyTerm =  get_mean(ptclObj.E, ptclObj.Weight) 
        energySpread = get_rms(ptclObj.E, ptclObj.Weight)
        if energyTerm == 0 or energySpread == 0:
            return 0
        return get_5D_brightness(ptclObj, line,binSize)/ (energySpread /energyTerm * energySpreadUnitFactor )
    
       
    elif quantity.lower().find("twissa") > -1:
        if quantity.lower()[-1] is not "y" and quantity.lower()[-1] is not "z":
            direction = "y"
        else:
            direction = quantity.lower()[-1]
        return get_twiss_alpha(ptclObj, direction)
    
    
    elif quantity.lower().find("twissb") > -1:
        if quantity.lower()[-1] is not "y" and quantity.lower()[-1] is not "z":
            direction = "y"
        else:
            direction = quantity.lower()[-1]
        return get_twiss_beta(ptclObj, direction)


    elif quantity.lower().find("twissg") > -1:
        if quantity.lower()[-1] is not "y" and quantity.lower()[-1] is not "z":
            direction = "y"
        else:
            direction = quantity.lower()[-1]
        return get_twiss_gamma(ptclObj, direction)
    
    
    else:
        vector = get_particles_vector_from_string(ptclObj, quantity)
        return get_mean(vector, ptclObj.Weight) if vector is not None else None
    



"""
check out https://indico.cern.ch/event/528094/contributions/2213316/attachments/1322590/1984069/L3-4-5_-_Transverse_Beam_Dynamics.pdf slide 34
"""

def get_twiss_alpha(ptclObj, direction):
    locVec = ptclObj.Y*1e-6   if direction == "y" else ptclObj.Z*1e-6
    momVec = ptclObj.PY   if direction == "y" else ptclObj.PZ
    n = np.sum(ptclObj.Weight)
    yPyOverPxMean   =  (1./n) * np.sum(ptclObj.Weight * locVec * (momVec/ptclObj.PX)) - (1./n**2)*np.sum(ptclObj.Weight*locVec) * np.sum(ptclObj.Weight*(momVec/ptclObj.PX)) 
    emittance = get_emittance(ptclObj, direction, geom = 1)

    # twiss_a = np.sqrt(get_twiss_beta(ptclObj, direction) * get_twiss_gamma(ptclObj, direction) -1.) # works as well
    twiss_a = -1. * yPyOverPxMean / emittance
    return twiss_a
    

def get_twiss_beta(ptclObj, direction):
    locVec = ptclObj.Y*1e-6   if direction == "y" else ptclObj.Z*1e-6
    n = np.sum(ptclObj.Weight)
    dirVec            = (1./n)*np.sum(ptclObj.Weight*(locVec**2)) - ((1./n)*np.sum(ptclObj.Weight*locVec))**2
    emittance = get_emittance(ptclObj, direction, geom = 1)
    twiss_b = (dirVec)/emittance # [m]

    return twiss_b


def get_twiss_gamma(ptclObj, direction):
    momVec = ptclObj.PY   if direction == "y" else ptclObj.PZ
    n = np.sum(ptclObj.Weight)
    dirVec     = (1./n)*np.sum(ptclObj.Weight*(momVec/ptclObj.PX)**2) - ((1./n)*np.sum(ptclObj.Weight*momVec/ptclObj.PX))**2
    emittance = get_emittance(ptclObj, direction, geom = 1)
    twiss_g = dirVec/emittance
    return twiss_g



def get_5D_brightness(ptclObj, line, binSize):
    current = get_current_peak(ptclObj.X, ptclObj.Weight, ptclObj.numPtclsInMacro, binSize) if line == 0 else get_current(ptclObj.X, ptclObj.Weight, ptclObj.numPtclsInMacro, binSize)
    emitY   = get_emittance(ptclObj, "y")
    emitZ   = get_emittance(ptclObj, "z")
    if emitY == 0 or emitZ == 0:
        return 0
    return 2 * current / ( emitY  * emitZ  )  



def get_current_peak(xVec, weights, numPtclsInMacro, bin_size):
    try:
        return np.max(get_current(xVec, weights, numPtclsInMacro, bin_size))
    except: return 0



def get_current(xVec, weights, numPtclsInMacro, bin_size):
    if len(xVec) == 0: return 0
    bins = np.arange(min(xVec), max(xVec), bin_size)
    current = np.zeros(len(bins))
    for i in range(len(bins) -1):
        current[i] = get_charge(weights[(xVec >= bins[i]) & (xVec < bins[i+1])] , numPtclsInMacro)* 1e-12 / (bin_size*1e-6) * const.c 
    return current


def get_charge(weights, numPtclInMacro):
    return const.e*numPtclInMacro * np.sum(weights)*1e12
    

def get_emittance(ptclObj, direction, geom = 0, disp = 0):
    locVec = ptclObj.Y   if direction == "y" else ptclObj.Z
    momVec = ptclObj.PY  if direction == "y" else ptclObj.PZ
    n = np.sum(ptclObj.Weight)
    if n == 0 or len(ptclObj.Weight) == 0:
        return 0
    
    ySquaredMean            = (1./n)*np.sum(ptclObj.Weight*(locVec**2)) - ((1./n)*np.sum(ptclObj.Weight*locVec))**2
    pyOverPxSquaredMean     = (1./n)*np.sum(ptclObj.Weight*(momVec/ptclObj.PX)**2) - ((1./n)*np.sum(ptclObj.Weight*momVec/ptclObj.PX))**2
    yPyOverPxMeanSquared    = ( (1./n) * np.sum(ptclObj.Weight * locVec * (momVec/ptclObj.PX)) - (1./n**2)*np.sum(ptclObj.Weight*locVec) * np.sum(ptclObj.Weight*(momVec/ptclObj.PX)) )**2
    gammaBeta = 1 if geom == 1 else  (1./n)*np.sum(ptclObj.Weight*ptclObj.PX)/const.c
        
    if disp == 0:
        if ySquaredMean * pyOverPxSquaredMean - yPyOverPxMeanSquared >=0:
            return gammaBeta * np.sqrt(ySquaredMean * pyOverPxSquaredMean - yPyOverPxMeanSquared) * 1e-6
        else: return 0
    else:
        meanY = np.mean(locVec)*1e-6
        delta = get_rms(momVec,ptclObj.Weight)/get_mean(momVec,ptclObj.Weight)
        dispersionTerm = (meanY/delta)**2*( get_rms(ptclObj.E, ptclObj.Weight) /  get_mean(ptclObj.E, ptclObj.Weight) )**2
        return gammaBeta * np.sqrt(ySquaredMean * pyOverPxSquaredMean - yPyOverPxMeanSquared - dispersionTerm) * 1e-6
    

def get_mean(vector, weight):
    N = np.sum(weight)            
    if N == 0:
        return 0
    return (1./np.sum(weight))*np.sum(weight*vector)
    
        
def get_rms(vector, weight):
    N = np.sum(weight)     
    a = (1./N)*np.sum(weight*vector**2)
    b = ((1./N)*np.sum(weight*vector))**2
       
    if N == 0 or a < b:
        return 0
    return np.sqrt( a - b )





def make_particles_cuts(ptcl):
    """Performs all requested quantity cuts  
    
    Parameters
    ----------
        
    ptcl: Particles object
        Object that this operation is applied to
    """
    if ptcl.cutList is None:
        return
    for cut in ptcl.cutList:
        cutQuantVec = get_particles_vector_from_string(ptcl, cut[0])
        if isinstance(cutQuantVec, int):
            print ("       (!) Warning: Cannot apply cut on Particles " + ptcl.name + " with quantity " + cut[0] + " and interval [" + str(cut[1]) + ", "+ str(cut[2]) + "], ignored")
            return
        lower = cut[1]
        upper = cut[2]
        ptcl.X   = ptcl.X [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.Y   = ptcl.Y [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.Z   = ptcl.Z [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.PX  = ptcl.PX[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.PY  = ptcl.PY[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.PZ  = ptcl.PZ[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.E   = ptcl.E [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.EX  = ptcl.EX[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.EY  = ptcl.EY[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.EZ  = ptcl.EZ[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.Etrans  = ptcl.Etrans[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.YP = ptcl.YP [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.ZP = ptcl.ZP [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.T  = ptcl.T  [(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.Tag = ptcl.Tag[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
        ptcl.Weight = ptcl.Weight[(cutQuantVec >= lower) & (cutQuantVec <= upper)]
    



def get_particles_plane(particles, plotter):
    plane = particles.plane
        
    if plane == "xy":
        return particles.X, particles.Y
    if plane == "yx":
        return particles.Y, particles.X
    if plane == "xz":
        return particles.X, particles.Z
    if plane == "zx":
        return particles.Z, particles.X
    if plane == "yz":
        return particles.Y, particles.Z
    if plane == "zy":
        return particles.Z, particles.Y
    




def get_particles_vector_from_string(obj, inString):
    """Returns quantity vector for given object corresponding to input string  
    
    Parameters
    ----------
        
    obj: Particles object
        Object that this operation is applied to
        
    inString: string
        Name of the requested quantity. Can be X, Y, Z, PX, PY, PZ, YP, ZP, T, Tag, Weight, E, Ex, Ey, Ez, Etrans [lower case works as well]
        
    Returns
    -------
    1D array containing requested quantity     
    
    """

    if inString.lower() == "x":
        return obj.X
    elif inString.lower() == "y":
        return obj.Y
    elif inString.lower() == "z":
        return obj.Z
    elif inString.lower() == "px":
        return obj.PX
    elif inString.lower() == "py":
        return obj.PY
    elif inString.lower() == "pz":
        return obj.PZ
    elif inString.lower() == "t":
        return obj.T
    elif inString.lower() == "yp":
        return obj.YP
    elif inString.lower() == "zp":
        return obj.ZP
    elif inString.lower() == "e" or inString.lower() == "energy":
        return obj.E
    elif inString.lower() == "tag":
        return obj.Tag
    elif inString.lower() == "weight":
        return obj.Weight
    elif inString.lower() == "ex" :
        return obj.EX
    elif inString.lower() == "ey" :
        return obj.EY
    elif inString.lower() == "ez" :
        return obj.EZ
    elif inString.lower() == "etrans" :
        return obj.Etrans
    else:
        return 0
    



def get_phaseSpace_vectors(particles, direction):

    if direction == "x":
        return particles.X, particles.E
    
    elif direction == "t":
        return particles.T, particles.E

    elif direction == "y":
        return particles.Y, particles.YP

    elif direction == "z":
        return particles.Z, particles.ZP


    
