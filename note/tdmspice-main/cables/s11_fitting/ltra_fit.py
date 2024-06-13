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

counter=0
doFit=True
cleanup=True

# Load data to fit
#
length=1.232
#s2p = 'data/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
s2p = 'data/ucryomangan4ft_noshield_open_s11_0.0dBm/ucryomangan4ft_noshield_open_s11_0.0dBm_20230728_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
#
#length=3.639
#s2p = 'data/ucryomanganlongtwpshieldfloating_s11attempt1_0.0dBm/ucryomanganlongtwpshieldfloating_s11attempt1_0.0dBm_20230720_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
#s2p = 'data/ucryomanganlongwire2shield_s11attempt1_0.0dBm/ucryomanganlongwire2shield_s11attempt1_0.0dBm_20230720_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
#s2p = 'data/cafinewirecutwplong_s11attempt1_0.0dBm/cafinewirecutwplong_s11attempt1_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
#
ntwk = rf.Network(s2p)
fdata = ntwk.f
s11data = ntwk.s_db[:, 0, 0]
##

LTC = SimRunner(output_folder='./temp')
LTC.create_netlist('sparam_ltra_s11.asc')
netlist = SpiceEditor('sparam_ltra_s11.net')

def ltra_s11(Rperlen=72.9,Lperlen=711e-9,Cperlen=58e-12,length=1.232):
    global LTC
    global netlist
    global runner
    global counter
    global ctime
    netlist.set_parameters(Rperlen=Rperlen)
    netlist.set_parameters(Lperlen=Lperlen)
    netlist.set_parameters(Cperlen=Cperlen)
    netlist.set_parameters(length=length)

    raw, log = LTC.run_now(netlist, run_filename=f'{ctime}_sparam_ltra_s11_{counter}.net')
    counter+=1
    LTC.wait_completion()

    rr=RawRead(raw)
    s11=20.*np.log10(np.abs(rr.get_trace('S11(v1)')))
    f=rr.get_trace('frequency')
    return np.array(f,dtype=float),s11

def minfun(param, fitdB=False, fmin=10e3, fmax=50e6):
    global length

    global fdata
    global s11data
    Rperlen,Lperlen_nH,Cperlen_pF=param

    Lperlen=Lperlen_nH*1.e-9
    Cperlen=Cperlen_pF*1.e-12

    if Lperlen<0 or Cperlen<0:
        return 1e9
    else:
        print(f'Rperlen={Rperlen} Lperlen={Lperlen} Cperlen={Cperlen} length={length}')
    
    fsim,s11sim=ltra_s11(Rperlen=Rperlen,Lperlen=Lperlen,Cperlen=Cperlen,length=length)
    # interpolate sim
    fs11sim = interpolate.interp1d(fsim,s11sim)

    dsid=np.where((fdata>fmin)&(fdata<fmax))
    ssid=np.where((fsim>fmin)&(fsim<fmax))

    if fitdB:
        chi2=np.sum((np.real(s11data[dsid])-np.real(fs11sim(fdata[dsid])))**2)
    else:
        s11datamag=10**(np.real(s11data[dsid])/20.)
        s11simmag=10**(np.real(fs11sim(fdata[dsid]))/20.)
        chi2=np.sum((s11datamag-s11simmag)**2)
        
    return chi2/len(dsid[0])

fmin_hz=25e6
fmax_hz=75e6
#fmin_hz=80e6
#fmax_hz=120e6
x0=(72.2,711,31)

if doFit:
    res = optimize.minimize(lambda p : minfun(p,fmin=fmin_hz,fmax=fmax_hz, fitdB=False),x0)
# clean up

    ffit,s11fit=ltra_s11(Rperlen=res['x'][0],Lperlen=res['x'][1]*1.e-9,Cperlen=res['x'][2]*1.e-12,length=length)
    plt.semilogx(ffit,s11fit,label='Fit')
    
fguess,s11guess=ltra_s11(Rperlen=x0[0],Lperlen=x0[1]*1.e-9,Cperlen=x0[2]*1.e-12,length=length)

plt.semilogx(fguess,s11guess,'r--',label='Guess')

plt.semilogx(fdata,s11data,label='Measurement')
plt.xlim(fmin_hz,fmax_hz)

plt.xlabel('Frequency (Hz)',fontsize=18)
plt.ylabel('S11 (dB)',fontsize=18)

plt.legend(loc='lower left',fontsize=18)
plt.show(block=False)
plt.tight_layout()

if cleanup:
    import shutil
    shutil.rmtree('temp')
