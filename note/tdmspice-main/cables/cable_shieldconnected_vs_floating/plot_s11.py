import numpy as np
import sys
import glob
import os
import skrf as rf
import matplotlib.pylab as plt
import ltspice

plt.ion()

s2ps = ['data/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm/ucryomanganintwpshieldfloating4ft_s11attempt1_0.0dBm_20230719_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p',
        'data/ucryomangan4ft2_shieldconn_open_s11_0.0dBm/ucryomangan4ft2_shieldconn_open_s11_0.0dBm_20230728_0pt000ghz_1pt000ghz_0pt0dbm_100avg.s2p']

for s2p in s2ps:
    ntwk = rf.Network(s2p)
    
    f = ntwk.f
    s11 = ntwk.s_db[:, 0, 0]
    
    #fig, (ax1, ax2) = plt.subplots(2, figsize=(12,8))
    #ax1.semilogx(f,s11,label='Measurement')
    #ax2.semilogx(f,ntwk.s_deg_unwrap[:,0, 0],label='Measurement')

    plt.semilogx(f,s11,label=os.path.basename(s2p).split('.')[:-1][0])

plt.legend(loc='lower left',fontsize=10)

plt.show(block=False)
