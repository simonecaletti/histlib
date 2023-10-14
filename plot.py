#### Library with utilities for plotting histograms
#### author: Simone Caletti
####: email: scaletti@phys.ethz.ch
#### last update: October 2023

#### File base on an earlier version written by Gregory Soyez
#### and another one previously written by Gavin Salam.


import utils 
import hist
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec 
import matplotlib.cm as cm 

#######################################################

def init_plot(w=1, h=1, nratio=0):
    fig = plt.figure(figsize=(w, h))
    return fig

def add_axes(fig):
    

    return None

def set_ratioplot(nratioplt):

    nplt = nratioplt + 1
    relative_height = [nplt]
    for i in range(nratioplt):
        relative_height.append(1)

    gs = gridspec.GridSpec(nplt, height_ratios=relative_height)
    gs.update(wspace=0.0, hspace=0.0)
    
    ax = [plt.subplot(gs[0,0])]
    for i in range(nratioplt):
        ax += [plt.subplot(gs[i+1, 0])]

    return None

#########################################################à

def set_y_axis (ax, y_axis, if_show = True):
    yticks_ps    = []
    yticks_lb    = []
    
    y = y_axis[0]
    
    while y <= y_axis[1]:
        
        yticks_ps.append(y)
        
        yticks_lb.append(y)

        y = y + y_axis[2]
    
    yticks = []
    if '.' in str(y_axis[2]):
        dot_index = str(y_axis[2]).index('.')
        my_prc = len( str(y_axis[2])[dot_index::] ) - 1
    else:
        my_prc = 0
    
    for el in yticks_lb:
        string = '$' + "{value:{width}.{precision}f}".format(value=el, width=0, precision=my_prc) + '$'
            
        yticks.append( string  )
    
    ax.set_yticks(yticks_ps)
    ax.set_yticklabels(yticks)

    ax.set_ylim(y_axis[0], y_axis[1])
    
    if if_show == False:
        ax.set_yticklabels([])

##############################################################

def set_x_axis (ax, x_axis, if_show = True):
    xticks_ps    = []
    xticks_lb    = []
    
    x = x_axis[0]
    
    while x <= x_axis[1]:
        xticks_ps.append(x)
        
        xticks_lb.append(x)

        x = x + x_axis[2]
    
    xticks = []
    if '.' in str(x_axis[2]):
        dot_index = str(x_axis[2]).index('.')
        my_prc = len( str(x_axis[2])[dot_index::] ) - 1
    else:
        my_prc = 0

    for el in xticks_lb:
        string = '$' + "{value:{width}.{precision}f}".format(value=el, width=0, precision=my_prc) + '$'
        xticks.append( string  )

    ax.set_xticks(xticks_ps)
    ax.set_xticklabels(xticks)

    ax.set_xlim(x_axis[0], x_axis[1])
    
    if if_show == False:
        ax.set_xticklabels([])

####################################################################

def set_logx_axis (ax, x_min, x_max, if_show = True):
    ax.set_xscale('log')
    
    xticks_ps    = [0.001,       0.01,        0.1,         0.2,    0.4,     0.8,     1]
    xticks_lb    = ['$10^{-3}$', '$10^{-2}$', '$10^{-1}$', '$0.2$','$0.4$', '$0.8$', '$1$'] 
 
    xticks_ps_fn = []
    xticks_lb_fn = []
 
    for i,j  in zip(xticks_ps, xticks_lb):
        if x_min <= i and i <= x_max:
            xticks_ps_fn.append(i)
            xticks_lb_fn.append(j)
        
    ax.set_xticks(xticks_ps_fn)
    ax.set_xticklabels(xticks_lb_fn)

    ax.set_xlim( x_min, x_max )
    
    if if_show == False:
        ax.set_xticklabels([])

###################################################################

