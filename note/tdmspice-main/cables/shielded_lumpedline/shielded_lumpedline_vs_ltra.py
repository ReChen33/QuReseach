from PyLTSpice import SimRunner, SpiceEditor, RawRead

import matplotlib.pylab as plt
plt.ion()

import pandas as pd
import numpy as np
import time
import skrf as rf
import os

from scipy import interpolate, optimize

resdict={}
ctime=int(time.time())
cleanup=True

def runasc(asc,Rperlen,Lperlen,Cperlen,length):
    ascprefix=asc.split('.')[:-1][0]
    LTC = SimRunner(output_folder='./temp')
    LTC.create_netlist(f'{ascprefix}.asc')
    netlist = SpiceEditor(f'{ascprefix}.net')

    netlist.set_parameters(Rperlen=Rperlen)
    netlist.set_parameters(Lperlen=Lperlen)
    netlist.set_parameters(Cperlen=Cperlen)
    netlist.set_parameters(length=length)
    
    rfn=f"{ctime}_{ascprefix}"
    raw, log = LTC.run_now(netlist, run_filename=rfn)
    # for some reason, not returning properly on completion
    # for lumped element simulations
    LTC.wait_completion()

    rr=RawRead(raw)
    s11=20.*np.log10(np.abs(rr.get_trace('S11(v1)')))
    f=rr.get_trace('frequency')

    return f,s11

## LTRA that ~matches data with shield completely floating
fltra,s11ltra=runasc('sparam_ltra.asc',72.2,711e-9,58e-12,1.232)

## Lumped line with just extra shield capacitance
#fll,s11ll=runasc('sparam_shieldedbalancedlumpedline256_shieldcapacitanceonly.asc',72.2,711e-9,30e-12,1.232)
fll,s11ll=runasc('sparam_shieldedbalancedlumpedline256_shieldCRL_shieldgroundedatsource.asc',72.2,711e-9,30e-12,1.232)

plt.semilogx(fltra,s11ltra,label='LTRA')
plt.semilogx(fll,s11ll,label='Lumped Line')

# Label axes and stuff
plt.xlabel('Frequency (Hz)',fontsize=18)
plt.ylabel('S11 (dB)',fontsize=18)

# Limit ranges
plt.xlim(np.min(fltra),100e6)

plt.legend(loc='lower left',fontsize=18)
plt.show(block=False)
plt.tight_layout()

if cleanup:
    import shutil
    shutil.rmtree('temp')
