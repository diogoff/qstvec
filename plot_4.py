import glob

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------

def sort_key(fname):
    parts = fname.split('_')
    p_frac = float(parts[-2])
    return p_frac

# -----------------------------------------------------------------------------

files = sorted(glob.glob('out/out_*_0.txt'), key=lambda x: sort_key(x))

x_plot = []
y_plot = []

for fname in files:
    p_frac = sort_key(fname)

    n_max = 0

    f = open(fname, 'r', encoding='utf-16')
    for line in f:
        if 'terms' in line:
            n = int(line.split()[0].replace(',', ''))
            if n > n_max:
                n_max = n

    print(fname, n_max)

    f.close()

    x_plot.append(p_frac)
    y_plot.append(n_max)

# -----------------------------------------------------------------------------

plt.plot(x_plot, y_plot, 'k')

plt.yscale('log', base=2)

plt.xticks(np.linspace(0.9, 1.0, 11))
plt.yticks(2 ** np.linspace(6, 28, 12))

plt.xlabel('$p$ (for $p$-mass truncation)')
plt.ylabel('number of terms')

plt.grid()
plt.show()