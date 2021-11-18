#!/usr/bin/env python3
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

#add electric field and electric field lineout
accField  = picViz.add_field(EField, component = 0, colormap="ch_blue", plot_data=1, export =0, z_order = None)

accField.addLine(component= 0, axis="x", x_range=[0,1000], y_range=[-0.2,0.2], z_range =[-0.2,0.2], operation = "mean", tick_min = -10., tick_max = 10., invert_axis = 0, show_axis = 1, color = "red", plot_data = 1)

    
# add a copy of the electric field above, manually switching the field type to kind = "dummy_potential", and do not plot the field, only the lineout.
# this creates a dummy field object that is not plotted, but internally defined in picViz as a new kind of field.
# this will tell picViz to set the labels of the lineout correctly, and also to use a dedicated axis for the trapping potential
trapping_potential = picViz.add_field(EField, kind = "dummy_potential", plot_data = 0)
trapping_potential.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], show_range = 0, \
                        operation = "mean", tick_min = None, tick_max = None, invert_axis = 0, show_axis = 1, color = "purple", force_color = 1, \
                        z_order = None, export = 0, plot_data = 1, \
                        # the calculation of the trapping potential happens here (integrate, normalise, gauge):
                        calculus = "integrate", normalize = -1./511.7066619, gauge = "max", \
                        # add shaded area to show trapping region (here set to -0.5 for demonstration, for an actual trapping potential with gauge = "max" it would be -1.)
                        fill = ["below", -0.5])    



EField.addLine(component= 0, axis="x",  x_range = [0.,vars.LX*1.e6], y_range = [-y_cut,y_cut], z_range = [-z_cut,z_cut], color ="orange", tick_min = -100.0, tick_max = 100.0)

# Generate plots
plotptcls       = picViz.add_2D_plot(particles=[Ebeam,plasmaElectrons], plane='xy') # Plot particles and fields.
plot_field   = picViz.add_2D_plot(fields = [accField, trapping_potential],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
# Define analyzer
analyzeptcls    = picViz.add_particles_analyzer(particles=[Ebeam], quantityList=["q"]) # Analyze the beam.

##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
