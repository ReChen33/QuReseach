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
fitR=False

frf=None
if doFit:
    frf=open(f'{ctime}_fit.out','a+', buffering=1)
cleanup=True

# Load data to fit
#

length=1.232
s2p = 'data/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'

#length=1.196
#s2p = 'data/ucryomangan4ft2_shieldconn_open_s11_0.0dBm/ucryomangan4ft2_shieldconn_open_s11_0.0dBm_20230728_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
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
LTC.create_netlist('sparam_shieldedbalancedlumpedline256_shieldCRL_shieldgroundedatsource.asc')
netlist = SpiceEditor('sparam_shieldedbalancedlumpedline256_shieldCRL_shieldgroundedatsource.net')

def compute_s11(Rperlen,Lperlen,Cperlen,Rsperlen,Lsperlen,Csperlen):
    global LTC
    global netlist
    global runner
    global counter
    global ctime

    netlist.set_parameters(Rperlen=Rperlen)
    netlist.set_parameters(Lperlen=Lperlen)
    netlist.set_parameters(Cperlen=Cperlen)

    netlist.set_parameters(Rsperlen=Rsperlen)
    netlist.set_parameters(Lsperlen=Lsperlen)
    netlist.set_parameters(Csperlen=Csperlen)

    raw, log = LTC.run_now(netlist, run_filename=f'{ctime}_sparam_shieldedbalancedlumpedline256_shieldCRL_shieldgroundedatsource_{counter}.net')
    counter+=1
    LTC.wait_completion()
    print(raw)
    rr=RawRead(raw)
    s11=20.*np.log10(np.abs(rr.get_trace('S11(v1)')))
    f=rr.get_trace('frequency')
    return np.array(f,dtype=float),s11

def minfunnoR(param, Rperlen, Rsperlen, fitdB=False, fmin=10e3, fmax=50e6):
    global length
    global fdata
    global s11data
    global ctime
    global frf # =fit result file

    Lperlen_nH,Cperlen_pF,Lsperlen_nH,Csperlen_pF=param
    
    Lperlen=Lperlen_nH*1.e-9
    Lsperlen=Lsperlen_nH*1.e-9
    
    Cperlen=Cperlen_pF*1.e-12
    Csperlen=Csperlen_pF*1.e-12

    if any(map(lambda p: p<=0,param)):
        return 1e9
    else:
        print(f'Rperlen={Rperlen}')
        print(f'Lperlen={Lperlen}')
        print(f'Cperlen={Cperlen}')
        print(f'Rsperlen={Rsperlen}')
        print(f'Lsperlen={Lsperlen}')
        print(f'Csperlen={Csperlen}')
 
        print(f'({Rperlen},{Lperlen*1.e9},{Cperlen*1.e12},{Rsperlen},{Lsperlen*1.e9},{Csperlen*1.e12})')
    
    fsim,s11sim=compute_s11(Rperlen=Rperlen,Lperlen=Lperlen,Cperlen=Cperlen,Rsperlen=Rsperlen,Lsperlen=Lsperlen,Csperlen=Csperlen)
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

    frf.write(f'{counter}\t{Rperlen}\t{Lperlen_nH}\t{Cperlen_pF}\t{Rsperlen}\t{Lsperlen_nH}\t{Csperlen_pF}\t{chi2}\n')
    frf.flush()
        
    return chi2 #/len(dsid[0])
    

def minfun(param, fitdB=False, fmin=10e3, fmax=50e6):
    Rperlen_Ohm,Lperlen_nH,Cperlen_pF,Rsperlen_Ohm,Lsperlen_nH,Csperlen_pF=param
    return minfunnoR((Lperlen_nH,Cperlen_pF,Lsperlen_nH,Csperlen_pF),fitdB=fitdB,fmin=fmin,fmax=fmax,Rperlen=Rperlen_Ohm,Rsperlen=Rsperlen_Ohm)

fmin_hz=10e3
fmax_hz=100e6
#fmin_hz=80e6
#fmax_hz=120e6

# (Rperlen_Ohm,Lperlen_nH,Cperlen_pF,Rsperlen_Ohm,Lsperlen_nH,Csperlen_pF)
x0=(72.2,710.869,28.966,5.93,0.1,53.546)
#x0=(72.2,355.4,14.25,5.93,49.6,72.8)

if doFit:
    res = None
    x1=None
    if fitR:
        res = optimize.minimize(lambda p : minfun(p,fmin=fmin_hz,fmax=fmax_hz, fitdB=False),x0)
        x1=res['x']
    else:
        res = optimize.minimize(lambda p : minfunnoR(p,x0[0],x0[3],fmin=fmin_hz,fmax=fmax_hz, fitdB=False),(x0[1],x0[2],x0[4],x0[5]))
        x1=np.array([x0[0],res['x'][0],res['x'][1],x0[3],res['x'][2],res['x'][3]])
# clean up

    
    ffit,s11fit=compute_s11(Rperlen=x1[0],
                            Lperlen=x1[1]*1.e-9,
                            Cperlen=x1[2]*1.e-12,
                            Rsperlen=x1[3],
                            Lsperlen=x1[4]*1.e-9,
                            Csperlen=x1[5]*1.e-12)
    
    plt.semilogx(ffit,s11fit,label='Fit')

if frf is not None:
    frf.close()

fguess,s11guess=compute_s11(Rperlen=x0[0],
                            Lperlen=x0[1]*1.e-9,
                            Cperlen=x0[2]*1.e-12,
                            Rsperlen=x0[3],
                            Lsperlen=x0[4]*1.e-9,
                            Csperlen=x0[5]*1.e-12)

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
