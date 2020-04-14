# -*- coding: utf-8 -*-
"""
Created on Tue May 01 20:28:47 2018

@author: Paul Scherkl
"""


def show_sim_progress(axis, plotter, gridData, kind):
    import numpy as np
    quant = "t_{\mathrm{sim}}"  if kind == "t" else "x_{\mathrm{sim}}"
    unit  = "ps" if kind == "t" else "mm"
    number ='{0:.2f}'.format(np.round(gridData["runTime"]*1e12, 2))  if kind == "t" else '{0:.2f}'.format(np.round(gridData["runTime"]*3e8*1e3, 2))
    axis.text(0, axis.xaxis.label.get_position()[1], "$" + quant + "\ = \ " + str(number) + "\ \mathrm{"+unit+"}$", transform = axis.transAxes, size = plotter.labelSize, verticalalignment='top')


def format_plotter_axes(ax, plotter):

    from plotter import PlotterPhaseSpace
    import numpy as np
    xpower = ypower = 1
    if isinstance(plotter, PlotterPhaseSpace):
        if plotter.x_lim:
            xticks, xtickLabels, xpower = get_axis_ticks(plotter.x_lim[0], plotter.x_lim[1])            
            ax.set_xlim(plotter.x_lim)
            ax.set_xticks(np.linspace(plotter.x_lim[0], plotter.x_lim[1], 6))
            if plotter.direction == "x" or plotter.direction == "t":
                ax.set_xticklabels( np.round(np.linspace(plotter.x_lim[0], plotter.x_lim[1], 6 ), 1) ) 
            else:
                ax.set_xticklabels( xtickLabels )
        if plotter.y_lim:
            yticks, ytickLabels, ypower = get_axis_ticks(plotter.y_lim[0], plotter.y_lim[1])            
            ax.set_ylim(plotter.y_lim)
            ax.set_yticks(np.linspace(plotter.y_lim[0], plotter.y_lim[1], 6))
            ax.set_yticklabels( ytickLabels )
        if not plotter.x_lim and not plotter.y_lim: 
            ax.set_xlim(-1,1 )
            ax.set_ylim(-1,1 )
            ax.set_xticks([])
            ax.set_yticks([])
            
    else:
        if not plotter.x_lim: 
            ax.set_xlim(-1,1 )
            ax.set_xticks([])
           
        else:
            ax.set_xlim(plotter.x_lim)
            ax.set_xticks(np.linspace(plotter.x_lim[0], plotter.x_lim[1], 6))
        if not plotter.y_lim: 
            ax.set_ylim(-1,1 )
            ax.set_yticks([])
           
        else:
            ax.set_ylim(plotter.y_lim)
            ax.set_yticks(np.linspace(plotter.y_lim[0], plotter.y_lim[1], 6))
        

        
    labelX, labelY = get_figure_labels(plotter, xpower, ypower)
    
    ax.set_xlabel(labelX, fontsize = plotter.labelSize)
    ax.set_ylabel(labelY, fontsize = plotter.labelSize)

    [ticklabel.set_fontsize(plotter.tickSize) for ticklabel in ax.get_xticklabels()]
    [ticklabel.set_fontsize(plotter.tickSize) for ticklabel in ax.get_yticklabels()]
        

    trans = ax.transAxes.transform([(0,0), (1,1)])
    x = ax.get_figure().get_dpi() / (trans[1,1] - trans[0,1])/72
    y = ax.get_figure().get_dpi() / (trans[1,0] - trans[0,0])/72
    
    ax.xaxis.set_label_coords(0.5, -1.0*plotter.labelSpacingX*x)
    ax.yaxis.set_label_coords( -plotter.labelSpacingY*y, 0.5)
    


