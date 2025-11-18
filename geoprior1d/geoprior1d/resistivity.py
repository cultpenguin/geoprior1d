import numpy as np

def prior_res_reals(info, m, o, layer_index, z_vec):

    # Initialize n vector
    n = m.copy()
    if o != z_vec[0]:
        n_unsat = n.copy()
    else:
        n_unsat = None

    # Input resistivities for each layer
    for i in range(1, np.max(layer_index) + 1):
        for j in range(1, np.max(info['Classes']['codes']) + 1):
            mask = (m == j) & (layer_index == i)
            if np.any(mask):
                n[mask] = 10 ** (np.log10(info['Resistivity']['res'][j-1])
                    + info['Resistivity']['res_unc'][j-1]
                    * np.random.randn())
                # Unsaturated resistivity above water table
                if o != z_vec[0]:
                    n_unsat[mask] = 10 ** (np.log10(info['Resistivity']['unsat_res'][j-1])
                        + info['Resistivity']['unsat_res_unc'][j-1]
                        * np.random.randn())

    # Apply unsaturated values above water table
    if o != 0:
        n[z_vec < o] = n_unsat[z_vec < o]

        diffs = z_vec - o
        idx = np.where(diffs[:-1] * diffs[1:] < 0)[0]  # find sign change crossing

        # Weighted mean in the interval containing the water table
        if idx.size > 0:
            i = idx[0]
            n[i+1] = (
                n_unsat[i+1] * abs(diffs[i]) + n[i+1] * diffs[i+1]
            ) / (abs(diffs[i]) + diffs[i+1])

    return n
