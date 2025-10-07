import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, LogNorm
from .flj_log import flj_log

def res_plot_improved(x, y, ax = None):
    """
    Creates a colored resistivity plot.
    
    Parameters:
    x : array-like
        Resistivity values.
    y : array-like
        Counts, probability, or similar.
    """
    
    created_new_ax = False
    
    # Create logarithmic spacing
    xs = np.logspace(np.log10(0.1), np.log10(2600), 444)
    xs_center = np.sqrt(xs[:-1] * xs[1:])
    
    # Interpolate y values to match xs_center
    ys = np.interp(xs_center, x, y, left=0, right=0)

    # Create patches for coloring
    patches = []
    colors = []

    for i in range(len(xs_center)):
        verts = [
            (xs[i], 0),
            (xs[i], ys[i]),
            (xs[i + 1], ys[i]),
            (xs[i + 1], 0)
        ]
        polygon = Polygon(verts, closed=True)
        patches.append(polygon)
        colors.append(xs_center[i])

    if ax is None:
        fig, ax = plt.subplots()
        created_new_ax = True
    else:
        fig = ax.figure
        
    cmap_res = ListedColormap(flj_log())
    norm_res = LogNorm(vmin=0.1, vmax=2600)
    p = PatchCollection(patches, array=np.array(colors), edgecolor='none', cmap=cmap_res, norm=norm_res)
    ax.add_collection(p)

    # Plot the original curve
    ax.plot(x, y, '-k')

    # Log scaling and plot settings
    ax.set_xscale('log')
    ax.set_yscale('linear')
    ax.set_xlim([0.1, 2600])
    ax.set_ylim(bottom=0)
    ax.set_facecolor('none')
    ax.set_axisbelow(False)
    ax.set_title("Resistivity Plot")

    # Apply colormap and color limits
    p.set_clim([0.1, 2600])
    fig.colorbar(p, ax=ax, label='Resistivity')

    if created_new_ax:
        plt.show()
    
    return ax