def get_label_from_key(key):
    
    if key.split(",")[0].find("fld") > -1:  # label dedicated to Field-related keys

        quantity = key.split(",")[3] 
        comp     = key.split(",")[4]

        if quantity =="electric":
            quantity = "$\mathit{E}$"
        elif quantity == "magnetic":
            quantity = "$\mathit{B}$"
        elif quantity == "current":
            quantity = "$\mathit{J}$"
        elif quantity == "chargedens":
            return "$\mathit{\\rho}$"
        
        if comp == "0":
            comp = "$_{\mathrm{x}}$"
        elif comp == "1":
            comp = "$_{\mathrm{y}}$"
        elif comp == "2":
            comp = "$_{\mathrm{z}}$"
        elif comp == "-1":
            comp = "$_{\mathrm{sum}}$"
        elif comp == "-2":
            comp = "$_{\mathrm{sum, trans}}$"
        return quantity + comp
    
    elif key.split(",")[0].find("ptcl") > -1:  # label dedicated to Particles-related keys
        quantity = key.split(",")[3]
        if quantity == "e":
            return "$\overline{E}_{\mathrm{kin}}$"
        
        elif quantity == "etrans":
            return "$\overline{E}_{\mathrm{kin, trans}}$"
        
        elif quantity == "emax":
            return "$E_{\mathrm{kin, max}}$"
        
        elif quantity == "etotal":
            return "$E_{\mathrm{kin, total}}$"

        elif quantity == "edev":
            return "$\sigma E_{\mathrm{kin}}$"

        elif quantity == "espread":
            return "$\sigma E_{\mathrm{kin}} / E_{\mathrm{kin}}$"
        
        elif quantity == "ex":
            return "$\overline{E}_{{\mathrm{kin, x}}$"
            
        elif quantity == "ey":
            return "$\overline{E}_{\mathrm{kin, y}}$"
        
        elif quantity == "ez":
            return "$\overline{E}_{\mathrm{kin, z}}$"
        
        
        elif quantity == "widthx":
            return "$\sigma \ x$"

        elif quantity == "widthxmax":
            return "$\sigma x_{\mathrm{max}}$"

        elif quantity == "widthy":
            return "$\sigma y$"
        
        elif quantity == "widthymax":
            return "$\sigma y_{\mathrm{max}}$"
        
        elif quantity == "widthz":
            return "$\sigma z$"
        
        elif quantity == "widthzmax":
            return "$\sigma z_{\mathrm{max}}$"
       
        
        elif quantity == "x":
            return "$\mathrm{\\xi}$"
        
        elif  quantity == "posx":
            return "$\overline{\\xi}$"
            
        elif quantity == "posxlab":
            return "$\overline{\\x}_{lab}$"
        
        elif  quantity == "posy":
            return "$\overline{y}$"
        
        elif  quantity == "posz":
            return "$\overline{z}$"
        
        elif quantity == "y" or quantity == "z":
            return "$\mathrm{"+quantity+"}$"
        
        elif quantity == "q":
            return "$\mathrm{Q}$"
        
        elif quantity == "i":
            return "$\mathrm{I}$"
        

        elif quantity == "divy":
            return "$\sigma y'$"
        
        elif quantity == "divz":
            return "$\sigma z'$"


        elif quantity == "emity":
            return "$\epsilon_{\mathrm{n,y}}$"
        
        elif quantity == "emitydisp":
            return "$\epsilon_{\mathrm{n,y, disp}}$"

        elif quantity == "emitz":
            return "$\epsilon_{\mathrm{n,z}}$"
        
        elif quantity == "emitzdisp":
            return "$\epsilon_{\mathrm{n,z, disp}}$"

        
        elif quantity == "b5":
            return "$B_{\mathrm{5D} }$"
        
        elif quantity.find("b6") > -1:
            return "$B_{\mathrm{6D}}$"

    return "$"+ quantity.capitalize()+"$"

        

