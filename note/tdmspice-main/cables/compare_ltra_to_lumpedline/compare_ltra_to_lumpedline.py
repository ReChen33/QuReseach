from PyLTSpice import SimRunner, SpiceEditor, RawRead

import matplotlib.pylab as plt
plt.ion()

import pandas as pd
import numpy as np
import time
import skrf as rf
import os

from scipy import interpolate, optimize

ctime=int(time.time())

cleanup=True
ascs=['sparam_ltra.asc','sparam_lumpedline256.asc','sparam_balancedlumpedline256.asc']
##

Rperlen=72.2
Lperlen=711e-9
Cperlen=58e-12
length=1.232

resdict={}
for asc in ascs:

    ascprefix=asc.split('.')[:-1][0]
    LTC = SimRunner(output_folder='./temp')
    LTC.create_netlist(f'{ascprefix}.asc')
    netlist = SpiceEditor(f'{ascprefix}.net')

    netlist.set_parameters(Rperlen=Rperlen)
    netlist.set_parameters(Lperlen=Lperlen)
    netlist.set_parameters(Cperlen=Cperlen)
    netlist.set_parameters(length=length)

    rfn=f"{ctime}_{ascprefix}"
    resdict[rfn]={}
    raw, log = LTC.run_now(netlist, run_filename=rfn)
    # for some reason, not returning properly on completion
    # for lumped element simulations
    LTC.wait_completion(timeout=45)

    rr=RawRead(raw)
    s11=20.*np.log10(np.abs(rr.get_trace('S11(v1)')))
    f=rr.get_trace('frequency')

    resdict[rfn]['s11_dB']=s11
    resdict[rfn]['f_Hz']=f

    plt.semilogx(f,s11,label=ascprefix)


#plt.xlim(fmin_hz,fmax_hz)

plt.xlabel('Frequency (Hz)',fontsize=18)
plt.ylabel('S11 (dB)',fontsize=18)

plt.legend(loc='lower left',fontsize=18)
plt.show(block=False)
plt.tight_layout()

if cleanup:
    import shutil
    shutil.rmtree('temp')
