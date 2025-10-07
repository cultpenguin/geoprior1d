import numpy as np
import random

def prior_lith_reals(info, z, flag_vector):
    # Number of units
    N = info['Sections']['N_sections']

    # Initialize lithology vector
    types = info['Sections']['types'][N-1]
    probs = info['Sections']['probabilities'][N-1]
    choice = random.choices(types, weights=probs, k=1)[0]
    m = np.full_like(z, choice, dtype=float)

    # Initialize layer vector
    layer_count = 1
    layer_index = np.full_like(z, layer_count, dtype=int)
    layer_count += 1
    if N == 1:
        return m, layer_index, flag_vector

    #Random vector for frequency of layers
    r = np.random.rand(N-1)

    # Preallocate vectors
    thick_sections = np.zeros(N)
    N_layers = np.zeros(N-1, dtype=int)
    types_layers = [None] * (N-1)
    thick_layers = [None] * (N-1)

    # Draw random values
    for i in range(N-1):
        if r[i] <= info['Sections']['frequency'][i]:
            # Thickness of unit
            thick_sections[i] = np.random.rand() * (
                info['Sections']['max_thick'][i] - info['Sections']['min_thick'][i]
            ) + info['Sections']['min_thick'][i]

            # Number of layers
            N_layers[i] = np.random.randint(
                info['Sections']['min_layers'][i],
                info['Sections']['max_layers'][i] + 1)

            # Types of layers
            if info['Sections']['repeat'][i] == 1 or N_layers[i] < 2:
                types_layers[i] = random.choices(
                    info['Sections']['types'][i],
                    weights=info['Sections']['probabilities'][i],
                    k=N_layers[i])
            else:
                vec = [random.choices(
                    info['Sections']['types'][i],
                    weights=info['Sections']['probabilities'][i],
                    k=1)[0]]
                for j in range(1, N_layers[i]):
                    available_types = [t for t in info['Sections']['types'][i] if t != vec[j-1]]
                    available_probs = [p for t, p in zip(info['Sections']['types'][i], info['Sections']['probabilities'][i]) if t != vec[j-1]]
                    vec.append(random.choices(available_types, weights=available_probs, k=1)[0])
                types_layers[i] = vec

            # Thicknesses of layers
            t_layers = []
            for t in types_layers[i]:
                idx = t - 1
                t_layers.append(
                    np.random.rand() * (info['Classes']['max_thick'][idx] - info['Classes']['min_thick'][idx])
                    + info['Classes']['min_thick'][idx])
            thick_layers[i] = np.array(t_layers)

        else:
            thick_sections[i] = 0
            N_layers[i] = 0
            types_layers[i] = []
            thick_layers[i] = np.array([])

    # Normalize thicknesses
    if N > 1:
        for i in np.where(thick_sections != 0)[0]:
            thick_layers[i] = thick_layers[i] / (np.sum(thick_layers[i]) / thick_sections[i])

    # Check constraints
    tries = 1
    checksum_layers = 0
    for i in np.where(thick_sections != 0)[0]:
        idxs = [t-1 for t in types_layers[i]]
        layers_max_check = np.sum(thick_layers[i] >= 1.05 * np.array([info['Classes']['max_thick'][j] for j in idxs]))
        layers_min_check = np.sum(thick_layers[i] <= (1/1.05) * np.array([info['Classes']['min_thick'][j] for j in idxs]))
        checksum_layers += layers_max_check + layers_min_check

    checksum_sections = 0
    for i in range(1, N):
        if np.sum(thick_sections[:i]) < info['Sections']['min_depth'][i]:
            checksum_sections = 1
            break

    # Redraw loop
    while checksum_layers > 0 or checksum_sections > 0:
        for i in range(N-1):
            if r[i] <= info['Sections']['frequency'][i]:
                if tries > 100:
                    N_layers[i] = np.random.randint(
                        info['Sections']['min_layers'][i],
                        info['Sections']['max_layers'][i] + 1)
                thick_sections[i] = np.random.rand() * (
                    info['Sections']['max_thick'][i] - info['Sections']['min_thick'][i]
                ) + info['Sections']['min_thick'][i]

                if info['Sections']['repeat'][i] == 1 or N_layers[i] < 2:
                    types_layers[i] = random.choices(
                        info['Sections']['types'][i],
                        weights=info['Sections']['probabilities'][i],
                        k=N_layers[i])
                else:
                    vec = [random.choices(
                        info['Sections']['types'][i],
                        weights=info['Sections']['probabilities'][i],
                        k=1)[0]]
                    for j in range(1, N_layers[i]):
                        available_types = [t for t in info['Sections']['types'][i] if t != vec[j-1]]
                        available_probs = [p for t, p in zip(info['Sections']['types'][i], info['Sections']['probabilities'][i]) if t != vec[j-1]]
                        vec.append(random.choices(available_types, weights=available_probs, k=1)[0])
                    types_layers[i] = vec

                t_layers = []
                for t in types_layers[i]:
                    idx = t - 1
                    t_layers.append(
                        np.random.rand() * (info['Classes']['max_thick'][idx] - info['Classes']['min_thick'][idx])
                        + info['Classes']['min_thick'][idx])
                thick_layers[i] = np.array(t_layers)

            else:
                thick_sections[i] = 0
                N_layers[i] = 0
                types_layers[i] = []
                thick_layers[i] = np.array([])

        if N > 1:
            for i in np.where(thick_sections != 0)[0]:
                thick_layers[i] = thick_layers[i] / (np.sum(thick_layers[i]) / thick_sections[i])

        checksum_layers = 0
        for i in np.where(thick_sections != 0)[0]:
            idxs = [t-1 for t in types_layers[i]]  # ✅ fix
            layers_max_check = np.sum(thick_layers[i] >= 1.05 * np.array([info['Classes']['max_thick'][j] for j in idxs]))
            layers_min_check = np.sum(thick_layers[i] <= (1/1.05) * np.array([info['Classes']['min_thick'][j] for j in idxs]))
            checksum_layers += layers_max_check + layers_min_check

        checksum_sections = 0
        for i in range(1, N):
            if np.sum(thick_sections[:i]) < info['Sections']['min_depth'][i]:
                checksum_sections = 1
                break

        tries += 1
        if tries > 1000:
            flag_vector[0] = 1
            break

    flag_vector[2] = flag_vector[2] + tries

    # Combine
    Ts_all = np.concatenate([arr for arr in thick_layers if arr.size > 0])
    types_all = np.concatenate([np.array(t) for t in types_layers if len(t) > 0])

    # Depths
    Ds = np.cumsum(Ts_all)

    # Fill results
    for i in range(len(types_all)-1, -1, -1):
        m[z <= Ds[i]] = types_all[i]
        layer_index[z < Ds[i]] = layer_count
        layer_count += 1

    return m, layer_index, flag_vector
