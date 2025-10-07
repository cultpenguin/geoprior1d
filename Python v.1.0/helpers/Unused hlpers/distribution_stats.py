import numpy as np
import h5py
from collections import Counter

def distribution_stats(ms, h5_filename):
    """
    Calculate distribution statistics for lithology models.

    Parameters:
    ms : np.ndarray
        Array of shape (Nreals, Nz) with lithology classifications.
    h5_filename : str
        Path to the HDF5 file with attributes.

    Returns:
    counts : np.ndarray
        Count of each lithology per depth.
    mode : np.ndarray
        Most frequent lithology per depth.
    E : np.ndarray
        Entropy per depth.
    layer_counts : np.ndarray
        Histogram of the number of layers across realizations.
    thickness_counts : np.ndarray
        Histogram of layer thicknesses by lithology type.
    edges : np.ndarray
        Edges used for layer count histogram.
    """
    # Load metadata from HDF5
    with h5py.File(h5_filename, 'r') as f:
        types = f['/M2'].attrs['class_name']
        z_vec = f['/M1'].attrs['x']

    z_vec = np.array(z_vec).flatten()
    n_types = len(types)
    Nreals, Nz = ms.shape

    # 1. Counts and mode per depth
    mode, _, _, counts = count_category_all(ms.T, np.arange(1, n_types + 1))

    # 2. Entropy per depth
    E = np.zeros(Nz)
    for i in range(Nz):
        p = counts[i, counts[i, :] != 0] / Nreals
        E[i] = -np.sum(p * np.log(p) / np.log(n_types))

    # 3. Number of layers per realization
    n_layers = np.sum(np.diff(ms, axis=1) != 0, axis=1) + 1
    edges = np.arange(0.5, np.max(n_layers) + 2.5)
    layer_counts, _ = np.histogram(n_layers, bins=edges)

    # 4. Layer thickness histogram per lithology
    thickness_counts = np.zeros((Nz, n_types), dtype=int)

    # Extend ms with a 0 delimiter row
    ms_temp = np.vstack([ms.T, np.zeros(Nreals, dtype=int)])
    ms_array = ms_temp.flatten()

    # Build matching z vector
    dz = z_vec[1] - z_vec[0]
    zs_array = np.tile(np.append(z_vec, z_vec[-1] + dz), Nreals)

    for lith in range(1, n_types + 1):
        counter = 0
        z1 = -1
        for j in range(len(ms_array)):
            if ms_array[j] == lith:
                counter += 1
                if z1 == -1:
                    z1 = zs_array[j]
            elif ms_array[j] != lith and counter > 0:
                z2 = zs_array[j]
                thickness = z2 - z1
                # Find index for thickness if it matches a depth exactly
                idx = np.where(np.isclose(z_vec, thickness))[0]
                if idx.size > 0:
                    thickness_counts[idx[0], lith - 1] += 1
                counter = 0
                z1 = -1

    return counts, mode, E, layer_counts, thickness_counts, edges
