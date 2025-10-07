import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib import cm
from distribution_stats import distribution_stats  # assumes this exists

def prior_summary(filename, mix=False):
    np.random.seed(1)

    # Load data
    with h5py.File(filename, 'r') as f:
        z_vec = f['/M1'].attrs['x']
        cmap = f['/M2'].attrs['cmap']
        types = f['/M2'].attrs['class_name']
        ns = f['/M1'][:].T
        ms = f['/M2'][:].T

    n_types = len(types)
    Nr, Nm = ms.shape

    # Compute distributions
    counts, mode, E, layer_counts, thickness_counts, edges = distribution_stats(ms, filename)

    # Start figure
    fig = plt.figure(figsize=(16, 8))
    fig.suptitle('Summary', fontsize=16)
    grid = plt.GridSpec(2, 7, wspace=0.4, hspace=0.3)

    # Mode plot
    ax1 = fig.add_subplot(grid[0, 0])
    im1 = ax1.imshow(mode[:, np.newaxis], aspect='auto', origin='lower',
                     extent=[0.5, 1.5, z_vec[0], z_vec[-1]],
                     cmap=cm.get_cmap('jet', n_types))  # fallback cmap
    ax1.set_title('Mode')
    ax1.set_xticks([])
    ax1.set_ylabel('Depth [m]')
    ax1.set_ylim(z_vec[0], z_vec[-1])

    # 100 realizations
    ax2 = fig.add_subplot(grid[0, 1:7])
    ms_sample = ms[np.random.permutation(Nr)[:100], :] if mix else ms[:min(Nr, 100), :]
    im2 = ax2.imshow(ms_sample.T, aspect='auto', origin='lower',
                     extent=[0.5, 100.5, z_vec[0], z_vec[-1]],
                     cmap=cm.get_cmap('jet', n_types))
    ax2.set_title(f'Realizations, N = {Nr}')
    ax2.set_xlabel('Real #')
    ax2.set_yticks([])
    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label('Class')
    cbar2.set_ticks(np.arange(1, n_types + 1))
    cbar2.set_ticklabels([t.decode('utf-8') if isinstance(t, bytes) else t for t in types])

    # Marginal distribution
    ax3 = fig.add_subplot(grid[1, 1:3])
    dist = counts / Nr
    im3 = ax3.imshow(dist, aspect='auto', origin='lower',
                     extent=[0.5, n_types + 0.5, z_vec[0], z_vec[-1]])
    ax3.set_title('Marginal distribution')
    ax3.set_ylabel('Depth [m]')
    ax3.set_xticks(np.arange(1, n_types + 1))
    ax3.set_xticklabels([t.decode('utf-8') if isinstance(t, bytes) else t for t in types],
                        rotation=90, fontsize=10)
    plt.colorbar(im3, ax=ax3)

    # Entropy
    ax4 = fig.add_subplot(grid[1, 3])
    ax4.plot(E, z_vec, '-b')
    ax4.set_title('Entropy')
    ax4.set_xlabel('Entropy')
    ax4.set_ylabel('Depth [m]')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(z_vec[0], z_vec[-1])
    ax4.invert_yaxis()

    # Number of layers
    ax5 = fig.add_subplot(grid[1, 4:6])
    ax5.hist(np.arange(len(layer_counts)) + 0.5, bins=edges, weights=layer_counts)
    ax5.set_title('Number of layers')
    ax5.set_xlabel('Number of layers')
    ax5.set_ylabel('Realizations')

    # Layer thickness
    ax6 = fig.add_subplot(grid[1, 6])
    im6 = ax6.imshow(thickness_counts, aspect='auto', origin='lower',
                     extent=[0.5, n_types + 0.5, z_vec[0], z_vec[-1]],
                     cmap='bone_r')
    ax6.set_title('Layer thicknesses')
    ax6.set_xticks(np.arange(1, n_types + 1))
    ax6.set_xticklabels([t.decode('utf-8') if isinstance(t, bytes) else t for t in types],
                        rotation=90, fontsize=10)
    ax6.set_ylabel('Thickness [m]')
    plt.colorbar(im6, ax=ax6)

    plt.show()

    return dist