def get_unit_from_component(key):
    if key.find("ptcl") > -1:
        quantity = key.split(",")[3]
        
        
        if quantity == "e" or quantity == "emax" or quantity == "edev":
            return "MeV"
        
        elif quantity == "x" or quantity == "y" or quantity == "z" or quantity.find("width")>-1  or quantity.find("pos")>-1: 
            return "$\mathrm{\mu m}$"
        
        elif quantity == "px" or quantity =="py" or quantity =="pz":
            return "($\\beta$c)$^{-1}$"

        elif quantity == "q":
            return "pC"
        
        elif quantity == "t":
            return "fs"
        
        elif quantity.find("i") == 0:
            return "A"

        elif quantity.find("div")>-1:
            return "mrad"
        
        elif quantity.find("emit")>-1:
            return "m rad"

        elif quantity == "etotal":
            return "J"
        
        elif quantity == "espread":
            return "%"
        
        elif quantity == "gamma":
            return ""
        
        elif quantity == "b5" :
            return "$\mathrm{A\ m^{-2} \ rad^{-2}}$"
        
        elif quantity.find("b6")>-1:
            divisor = quantity.lower().split("b6")[1]
            divisor = "01 \%\ \mathrm{BW}" if divisor == "01" else "001 \%\ \mathrm{BW}" if divisor == "001" else "1 \%\ \mathrm{BW}" if divisor == "1" or divisor == "" else "1"
            return "$\mathrm{A\ (m^{2} \ rad^{2}}\ " + divisor + ")^{-1}\ $"
        
        
        elif quantity == "twissb":
            return "m"


        else:
            return ""
        #TODO: add twiss parameters here
            
        # TODO: add all beam properties that can be calculated

    elif key.find("electric") > -1:
        return "GV m$^{-1}$"
    
    elif key.find("magnetic") > -1:
        return "T"
    
    elif key.find("current") > -1:
        return "A"
    
    elif key.find("chargedens") > -1:
        return "m$^{-3}$"
    else:
        return ""



def get_figure_labels(plotter, powerX, powerY):
    from plotter import Plotter2D, PlotterPhaseSpace, PlotterHist
    
    
    if isinstance(plotter, PlotterHist):
        xQuant = plotter.quantx
        xUnit = get_unit_from_component("ptcl,0,xz,"+plotter.quantx+",-1")
        yQuant = "Q"
        yUnit  = "pC"
        xLabel = "$" + xQuant + "\ \mathrm{("+xUnit+")}$" if powerX == 1 else "$" + xQuant + "\ \mathrm{(\\times10 ^ {" +str(powerX) + "}\ " + xUnit + ")}$"
        yLabel = "$" + yQuant + "\ \mathrm{("+yUnit+")}$" if powerY == 1 else "$" + yQuant + "\ \mathrm{(\\times10 ^ {" +str(powerY) + "}\ " + yUnit + ")}$"
        return xLabel, yLabel
        

    if isinstance(plotter, PlotterPhaseSpace):

        if plotter.direction == "x":
            xQuant = "\\xi"
            xUnit  = "\mu m"
            yQuant = "E"
            yUnit  = "MeV"
            return "$" + xQuant + "\ \mathrm{("+xUnit+")}$" , "$" + yQuant + "\ \mathrm{("+yUnit+")}$" if powerY == 1 else "$" + yQuant + "\ \mathrm{(\\times10 ^ {" +str(powerY) + "}\ " + yUnit + ")}$"

        if plotter.direction == "t":
            xQuant = "\t"
            xUnit  = "fs"
            yQuant = "E"
            yUnit  = "MeV"
        
        if plotter.direction == "y":
            xQuant = "y"
            xUnit  = "\mu m"
            yQuant = "yp"
            yUnit  = "mrad"
        
        if plotter.direction == "z":
            xQuant = "z"
            xUnit  = "\mu m"
            yQuant = "zp"
            yUnit  = "mrad"
            
        
        xLabel = "$" + xQuant + "\ \mathrm{("+xUnit+")}$" if powerX == 1 else "$" + xQuant + "\ \mathrm{(\\times10 ^ {" +str(powerX) + "}\ " + xUnit + ")}$"
        yLabel = "$" + yQuant + "\ \mathrm{("+yUnit+")}$" if powerY == 1 else "$" + yQuant + "\ \mathrm{(\\times10 ^ {" +str(powerY) + "}\ " + yUnit + ")}$"
        return xLabel, yLabel
        
    
    if isinstance(plotter, Plotter2D):
        if plotter.plane is not None:
            if plotter.plane[0] == "x":
                return "$\\xi\ \mathrm{(\mu m)}$", "$" + plotter.plane[1] + "\ \mathrm{(\mu m)}$"
            if plotter.plane[1] == "x":
                return "$" + plotter.plane[0] + "\ \mathrm{(\mu m)}$", "$\\xi\ \mathrm{(\mu m)}$"
            else:
                return "$" + plotter.plane[0] + "\ \mathrm{(\mu m)}$", "$" + plotter.plane[1] + "\ \mathrm{(\mu m)}$"
        else:
            if plotter.fields:
                if plotter.fields[0].plane[0] == "x":
                    return "$\\xi\ \mathrm{(\mu m)}$", "$" + plotter.fields[0].plane[1] + "\ \mathrm{(\mu m)}$"
                if plotter.fields[0].plane[1] == "x":
                    return "$" + plotter.fields[0].plane[0] + "\ \mathrm{(\mu m)}$", "$\\xi\ \mathrm{(\mu m)}$"
                else:
                    return "$" + plotter.fields[0].plane[0] + "\ \mathrm{(\mu m)}$", "$" + plotter.fields[0].plane[1] + "\ \mathrm{(\mu m)}$"
            else:
                if plotter.particles[0].plane[0] == "x":
                    return "$\\xi\ \mathrm{(\mu m)}$", "$" + plotter.particles[0].plane[1] + "\ \mathrm{(\mu m)}$"
                if plotter.particles[0].plane[1] == "x":
                    return "$" + plotter.particles[0].plane[0] + "\ \mathrm{(\mu m)}$", "$\\xi\ \mathrm{(\mu m)}$"
                else:
                    return "$" + plotter.particles[0].plane[0] + "\ \mathrm{(\mu m)}$", "$" + plotter.particles[0].plane[1] + "\ \mathrm{(\mu m)}$"
                




