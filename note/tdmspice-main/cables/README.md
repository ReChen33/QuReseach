

On windows machine

- Go to https://www.python.org/downloads/ (must put in windows path and install pip).
	- Tried 3.11.4.  Right click the installer and install as administrator.  Enable the Install for all users and install pip options.
- Confirm python is now in path by entering 

echo $PATH$

In a windows cmd session.
- If it’s there, you should be able to verify python is installed by running

python

In a windows command session.
- If that’s successful, can install PyLTSpice (https://pypi.org/project/PyLTSpice/) using pip

pip install PyLTSpice

You may want to upgrade pip.  If you do upgrade pip, you may want to then upgrade PyLTSpice via

pip install —upgrade PyLTSpice
>>
pip3 install ltspice
>>
https://ltwiki.org/index.php?title=O-device_(Lossy_Transmission_Line)_and_T-device_(Lossless_Transmission_Line)_modelling_issues - If can't get what we need out of basic SPICE models like LTRA, there's some more advanced modelling possible.

https://www.edn.com/designing-with-a-complete-simulation-test-bench-for-op-amps-part-4-noise - examples for bench testing amp noise models.

Tline_3_cases.asc - starting example from https://iexploresiliconvalley.com/2019/08/27/ltspice-lesson-3-transmission-lines-part-1/.

rg58c-u.pdf - Typical datasheet for RG58C/U coax.