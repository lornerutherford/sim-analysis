#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 03:56:58 2021

@author: lornerutherford
"""
import sys
import numpy as np
sys.path.append('//global//cscratch1//sd//lorner96//20211007_HighResChannel//')
from main import picVIZ
import sys

pathToData              = '//global//cscratch1//sd//lorner96//20211007_HighResChannel//'
outputPath 				= pathToData + 'VIZ//'
#dumpNumbers = [90]
dumpNumbers = np.arange(0,100 +1)

picViz = picVIZ(pathToData, dumpNumbers, outPath = outputPath, isHeadless = 1)
sys.path.append(pathToData)
import LorneE310_WIPVars as vars
y_cut = vars.DY*1.e6/2.
z_cut = vars.DZ*1.e6/2.

# define particles, fields, analyzers and plotters here

# Add particles
Ebeam           = picViz.add_particles("BeamElectrons", color="blue") # Add the beam electrons.
plasmaElectrons = picViz.add_particles("LIT_Electrons", color="black")
plasmaElectrons.cut("z", -vars.DZ*1e6, vars.DZ*1e6)
# Add fields
EField          = picViz.add_field("EFieldAcc",component=0, colormap="ch_blue_r") # Add E-field.

# Add lineouts

EField.addLine(component= 0, axis="x",  x_range = [0.,vars.LX*1.e6], y_range = [-y_cut,y_cut], z_range = [-z_cut,z_cut], color ="orange", tick_min = -100.0, tick_max = 100.0)

# Generate plots
plotptcls       = picViz.add_2D_plot(particles=[Ebeam,plasmaElectrons,], fields=[EField], plane='xy') # Plot particles and fields.

# Define analyzer
analyzeptcls    = picViz.add_particles_analyzer(particles=[Ebeam], quantityList=["q"]) # Analyze the beam.

##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
