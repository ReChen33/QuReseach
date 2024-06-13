import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import numpy as np
from scipy.signal import savgol_filter
import os

plt.ion()

remove_baseline=True
datafile=sys.argv[1]

datadf=pd.read_csv(datafile, index_col=False)
datadf=datadf.dropna(axis=1,how='all')

t_ns=1.e9*datadf['in s'].values
v1=datadf['C1 in V'].values
v4=datadf['C4 in V'].values

if remove_baseline:
    #remove baseline at start
    v1=v1-np.mean(v1[:200])
    v4=v4-np.mean(v4[:200])
    
#plt.plot(t_ns,v1,label=f'{datafile} - CH1')
plt.plot(t_ns,v4,label=f'{datafile} - CH4')
v4_filt=savgol_filter(v4, 31, 3, mode="nearest")
plt.plot(t_ns,v4_filt,'r--')

# save filtered data to pwl file
pwlfn=os.path.join('./pwlfiles/',os.path.basename(datafile).split('.')[:-1][0]+'.pwl')
t_pwl=[f'{t-t_ns[0]:.3f}n' for t in t_ns]
v4_filt_pwl=[f'{v*1000.:.3f}m' for v in v4_filt]
with open(pwlfn, 'w') as writer:
    for t,v in zip(t_pwl,v4_filt_pwl):
        writer.write(f'{t},{v}\n')
        
        #toffset=-31.
        #for tau in [1,2,3,4,5,6]:
        #    plt.plot(t_ns,[0 if t<toffset else 1.0*(1.0-np.exp(-(t-toffset)/tau)) for t in t_ns],'--')
        
plt.legend()
plt.show()
