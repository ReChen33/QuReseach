import numpy as np
import os
#python3 -i lazy_ltspice_chi2.py 8.8 8 100 100

os.system('rm -v results.out')

R=72.2
for C in np.linspace(30,70,20):
    for L in np.linspace(500,1500,20):
        cmd=f'python3 lazy_ltspice_chi2.py {R:.3f} {C:.3f} {L:.3f} 1.232'
        print(cmd)
        os.system(cmd)
