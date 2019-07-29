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
#pathToData = "E://Paul//Personal Folders//Science//Data//paperICS//lightSource11//"
pathToData     = "D:\\Strathcloud\\\Personal Folders\\Science\\Data\\paperICS\\lightSource11\\"
#pathToData     = "D:\\Strathcloud\\\Personal Folders\\Science\\Data\\paperICS\\2018_aac\\aac_dechirp\\"

dumpnumbers = np.arange(56, 56 + 1)
dumpnumbers = [29]
picViz = picVIZ(pathToData, dumpnumbers, isHeadless=0)



##################################################################################################################
#                  Define Particles and Field objects




beam = picViz.add_particles("BeamElectrons", show_ratio=0.1, opacity = 0.08, color = "black")
beam.cut("y", -5, 5)



HIT = picViz.add_particles("HITElectrons", show_ratio=1. , opacity = 0.3, color = "k", export = 0)
# HIT.addLine(quantity = "i", color = "red", bin_size=0.2, tick_max = 3.0e3)
# HIT.cut("e", 1, 1000)
#HIT.cut("x", 46, 170)
#HIT.cut("y", -10,10)
#HIT.cut("z", -10, 10)
HIT.color_code("E")


#a = picViz.add_particles_analyzer(particles=[HIT], quantityList=["q", "i", "ipeak", "e", "edev", "espread", "emity", "emitz", "widthx" , "widthy" , "widthz", "divy", "divz" ], use_existing_file =0,  bin_size=0.05)



accField  = picViz.add_field("EFieldAcc", component = -1, colormap="ch_blue_r", plot_data=1, clip_min = 10, clip_max = 20, export =0)
#accField.colormap.set_under("white")
accField.addLine(component= 0,axis="x",  x_range=[0, 400], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="red",  invert_axis= 0, tick_min=-150, tick_max=160, export = 0)
#
#
#
#ionizationField  = picViz.add_field("EFieldIon", component = -1, colormap="ch_blue_r",  plot_data=1)
#ionizationField.colormap.set_under("white")
#
#ionizationField.addLine(component=-1 ,axis="z",  x_range=[150], z_range=[-100, 100], y_range =[0], color ="red",  invert_axis= 0, tick_min= 0, tick_max=100, show_range = 1)
#




##################################################################################################################
#                  Define plotting objects




#
#psXPlot         = picViz.add_phasespace_plot(particles = [  HIT], fig_size=[6,6], x_lim = [30, 60], save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
#
#psYPlot         = picViz.add_phasespace_plot(particles = [  HIT], direction = "y", fig_size=[6,6], x_lim = [-10, 10], y_lim = [-8.0, 8.0], save_fig=1, make_fig =0, show_sim_progress="x", dpi = 300)
#
#psZPlot         = picViz.add_phasespace_plot(particles = [  HIT], direction = "z", fig_size=[6,6], x_lim = [-10, 10], y_lim = [-8.0, 8.0], save_fig=1, make_fig =0, show_sim_progress="x", dpi = 300)


#
ionPlot         = picViz.add_2D_plot(fields = [ accField], particles = [ HIT ], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
#ionPlot.fields[1].plot_data = 0
#

#test = picViz.add_hist_plot(particles=[HIT], bin_size=1, log_y = 1, log_x = 0, x_lim = [0, 40])
#
#multi = picViz.add_multi_plot(plot_list = [psXPlot, test], grid = [2])
#multi.plotters[1].particles[0].cut("e", 100, 200)


##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
