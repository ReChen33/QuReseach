import numpy as np
import sys
import glob
import os
import skrf as rf
import matplotlib.pylab as plt
import ltspice

plt.ion()

# low res, only down to 10 Mhz
#s2p = 'data/ucryomanganintwpshieldfloating4ft_0.0dBm_20230620/ucryomanganintwpshieldfloating4ft_0.0dBm_20230620_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
# higher res, 100k pts between 9 kHz and 1 GHz

s2p = 'data/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'
#s2p = 'data/ucryomanganintwpshieldfloatinglong_s11attempt3_0.0dBm/ucryomanganintwpshieldfloatinglong_s11attempt3_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p'

ntwk = rf.Network(s2p)

f = ntwk.f
s11 = ntwk.s_db[:, 0, 0]

fig, (ax1, ax2) = plt.subplots(2, figsize=(12,8))

ax1.semilogx(f,s11,label='Measurement')
ax2.semilogx(f,ntwk.s_deg_unwrap[:,0, 0],label='Measurement')
#ax1.semilogx(f,s21)

# overplot lumped element model with compact skin effect
# must be open and have been run
rawfile='sparam_ltra_s11.raw'
l = ltspice.Ltspice(rawfile)
l.parse()

sim_freq=l.frequency
sim_s11=20.*np.log10(l.get_data('S11(v1)'))
sim_phase_deg=np.unwrap(np.angle(l.get_data('S11(v1)'),deg=True))

ax1.semilogx(sim_freq,sim_s11,label='Model')
ax2.semilogx(sim_freq,sim_phase_deg,label='Model')

ax2.legend(loc='lower left',fontsize=18)

ax1.set_xlim(1e6,1e8)
ax2.set_xlim(1e6,1e8)

plt.show(block=False)
