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
s2p = 'data/ucryomanganintwpshieldfloating4ft_higherres2_0.0dBm/ucryomanganintwpshieldfloating4ft_higherres2_0.0dBm_20230710_0pt000ghz_1pt000ghz_0pt0dbm_10avg.s2p'

ntwk = rf.Network(s2p)

f = ntwk.f
s21 = ntwk.s_db[:, 1, 0]
s11 = ntwk.s_db[:, 0, 0]

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.semilogx(f,s21)
ax2.semilogx(f,s11)

# overplot lumped element model with compact skin effect
# must be open and have been run
rawfile='sparam_lumped_line_skineffect_1.raw'
l = ltspice.Ltspice(rawfile)
l.parse()

ax1.semilogx(l.frequency,20.*np.log10(l.get_data('S21(v1)')))
ax2.semilogx(l.frequency,20.*np.log10(l.get_data('S11(v1)')))

plt.show(block=False)
