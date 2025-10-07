import numpy as np
import time
from tqdm import tqdm
from .prior_lith_reals import prior_lith_reals
from .prior_water_reals import prior_water_reals
from .prior_res_reals import prior_res_reals

def get_prior_sample(info, z_vec, Nreals):
    """
    Generate prior samples of lithology, resistivity, and water level.

    Args:
        info (dict): Prior information dictionary.
        z_vec (array-like): Depths to layer bottoms.
        Nreals (int): Number of realizations to generate.

    Returns:
        ms (ndarray): Lithology samples (Nreals x Nz).
        ns (ndarray): Resistivity samples (Nreals x Nz).
        os (ndarray): Water level samples (Nreals,).
        flag_vector (list): Flags indicating issues during generation.
    """

    Nz = len(z_vec)
    ms = np.zeros((Nreals, Nz))  # Lithology samples
    ns = np.zeros((Nreals, Nz))  # Resistivity samples
    os = np.zeros(Nreals)        # Water level samples
    flag_vector = [0, 0, 0]      # Simulation status flags

    # Even probabilities if not specified
    for i in range(len(info['Sections']['probabilities'])):
        if info['Sections']['probabilities'][i][0] == 1:
              n_types = len(info['Sections']['types'][i])
              info['Sections']['probabilities'][i] = np.ones(n_types) / n_types
              
    start_time = time.time()

    for i in tqdm(range(Nreals), desc="Generating priors", unit="real"):

        # Assign lithologies
        m, layer_index, flag_vector = prior_lith_reals(info, z_vec, flag_vector)
        ms[i, :] = m

        # Assign water level
        if 'Water Level' in info:
            o = prior_water_reals(info)
        else:
            o = 0
        os[i] = o

        # Assign resistivities
        n = prior_res_reals(info, m, o, layer_index, z_vec)
        ns[i, :] = n

    elapsed = time.time() - start_time
    print(f"Prior generation completed in {round(elapsed)} seconds.")

    # Final warnings if applicable
    if flag_vector[0] == 1:
        print("⚠️  Warning: Something went wrong. Models may not reflect your input assumptions.")
    if flag_vector[1] == 1:
        print("⚠️  Warning: Number of layers may not be uniformly distributed.")
    flag_vector[2] = flag_vector[2] / Nreals

    return ms, ns, os, flag_vector