def set_logy_axis (ax, pow_min, pow_max, if_show = True):
    ax.set_yscale('log')

    yticks_ps    = []
    yticks_lb    = []

    pow_it = pow_min
    
    while pow_it <= pow_max:
        
        yticks_ps.append( m.pow(10, pow_it) )
        yticks_lb.append( pow_it )
        
        pow_it = pow_it + 1
    
    yticks = []
    for el in yticks_lb:
        string = '$10^{' + str(el) +  '}$'
        yticks.append( string )
    
    ax.set_yticks(yticks_ps)
    ax.set_yticklabels(yticks)

    ax.set_ylim( m.pow(10, pow_min), m.pow(10, pow_max) )
    
    if if_show == False:
        ax.set_yticklabels([])

#####################################################

def remove_overlapping_ticks(axis_list):
    # Remove overlapping ticks
    for ax in axis_list:
        yticks = ax.yaxis.get_major_ticks()
        yticks[-1].set_visible(False)
        yticks[0].set_visible(False)
            
        xticks = ax.xaxis.get_major_ticks()
        xticks[-1].set_visible(False)
        xticks[0].set_visible(False)

    return None


#####################################################


def plot(w=30., h=30., nratioplt=0, show_MC=False, errboxes=False, X=[100, 1000, 100], Y0=[-6, 0], Y1=[0, 1, 0.1], Y2=[0, 1, 0.1], Y3=[0, 1, 0.1], figname="prova", legend=["A", "B", "C"], y_leg2=0.75):
    
    # Adjust width and height with respect to your screen
    f, ax = plt.subplots(1, 1, sharex=True, figsize=(w , h), dpi=100)

    set_ratioplot(nratioplt)

    # Customize axis 
    set_x_axis(ax[0], X, False)         #ax[0]
    set_logy_axis(ax[0], Y0[0], Y0[1])
    #set_x_axis(ax[1], X, False)         #ax[1]
    #set_y_axis(ax[1], Y1)
    #set_x_axis(ax[2], X)                #ax[2]
    #set_y_axis(ax[2], Y2)
    #set_x_axis(ax[3], X)                #ax[3]
    #set_y_axis(ax[3], Y3)

    #Set labels for the y-axis
    ax[0].set_ylabel ('$\mathrm{d}\sigma/\mathrm{d}p_{t\,J}\,\left[\,\mathrm{pb}/\mathrm{GeV}\,\\right]$')
    #ax[3].set_xlabel ('$p_{t\,J}\,\left[\mathrm{GeV}\\right]$')
    #ax[1].set_ylabel ('$\mathrm{RES/MC}$', size=70)
    #ax[2].set_ylabel ('$\mathrm{TAG/NO\,TAG}$', size=70)
    #ax[3].set_ylabel ('$\mathrm{HAD/PS}$', size=70)

    #Set title
    #ax[0].set_title("$\mathrm{%s\,LEVEL,\,NLL'+LO}$"% mode)
    
    #colors
    #colors = ['black', 'blue', 'magenta', 'green', 'darkorange', 'yellow', 'grey', 'red']
    colors = ["black"]
    for c in cm.Dark2(range(len(obs_list)-1)): colors.append(c)
    #colors = cm.Dark2(range(len(obs_list)))
    #colors.insert("black", 0)
    
    #Set legend 1
    #patches = [mpatches.Patch(color='black', label='$\mathrm{No\,Tag}$')]
    #lines1 = [mlines.Line2D([], [], color='black', label='$\mathrm{No\,Tag}$')]
    lines1 = []
    for color, l in zip(colors, legend):
        line = mlines.Line2D([], [], color=color, label=l)
        lines1.append(line)
        #patch = mpatches.Patch(color=color, label=l)
        #patches.append(patch)
    leg1 = ax[0].legend(handles=lines1, loc='upper right')
    
    #Set legend 2
    lines2 = [mlines.Line2D([], [], color='black', alpha=0.3, label="$\mathrm{NLL'}+\mathrm{LO}$")]
    if show_MC: lines2.append(mlines.Line2D([], [], color='black', alpha=0.3, label="$\mathrm{Sherpa\,MC@NLO}$", linestyle='--'))
    leg2 = ax[0].legend(handles=lines2, loc='upper right', bbox_to_anchor=(1, y_leg2))
    
    #Restore legend 1
    ax[0].add_artist(leg1)
    
    #Grids
    ax[0].grid(True, which = 'major')
    #ax[1].grid(True, which = 'major')
    #ax[2].grid(True, which = 'major')
    #ax[3].grid(True, which = 'major')

    #Hide overlapping ticks
    remove_overlapping_ticks(ax)

    plt.tight_layout(rect=[0.01, 0.01, 0.99, 0.99])
    
    #print RES
    for obs, color in zip(obs_list, colors):
        ax[0].hist(RES[mode][obs]["CENTRAL"]["bin_center"], RES[mode][obs]["CENTRAL"]["edges"], weights=RES[mode][obs]["CENTRAL"]["dsigma_dpt"], color=color, histtype='step', linewidth=4)
        if errboxes: print_errboxes(ax[0], color, RES[mode][obs]["CENTRAL"]["errbox"]["dsigma_dpt"])

    #print MC
    if show_MC:
        for obs, color in zip(obs_list, colors):
            ax[0].hist(MC[mode][obs]["CENTRAL"]["bin_center"], MC[mode][obs]["CENTRAL"]["edges"], weights=MC[mode][obs]["CENTRAL"]["dsigma_dpt"], color=color, histtype='step', linewidth=4, linestyle='--')
            if errboxes: print_errboxes(ax[0], color, MC[mode][obs]["CENTRAL"]["errbox"]["dsigma_dpt"])
        
    #print RES/MC ratio HAD=PS
    for obs, color in zip(obs_list, colors):
        ax[1].hist(RES[mode][obs]["CENTRAL"]["bin_center"], RES[mode][obs]["CENTRAL"]["edges"], weights=RES[mode][obs]["CENTRAL"]["res/mc"], color=color, histtype='step', linewidth=4)
        if errboxes: print_errboxes(ax[1], color, RES[mode][obs]["CENTRAL"]["errbox"]["res/mc"])
        
    #print Tag/noTag ratio
    for obs, color in zip(obs_list, colors):
        if show_MC: ax[2].hist(MC[mode][obs]["CENTRAL"]["bin_center"], MC[mode][obs]["CENTRAL"]["edges"], weights=MC[mode][obs]["CENTRAL"]["tag/notag"], color=color, histtype='step', linewidth=4, linestyle='--')
        ax[2].hist(RES[mode][obs]["CENTRAL"]["bin_center"], RES[mode][obs]["CENTRAL"]["edges"], weights=RES[mode][obs]["CENTRAL"]["tag/notag"], color=color, histtype='step', linewidth=4)
        if errboxes:
            if errboxes: print_errboxes(ax[2], color, RES[mode][obs]["CENTRAL"]["errbox"]["tag/notag"])
            if errboxes and show_MC: print_errboxes(ax[2], color, MC[mode][obs]["CENTRAL"]["errbox"]["tag/notag"])
    
    #print HAD/PS ratio RES=MC
    if mode == "HAD":
        for obs, color in zip(obs_list, colors):
            ax[3].hist(MC[mode][obs]["CENTRAL"]["bin_center"], MC[mode][obs]["CENTRAL"]["edges"], weights=MC[mode][obs]["CENTRAL"]["had/ps"], color=color, histtype='step', linewidth=4)
            if errboxes: print_errboxes(ax[3], color, MC[mode][obs]["CENTRAL"]["errbox"]["had/ps"])
            #print(MC[mode][obs]["CENTRAL"]["errbox"]["had/ps"])
    
    if printpdf:
        plt.savefig(savepath + figname + ".pdf")




