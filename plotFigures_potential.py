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
accField  = picViz.add_field(Efieldraw, component = 0, colormap="ch_blue", plot_data=1, export =0, z_order = None)

accField.addLine(component= 0, axis="x", x_range=[0,1000], y_range=[-0.2,0.2], z_range =[-0.2,0.2], operation = "mean", tick_min = -10., tick_max = 10., invert_axis = 0, show_axis = 1, color = "red", plot_data = 1)

    
# add a copy of the electric field above, manually switching the field type to kind = "dummy_potential", and do not plot the field, only the lineout.
# this creates a dummy field object that is not plotted, but internally defined in picViz as a new kind of field.
# this will tell picViz to set the labels of the lineout correctly, and also to use a dedicated axis for the trapping potential
trapping_potential = picViz.add_field(Efieldraw, kind = "dummy_potential", plot_data = 0)
trapping_potential.addLine(component= 0, axis="x", x_range=[0,1000], z_range=[-0.2,0.2], y_range =[-0.2,0.2], show_range = 0, \
                        operation = "mean", tick_min = None, tick_max = None, invert_axis = 0, show_axis = 1, color = "purple", force_color = 1, \
                        z_order = None, export = 0, plot_data = 1, \
                        # the calculation of the trapping potential happens here (integrate, normalise, gauge):
                        calculus = "integrate", normalize = -1./511.7066619, gauge = "max")    


# plot both field objets
plot_field   = picViz.add_2D_plot(fields = [accField, trapping_potential],   particles = [], fig_size=[6,6], plane ="xz",  save_fig=1, make_fig =1, show_sim_progress="x", dpi = 300)

##################################################################################################################
#                  start code

picViz.execute(print_progress = 1, print_gridData = 1, print_metaData = 1)

#del picViz
