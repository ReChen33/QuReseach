import numpy as np
import scipy.constants
import sys
import matplotlib.pylab as plt

# Trying to reproduce some skin effect calcs
# from "Compact Equivalent Circuit Model for the Skin Effect", S. Kim
# & D.P. Neikirk, 1996.

alpha_R=float(sys.argv[1])
alpha_L=float(sys.argv[2])
Lint_per_m=float(sys.argv[3])
Llf_per_m=float(sys.argv[4])
Rdc_per_m=float(sys.argv[5])

Lext_per_m = Llf_per_m-Lint_per_m

print(f'alpha_R = {alpha_R:.3f}')
print(f'alpha_L = {alpha_L:.3f}')

print(f'Llf_per_m = {Llf_per_m*1.e9:.1f} nH/m')

print(f'Lint_per_m = {Lint_per_m*1.e9:.1f} nH/m')
print(f'Lext_per_m = {Lext_per_m*1.e9:.1f} nH/m')

print(f'Rdc_per_m = {Rdc_per_m:.1f} Ohm/m')
print('--------------------')

## ## Twisted pair geometry
## # units um
## # single conductor radius
## r_um=127/2. # 0.005in diameter is 36 AWG
## # separation between wire centers
## insulation_thickness_um=114.3
## d_um=(r_um+insulation_thickness_um)
## 
## # Resistivity
## rho=Rdc_per_m*(np.pi * (r_um/1.e6)**2)*1.e6 # uOhm * m
## print(f'rho = {rho} uOhm*m')
## # Conductivity
## sigma = 1./rho
## 
## # Eq. 8
## zeta=( 1. / np.pi )*(
##     np.arcsin( np.sqrt( 1. - (r_um/d_um)**2. ) )
## )
## 
## print(f'zeta = {zeta}')
## 
## # Eq. 5
## # Maximum frequency of interest
## f_max = 10.e6
## omega_max = 2.*np.pi*f_max
## # Magnetic permeability of free space
## mu_0 = scipy.constants.physical_constants['vacuum mag. permeability'][0] # N/A^2
## print(f'mu_0 = {mu_0}')
## # Skin depth (meters)
## delta_max = np.sqrt( (2. * (rho/1.e6) ) / ( omega_max * mu_0)  )
## print(f'delta_max = {delta_max}')
## 
## # Eq 4
## alpha_R = 0.53*(r_um/1.e6)/delta_max
## print(f'alpha_R = {alpha_R}')
## # Eq 6
## alpha_L = 0.315*alpha_R
## 
## # Eq 1
## R1 = alpha_R*Rdc_per_m

# Solve Eq 2
## Apparently, alphaR needs to be bigger than 1!  Kludge for now.
R_coeff = [ 1., 1., 1., (1. - alpha_R) ]
R_roots=np.roots(R_coeff)
R_real_valued_positive_roots = R_roots.real[(abs(R_roots.imag)<1e-5)&(R_roots.real>0)]
if len(R_real_valued_positive_roots)!=1:
    print('! Failed to solve for RR!  Abort!')
    sys.exit(1)
RR = R_real_valued_positive_roots[0]
print(f'RR = {RR}')

# Assume some alpha_L
invL_coeff = [ 1.,
               ( 1. + ( 1. / RR ) )**2,
               ( ( ( 1. / RR )**2 + ( 1. / RR ) + 1. )**2 -
                 alpha_L*( ( 1. + ( 1. / RR ) )*
                           ( 1. + ( 1. / RR )**2 ) )**2 ) ]

invL_roots=np.roots(invL_coeff)
invL_real_valued_positive_roots = invL_roots.real[(abs(invL_roots.imag)<1e-5)&(invL_roots.real>0)]
if len(invL_real_valued_positive_roots)!=1:
    print('! Failed to solve for LL!  Abort!')
    sys.exit(1)
LL = 1./(invL_real_valued_positive_roots[0])
print(f'LL = {LL}')
print('--------------------')

f=np.linspace(1.,1e9,1000000)
omega=2.*np.pi*f
d={}
for ii in range(4):
    print(f'R{ii+1} = {alpha_R*Rdc_per_m/(RR)**(ii):.1f} Ohm')
    print(f'L{ii+1} = {1.e9*(Lint_per_m/alpha_L)/(LL)**(ii):.1f} nH')
    
    d[f'R{ii+1}'] = alpha_R*Rdc_per_m/(RR)**(ii) # Ohm
    if ii<3:
        d[f'L{ii+1}'] = (Lint_per_m/alpha_L)/(LL)**(ii) # H

L2Ohm = lambda f_Hz,L_Henry : 1.j*2.*np.pi*f_Hz*(L_Henry)

Z= L2Ohm(f,Lext_per_m) + 1./(1./d['R1']+1./(L2Ohm(f,d['L1'])+1./(1./d['R2']+1./(L2Ohm(f,d['L2']) + 1./(1./d['R3'] + (1./(L2Ohm(f,d['L3']) + d['R4'])))))))

#invZtotal += 1./( d[f'R{ii+1}'] + 1.j * (2. * np.pi * f)*d[f'L{ii+1}']*1.e-6 )
#Ztotal = 1./invZtotal

plt.ion()

fig, ax1 = plt.subplots()

color = 'tab:green'
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Resistance ($\Omega$)', color=color)
ax1.semilogx(f, np.real(Z), color=color,label='Kim (1996)')

# McCammo
#color = 'tab:lime'
#plt.plot(

ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('L ($\mu$H)', color=color)  # we already handled the x-label with ax1
ax2.plot(f, 1.e9*np.imag(Z)/2./np.pi/f, color=color, label='Kim (1996)')

## # McCammon
## color = 'tab:cyan'
## A=1.6
## omegaL = 2.*np.pi*161.e3
## Linf_per_m = Llf_per_m/2.
## ax2.plot(f, Linf_per_m + (Llf_per_m - Linf_per_m)/(1. + A*(omega/omegaL) + (omega/omegaL)**2 )**(1./4.), color=color, linestyle='--')

ax2.tick_params(axis='y', labelcolor=color)
