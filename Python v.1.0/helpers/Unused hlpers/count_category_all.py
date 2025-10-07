import numpy as np

def count_category_all(obs, types=None):
    """
    Count occurrences of categorical values across columns.

    Parameters:
    obs : 2D array-like
        Observation matrix with categories as integers (rows: depths, columns: observations).
    types : 1D array-like, optional
        List of category values to count. Defaults to all unique values in `obs`.

    Returns:
    mode : np.ndarray
        Most frequent category at each row (depth).
    max_count : np.ndarray
        Count of the most frequent category at each row.
    N_obs : int
        Number of observations per row.
    counts : np.ndarray
        Count matrix of shape (n_depths, n_types).
    """
    obs = np.asarray(obs)
    if types is None:
        types = np.arange(1, np.max(obs) + 1)
    else:
        types = np.asarray(types)

    n_types = len(types)
    N_depths, N_obs = obs.shape

    counts = np.zeros((N_depths, n_types), dtype=int)

    for i in range(N_depths):
        for j, t in enumerate(types):
            counts[i, j] = np.sum(obs[i, :] == t)

    max_count = np.max(counts, axis=1)
    mode_idx = np.argmax(counts, axis=1)
    mode = types[mode_idx]

    return mode, max_count, N_obs, counts
