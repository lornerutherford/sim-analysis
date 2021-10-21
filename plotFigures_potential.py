# -*- coding: utf-8 -*-
"""

@author: Paul Scherkl
"""


import numpy as np
import sys
sys.path.append("//home//pinguin//Documents//GitLab//picviz2//")
from main import picVIZ
 

##################################################################################################################
#                  define general analysis parameters
pathToData     = "//home//pinguin//Documents//GitLab//picviz2//example_data//"

#dumpnumbers = np.arange(56, 56 + 1)
dumpnumbers = [100]
picViz = picVIZ(pathToData, dumpnumbers, isHeadless=0)



##################################################################################################################
#                  Define Particles and Field objects


Efieldraw = "EFieldAcc"

# add electric field and electric field lineout
accField_1  = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_1.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="black", invert_axis= 0, tick_min=-15, tick_max=15, export = 0)

# add central differences (i.e. "derivative") of electric field lineout (from front to back of the box)
accField_2 = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_2.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="orange", invert_axis= 0, export = 0, calculus = "differentiate")

# add cumulative sum (i.e. "rolling total") of electric field lineout (from front to back of the box)
accField_3 = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_3.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="green", invert_axis= 0, export = 0, calculus = "cumsum")

# add cummulative trapezoidal aread (i.e. "integral") of electric field lineout (from front to back of the box)
accField_4 = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_4.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="blue", invert_axis= 0, export = 0, calculus = "integrate")

# normalise integral of electric field lineout (i.e. generate trapping potential)
accField_5 = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_5.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="navy", invert_axis= 0, export = 0, calculus = "integrate", normalize = -1./511.7066619)

# zero-gauge trapping potential (e.g. set the maximum value to zero, such that -1 equals traoping)
accField_6 = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_6.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="purple", invert_axis= 0, export = 0, calculus = "integrate", normalize = -1./511.7066619, gauge = "max")



# generate plots
plot_field              = picViz.add_2D_plot(fields = [accField_1],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_derivative         = picViz.add_2D_plot(fields = [accField_2],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_sum                = picViz.add_2D_plot(fields = [accField_3],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_integral           = picViz.add_2D_plot(fields = [accField_4],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_potential          = picViz.add_2D_plot(fields = [accField_5],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_potential_gauged   = picViz.add_2D_plot(fields = [accField_6],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)

# generate multiplot
plotall = picViz.add_multi_plot(plot_list = [plot_field, plot_derivative, plot_sum, plot_integral, plot_potential, plot_potential_gauged], grid = [2,2,2], fig_height=18)






# "dirty" calculation of trapping potential via cumulative sum:
# (using "cumsum to calculate the potential does not require scipy, but is less accurate than "integrate", particularly at low resolution)

accField_alt  = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)

norm_DX     = 3.973196854370783e-06         # cell size in x (DX)
norm_GeV    = 1.e9          # translate GV --> V
norm_emass  = 511706.6619   # electron mass in eV
# calculate normalisation factor for trapping potential (just a showcase of dependencies, of course can be done more elegantly)
norm = norm_DX * norm_GeV / norm_emass
# add the potential lineout
accField_alt.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="red", invert_axis= 0, export = 0, calculus = "cumsum", normalize = -1.*norm, gauge = "max")

plot_dirty_potential    = picViz.add_2D_plot(fields = [accField_alt], particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)




# accuracy comparison:
    
accField_integrate = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_integrate.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="purple", invert_axis= 0, tick_min=-1, tick_max=1, export = 0, calculus = "integrate", normalize = -1./511.7066619, gauge = None)
accField_integrate.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="black",  invert_axis= 0, export = 0)

accField_cumsum = picViz.add_field(Efieldraw, component = 1, colormap="ch_blue", plot_data=1, export =0)
accField_cumsum.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="red", invert_axis= 0, export = 0, tick_min=-1, tick_max=1, calculus = "cumsum", normalize = -1.*norm, gauge = None)
accField_cumsum.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], color ="black",  invert_axis= 0, export = 0)

plot_potential_integrate   = picViz.add_2D_plot(fields = [accField_integrate], particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)
plot_potential_cumsum      = picViz.add_2D_plot(fields = [accField_cumsum],    particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)

potential_compare = picViz.add_multi_plot(plot_list = [plot_potential_integrate, plot_potential_cumsum], grid = [1,1], fig_height=12)

##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
