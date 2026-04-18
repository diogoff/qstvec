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

styles = {0.9: 'dotted',
          0.99: 'dashed',
          0.999: 'solid'}

labels = {0.9: '$p=0.9$',
          0.99: '$p=0.99$',
          0.999: '$p=0.999$'}

for fname in files:
    p_frac = sort_key(fname)

    if p_frac not in styles:
        continue

    x_plot = []
    y_plot = []

    f = open(fname, 'r', encoding='utf-16')
    for line in f:
        if '%' in line:
            x_plot.append(int(line.split('/')[0]))
        if 'terms' in line:
            y_plot.append(int(line.split()[0].replace(',', '')))

    f.close()

    plt.plot(x_plot, y_plot, 'k', label=labels[p_frac],
             linestyle=styles[p_frac])

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