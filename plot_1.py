import glob

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------

def sort_key(fname):
    parts = fname.split('_')
    n_max = int(parts[-1].split('.')[0])
    return n_max

# -----------------------------------------------------------------------------

y_1 = []
y_2 = []

# -----------------------------------------------------------------------------

files = sorted(glob.glob('out/out_1_*.txt'), key=lambda x: sort_key(x))

x_plot = []
y_plot = []

for fname in files:
    n_max = sort_key(fname)

    elapsed = None

    f = open(fname, 'r', encoding='utf-16')
    for line in f:
        if line.startswith('elapsed'):
            elapsed = float(line.split()[1])
    f.close()

    if 2**12 <= n_max <= 2**28:
        x_plot.append(n_max)
        y_plot.append(elapsed)

    if 2**12 <= n_max <= 2**24:
        y_1.append(elapsed)

    print(fname, n_max, elapsed)

plt.plot(x_plot, y_plot, 'sk', label='CPU',
         linewidth=0.5, linestyle=(0, (5, 5)),
         markersize=5)

# -----------------------------------------------------------------------------

files = sorted(glob.glob('out_gpu/out_1_*.txt'), key=lambda x: sort_key(x))

x_plot = []
y_plot = []

for fname in files:
    n_max = sort_key(fname)

    elapsed = None

    f = open(fname, 'r', encoding='utf-16')
    for line in f:
        if line.startswith('elapsed'):
            elapsed = float(line.split()[1])
    f.close()

    if 2**12 <= n_max <= 2**24:
        x_plot.append(n_max)
        y_plot.append(elapsed)

    if 2**12 <= n_max <= 2**24:
        y_2.append(elapsed)

    print(fname, n_max, elapsed)

plt.plot(x_plot, y_plot, '^k', label='GPU',
         linewidth=0.5, linestyle=(0, (5, 5)),
         markersize=6)

# -----------------------------------------------------------------------------

plt.xscale('log', base=2)
plt.yscale('log', base=10)

plt.xlabel('$k$ (for top-$k$ truncation)')
plt.ylabel('simulation time (seconds)')

plt.xticks(2 ** np.linspace(12, 28, 9))

plt.legend()

plt.grid()
plt.show()

# -----------------------------------------------------------------------------

y_1 = np.array(y_1)
y_2 = np.array(y_2)
print(y_1 / y_2)