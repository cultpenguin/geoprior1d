import numpy as np
import h5py
import matplotlib.pyplot as plt
import pandas as pd
from helpers.extract_prior_info import extract_prior_info
from helpers.get_prior_sample import get_prior_sample
from helpers.flj_log import flj_log
from scipy.stats import norm
from datetime import datetime
from matplotlib.colors import ListedColormap, BoundaryNorm, LogNorm
import os


def prior_generator(input_data, Nreals, dmax, dz, doPlot=0):
    # Extract input parameters

    info, cmaps = extract_prior_info(input_data)

    # Create z vector and generate priors
    z_vec = np.arange(dz, dmax + dz, dz)
    ms, ns, ws, flag_vector = get_prior_sample(info, z_vec, Nreals)

    # Construct output filename
    base_name = info.get("filename", input_data)
    
    # Remove Excel extension if present
    base_name, _ = os.path.splitext(base_name)

    # Construct new filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    name = f"{base_name}_N{Nreals}_dmax{dmax}_{timestamp}.h5"

    # Remove existing file
    if os.path.exists(name):
        os.remove(name)

    # Write HDF5 file
    with h5py.File(name, 'w') as f:

        # M1: Resistivity
        dset_M1 = f.create_dataset('M1', data=ns.astype(np.float32))
        dset_M1.attrs['is_discrete'] = 0
        dset_M1.attrs['name'] = 'Resistivity'
        dset_M1.attrs['x'] = np.arange(0, dmax, dz)
        dset_M1.attrs['clim'] = [.1, 2600]
        dset_M1.attrs['cmap'] = flj_log().T

        # M2: Lithology
        dset_M2 = f.create_dataset('M2', data=ms.astype(np.int16))
        dset_M2.attrs['is_discrete'] = 1
        dset_M2.attrs['name'] = 'Lithology'
        dset_M2.attrs['class_name'] = np.array(info['Classes']['names'], dtype='S')
        dset_M2.attrs['class_id'] = info['Classes']['codes']
        dset_M2.attrs['x'] = np.arange(0, dmax, dz)
        dset_M2.attrs['clim'] = [0.5, len(info['Classes']['codes']) + 0.5]
        dset_M2.attrs['cmap'] = cmaps['Classes'].T

        # M3: Water level
        if 'Water Level' in info:
            dset_M3 = f.create_dataset('M3', data=ws.astype(np.float32).reshape(-1, 1))
            dset_M3.attrs['is_discrete'] = 0
            dset_M3.attrs['name'] = 'Waterlevel'
            dset_M3.attrs['x'] = [0]

        # Read Excel sheets into DataFrames
        T_geo1 = pd.read_excel(input_data, sheet_name="Geology1")
        headers_geo1 = T_geo1.columns.astype(str).tolist()
        contents_geo1 = T_geo1.astype(str).values.flatten().tolist()
        
        T_geo2 = pd.read_excel(input_data, sheet_name="Geology2")
        headers_geo2 = T_geo2.columns.astype(str).tolist()
        contents_geo2 = T_geo2.astype(str).values.flatten().tolist()
        
        T_res = pd.read_excel(input_data, sheet_name="Resistivity")
        headers_res = T_res.columns.astype(str).tolist()
        contents_res = T_res.astype(str).values.flatten().tolist()
        
        # Open (or create) HDF5 file and write attributes
        with h5py.File(name, "a") as f:
            f.attrs["Creation date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.attrs["Class headers"] = headers_geo1
            f.attrs["Class table"] = contents_geo1
            f.attrs["Unit headers"] = headers_geo2
            f.attrs["Unit table"] = contents_geo2
            f.attrs["Resistivity headers"] = headers_res
            f.attrs["Resistivity table"] = contents_res
        
    # Plotting
    if doPlot == 1:
        plot_resistivity_distributions(info)
        plot_realizations(z_vec, ms, ns, ws, info, cmaps, Nreals)

    return name, flag_vector


# ========== Helper Plotting Functions ==========

def plot_resistivity_distributions(info):
    plt.figure(figsize=(12, 8))
    plt.suptitle("Resistivity distributions", fontsize=24)
    codes = info['Classes']['codes']
    for i, code in enumerate(codes):
        x = np.linspace(-1, 4, 500)
        y1 = norm.pdf(x, np.log10(info['Resistivity']['res'][i]),
                          info['Resistivity']['res_unc'][i] * np.log10(info['Resistivity']['res'][i]))
        plt.subplot((len(codes) + 2) // 3, 3, i + 1)
        plt.plot(10**x, y1, 'k', label='saturated')
        if 'Water Level' in info:
            y2 = norm.pdf(x, np.log10(info['Resistivity']['unsat_res'][i]),
                              info['Resistivity']['unsat_res_unc'][i] * np.log10(info['Resistivity']['unsat_res'][i]))
            plt.plot(10**x, y2, 'r', label='unsaturated')
        plt.title(info['Classes']['names'][i])
        plt.xscale('log')
        plt.xlabel('Resistivity [Ohm-m]')
        plt.legend()
    plt.tight_layout()
    plt.show()


def plot_realizations(z_vec, ms, ns, os, info, cmaps, Nreals):
    nshow = min(Nreals, 100)

    # Discrete lithology colormap
    cmap_classes = ListedColormap(cmaps['Classes'])
    bounds = np.arange(0.5, len(info['Classes']['codes']) + 1.5, 1) 
    norm_classes = BoundaryNorm(bounds, cmap_classes.N)

    # Resistivity colormap (continuous, log scale)
    cmap_res = ListedColormap(flj_log())
    norm_res = LogNorm(vmin=0.1, vmax=2600)

    plt.figure(figsize=(10, 6))

    # Lithology
    plt.subplot(2, 1, 1)
    plt.imshow(ms[:nshow].T, aspect='auto',
               extent=[0.5, nshow + 0.5, z_vec[-1], z_vec[0]],
               cmap=cmap_classes, norm=norm_classes, interpolation='nearest')
    plt.title("Lithostratigraphy")
    plt.ylabel("Depth [m]")
    cbar = plt.colorbar(ticks=info['Classes']['codes'], label='Lithology Class')
    cbar.ax.set_yticklabels(info['Classes']['names'])

    if 'Water Level' in info:
        for i in range(nshow):
            plt.plot([i+0.5, i + 1.5], [os[i], os[i]], 'k-')

    # Resistivity
    plt.subplot(2, 1, 2)
    plt.imshow(ns[:nshow].T, aspect='auto',
               extent=[0.5, nshow + 0.5, z_vec[-1], z_vec[0]],
               cmap=cmap_res, norm=norm_res, interpolation='nearest')
    plt.title("Resistivity")
    plt.xlabel("Realization #")
    plt.ylabel("Depth [m]")
    plt.colorbar(label='Resistivity [Ohm-m]')

    if 'Water Level' in info:
        for i in range(nshow):
            plt.plot([i+0.5, i + 1.5], [os[i], os[i]], 'k-')

    plt.tight_layout()
    plt.show()
