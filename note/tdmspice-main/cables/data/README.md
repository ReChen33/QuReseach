>>>
Switched to an Agilent 33250A 80 MHz Function/Arbitrary Waveform
Generator, because it qualitatively looked like it has a faster pulse
which I hoped would help with parameter extraction.

./long_coax_attempt2_fcngen33250a_20230613:
Measured ~0.15 Ohm roundtrip resistance DC for this 10ft coax.
	GLSD020.CSV - Direct into scope CH4, terminated into 50 Ohm with BNC tee.
	GLSD021.CSV - 10ft long coax RG58c/u, open at end furthest from scope.
	GLSD022.CSV - 10ft long coax RG58c/u, shorted at end furthest from scope.
	GLSD023.CSV - 10ft long coax RG58c/u, 50 Ohm at end furthest from scope using trim pot.
	GLSD024.CSV - 10ft long coax RG58c/u, 75 Ohm at end furthest from scope using trim pot.
	GLSD025.CSV - 10ft long coax RG58c/u, 25 Ohm at end furthest from scope using trim pot.

./ucryo_magnanin_twp_floatingshield_try2_fcngen33250a_20230613:
Use ./long_coax_attempt2_fcngen33250a_20230613/GLSD020.CSV for the
pulse direct into scope input (terminated into 50 Ohms using a BNC
tee).
	GLSD030.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, open at end furthest from scope.  Shield floating.
	GLSD031.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, shorted at end furthest from scope.  Shield floating.
	GLSD032.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, 50 Ohm at end furthest from scope.  Shield floating.
	GLSD033.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, 75 Ohm at end furthest from scope.  Shield floating.
	GLSD034.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, 125 Ohm at end furthest from scope.  Shield floating.
	GLSD035.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, 100 Ohm at end furthest from scope.  Shield floating.
	GLSD036.CSV - 10ft long shielded twisted pair from UCryo MDM100 cable, 250 Ohm at end furthest from scope.  Shield floating.

greenbnc10ft_0.0dBm_20230620 - VNA measurement of 10ft green BNC RG58c/u cable.

ucryomanganintwpshieldfloating4ft_0.0dBm_20230620 - VNA measurement of 1.232m, 88.9Ohm roundtrip resistance manganin twp from ucryo with shield floating on both ends.


