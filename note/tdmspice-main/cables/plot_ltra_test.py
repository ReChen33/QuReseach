import ltspice
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

plt.ion()

#
# Data
#
datafiles=[f'data/first_long_coax_attempt_20230607/20230607_longrg58cu_GLSD0{ii}.CSV' for ii in [2,3,4,5,6]]
mint=None
for datafile in datafiles:
    datadf=pd.read_csv(datafile, index_col=False)
    datadf=datadf.dropna(axis=1,how='all')
    
    t_ns=1.e9*datadf['in s'].values
    v4=datadf['C4 in V'].values
    v4=v4-np.mean(v4[:200]) # not sure why this is needed
    plt.plot(t_ns,v4,label=f'{datafile} - CH4',alpha=0.5)
    if mint is None:
        mint=np.min(t_ns)

# align sim to first dataset

#
# Simulation
#    
filepath = 'ltra_test.raw'
l = ltspice.Ltspice(filepath)
l.parse() # Data loading sequence. It may take few minutes for huge file.

for i in range(l.case_count):
    time = l.get_time(i)    
    vtdr = l.get_data('V(vtdr)',i)
    plt.plot(mint+time*1.e9,2.*vtdr)

plt.show()
