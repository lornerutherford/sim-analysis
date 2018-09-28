# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""


import numpy as np
import sys
#sys.path.append('E://Paul//Personal Folders//Science//CodeArea//picViz2//')
#sys.path.append('D://Strathcloud//Personal Folders//Science//CodeArea//picViz2//')
from main import picVIZ
 



##################################################################################################################
#                  define general analysis parameters
#pathToData = "D://Strathcloud//Personal Folders//Science//Data//paperICS//lightSource07//"
pathToData = "E://Paul//Personal Folders//Science//Data//paperICS//2018_aac//aac_dechirp//"
#pathToData     = "D:\\Strathcloud\\\Personal Folders\\Science\\Data\\paperICS\\2018_aac\\higherResDechirp\\"
#pathToData     = "D:\\Strathcloud\\\Personal Folders\\Science\\Data\\paperICS\\2018_aac\\aac_dechirp\\"

dumpnumbers = np.arange(70, 72 + 1)
picViz = picVIZ(pathToData, dumpnumbers, isHeadless=0)



##################################################################################################################
#                  Define Particles and Field objects


beam = picViz.add_particles("BeamElectrons", show_ratio=0.001, opacity = 0.1, color = "black")
beam.cut("y", -10, 10)

#beam.addLine(quantity = "emity", color = "blue", bin_size=10)
#beam.addLine(quantity = "emitz", color = "red", bin_size=10)
#beam.addLine(quantity = "i", color = "blue", bin_size=10, tick_max=10.0e3)
#beam.addLine(quantity = "b5", color = "green", bin_size=10, tick_max=2.0e18)

test = picViz.add_particles("LiPlusElec", show_ratio=1, opacity = 0.5, color = "black")
#test.cut("x", 80, 80.5)

a = picViz.add_particles_analyzer(particles=[test], quantityList=["i", "ipeak", "q", "widthx", "b5", "b6"], use_existing_file =0, file_name="test", bin_size=0.05)


test.addLine(quantity = "i", color = "blue", bin_size=0.05)
#beam.addLine(quantity = "twissb", color = "green", bin_size=10)
#beam.addLine(quantity = "twissg", color = "red", bin_size=10)


#HIT = picViz.add_particles("HITElectrons", show_ratio=0.1, opacity = 0.3, color = "red")
#HIT.color_code("E", colormap="magma", show_colorbar=1)
#HIT.cut("y", -10, 10)

#lPPC = picViz.add_particles("LOWPPCElectrons", show_ratio=0.1, opacity = 0.3, color = "red")
#lPPC.color_code("E", colormap="magma", show_colorbar=1)
#lPPC.cut("e", 5.0e-6, 10)


#ionField  = picViz.add_field("EFieldIon", component = -1, colormap="ch_blue_r", plane="xz", show_colorbar=1, clip_max= 50)
#ionField.addLine(component=-1, x_range=[250], z_range= [-100, 100], y_range = 0, axis="z",  color = "red", invert_axis= 0, tick_max= 250)


#accField  = picViz.add_field("rhoBeam", component = -1, colormap="ch_blue_r", plane="xz", show_colorbar=1, clip_max= 50, plot_data=1, kind = "electric")
#
#accField.addLine(component= 0 ,axis="x",  x_range=[0, 400], z_range=[-3,3], y_range =[-3,3], color ="red",  invert_axis= 0, tick_min= -30, tick_max=30)
#accField.addLine(component= 1 ,axis="z",  x_range=[250], z_range=[-100, 100], y_range =[-3,3], color ="blue", invert_axis= 0, tick_min= -30, tick_max=30)
#accField.addLine(component= 2 ,axis="z",  x_range=[250], z_range=[-100, 100], y_range =[-3,3], color ="green", invert_axis= 0, tick_min= -99, tick_max=99)




##################################################################################################################
#                  Define plotting objects

#plotPSE = picViz.add_phasespace_plot(particles = [lPPC],fig_size=[5,5],make_fig= 1)
#plotPSY = picViz.add_phasespace_plot(particles = [test],fig_size=[5,5],make_fig= 1, direction="x")
#
plotAcc = picViz.add_2D_plot(fields = [], particles = [test], fig_size=[6,6], plane ="xy", auto_aspect_ratio=1, save_fig=1, make_fig= 1, show_sim_progress="x", plane_offset=0)
#plotIon = picViz.add_2D_plot(fields = [ionField], particles = [beam, HIT, lPPC], fig_size=[6,6], plane ="xz", auto_aspect_ratio=1, save_fig=1, make_fig= 0, show_sim_progress="t")

#multi = picViz.add_multi_plot([plotIon, plotPSE, plotAcc, plotPSY], grid=[2,2], fig_height=10, save_fig =1, make_fig = 1)
#




##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
