import os
import fileinput
import sys
import subprocess

R=sys.argv[1]
C=sys.argv[2]
L=sys.argv[3]
length=sys.argv[4]

ascname='tdr_4ftucryomanginintwp_floatingshield_fcngen33250a'
os.system('rm -v tmp.raw')
os.system(f'cp {ascname}.asc tmp.asc')

for line in fileinput.input("tmp.asc", inplace=True, encoding='utf-16-le'):
    if 'LTRA1' in line:
        x=line.split(' ')
        y=[]
        for xx in x:
            if xx.startswith('R='):
                xx=f'R={R}'
            elif xx.startswith('C='):
                xx=f'C={C}p'
            elif xx.startswith('L='):
                xx=f'L={L}n'
            elif xx.startswith('len='):
                xx=f'len={length}' 
            else:
                xx=xx
            y.append(xx)
        print(' '.join(y))
    else:
        print(line, end='')

proc1=subprocess.Popen(['/Applications/LTspice.app/Contents/MacOS/LTspice','-Run','/Users/shawn/Documents/GitHub/tdmspice/cables/tmp.asc'])

###
import ltspice
import time
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
plt.ion()

time.sleep(5)
ascpath = '/Users/shawn/Documents/GitHub/tdmspice/cables/tmp.raw'
l = ltspice.Ltspice(ascpath)
l.parse() # Data loading sequence. It may take few minutes for huge file.

plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.viridis(np.linspace(0,1,l.case_count)))

times=[]
vtdrs=[]
for i in range(l.case_count):
    time = l.get_time(i)    
    vtdr = l.get_data('V(vtdr)',i)
    times.append(time)
    vtdrs.append(vtdr)
#    plt.plot(time*1.e9,2.0*vtdr,'r--') # 2x here because fcn gen outputs 2x the programmed signal in 50 Ohm mode

#plt.xlabel('Time (ns)')
#plt.ylabel('Voltage (V)')

#plt.show()

# Close LTspice
proc1.kill()

# Compute chi2 against data.  Assumes steps in model correspond to datasets in this order:
#
# Data
#
datafiles=['data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD030.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD031.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD032.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD033.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD034.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD035.CSV',
           'data/ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613/GLSD036.CSV']

# LTSpice trans data starts at zero, so pull the start time from the first dataset and use to offset the model data.
# assumes datasets were all taken with the same time offset.
datalabels=['Open',"Shorted","50 Ohm","75 Ohm","125 Ohm","100 Ohm","250 Ohm"]
mint,maxt=None,None

# Pick a nice color map
#plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.viridis(np.linspace(0,1,len(datafiles))))

of = open("results.out", "a+")

# Load datasets, and plot.  Also extract time offset for model.
idx=0
# In reverse order?
times=times[::-1]
vtdrs=vtdrs[::-1]
# why
times=[times[0], times[6], times[5], times[4], times[3], times[2], times[1]]
vtdrs=[vtdrs[0], vtdrs[6], vtdrs[5], vtdrs[4], vtdrs[3], vtdrs[2], vtdrs[1]]
chisq=0
for datalabel,datafile in zip(datalabels,datafiles):
    plt.figure()
    datadf=pd.read_csv(datafile, index_col=False)
    datadf=datadf.dropna(axis=1,how='all')
    
    t_ns=1.e9*datadf['in s'].values
    v4=datadf['C4 in V'].values
    v4=v4-np.mean(v4[:200]) # shifts starting voltage to zero to simplify plots

    plt.plot((t_ns-t_ns[0]),v4,'b')
    plt.plot(1.e9*times[idx],2.*vtdrs[idx],label=f'idx={idx}')
    res=v4-np.interp((t_ns-t_ns[0]),1.e9*times[idx],2.*vtdrs[idx])

    plt.xlim(np.min(t_ns-t_ns[0]), np.max(t_ns-t_ns[0]))
    
    ## plot residual
    #plt.plot((t_ns-t_ns[0]),res,'r--')
    chisq+=np.sum(res*res)
    idx+=1

plt.legend(loc='lower right')

of.write(f'{R}\t{C}\t{L}\t{length}\t{chisq}\n')
of.close()