def set_axis_label(axis, key, power, labelSize, color = "black", kind = "y"):
    if power == 1:
        if kind == "y":
            axis.set_ylabel(get_label_from_key(key) + " (" + str(get_unit_from_component(key) ) + ")", size = labelSize, color = color)
        else:
            axis.set_xlabel(get_label_from_key(key) + " (" + str(get_unit_from_component(key) ) + ")", size = labelSize, color = color)

    else:
        if kind == "y":
            axis.set_ylabel(get_label_from_key(key) + " ($\\times10 ^ {" + str(power) + "}$ " + \
                                          str(get_unit_from_component(key) )+  ")", size = labelSize , color = color)
        else:
            axis.set_xlabel(get_label_from_key(key) + " ($\\times10 ^ {" + str(power) + "}$ " + \
                                          str(get_unit_from_component(key) )+  ")", size = labelSize , color = color)
            
            
            
def get_axis_ticks(minVal, maxVal):
    import numpy as np
    power = 1
    if minVal is not None and not np.isnan(minVal) :
        maxAbs = float(np.max( [np.abs(minVal), np.abs(maxVal)] ))
        if maxAbs >= 100:
            if str(maxAbs).find("e+") > -1:
                power = int(str(maxAbs)[str(maxAbs).find("e+")+2::])
            else:
                power = str(maxAbs).find(".") - 1
                
            minVal = minVal/10.**power
            maxVal = maxVal/10.**power
            minVal = np.round(minVal, 2)
            maxVal = np.round(maxVal, 2)
            
        elif maxAbs < 0.01:
            if str(maxAbs).find("e-") > -1:
                power = -1*int(str(maxAbs)[str(maxAbs).find("e-")+2::])
            else:
                power = 1
                for i in range(len( str(maxAbs).split(".")[1] ) ) :
                    if str(maxAbs).split(".")[1][i] is not "0":
                        power = -1*(i + 1)
                        break
                
            minVal = minVal/10.**power
            maxVal = maxVal/10.**power
            minVal = np.round(minVal, 2)
            maxVal = np.round(maxVal, 2)
            
            # TODO: if min/max values differences are too small, only one tick remains (e.g due to rounding).. implement strategy to prevent that                
        
        ticks = np.linspace(minVal, maxVal, 6)
        ticks = np.round(ticks, 2)     
        
    else:
        ticks      = [0]
        
    tickLabels = [label for label in ['{0:.2f}'.format(item) for item in ticks]]
    return ticks, tickLabels, power       




