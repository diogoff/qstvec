import glob

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------

def sort_key(fname):
    parts = fname.split('_')
    n_max = int(parts[-1].split('.')[0])
    return n_max

# -----------------------------------------------------------------------------

files = sorted(glob.glob('out/out_1_*.txt'), key=lambda x: sort_key(x))

styles = {2**8: 'dotted',
          2**18: 'dashed',
          2**28: 'solid'}

labels = {2**8: '$k=2^{8}$',
          2**18: '$k=2^{18}$',
          2**28: '$k=2^{28}$'}

last = None

for fname in files:
    n_max = sort_key(fname)

    if n_max not in styles:
        continue

    x_plot = []
    y_plot = []

    f = open(fname, 'r', encoding='utf-16')
    for line in f:
        if '%' in line:
            x = int(line.split('/')[0])
        if 'terms' in line:
            y = int(line.split()[0].replace(',', ''))
            if (last == None) or (y >= last):
                x_plot.append(x)
                y_plot.append(y)

    f.close()

    plt.plot(x_plot, y_plot, 'k', label=labels[n_max],
             linestyle=styles[n_max])

    last = n_max

# -----------------------------------------------------------------------------

plt.yscale('log', base=2)

plt.xlabel('circuit instructions')
plt.ylabel('number of terms')

plt.xticks(np.linspace(0, 600, 13))
plt.yticks(2 ** np.linspace(2, 28, 14))

plt.xlim(0, 600)
plt.ylim(2**2, 2**30)

plt.legend(reverse=True)

plt.grid()
plt.show()