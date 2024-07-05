# Imports and file location

import pickle as pkl
import numpy as np

wafer_file = 'wafer/nist_so_mf_detector_array_padinfo.csv'
save_file = 'wafer/wafer_dict.pkl'

# Create empty dictionary
wafer_dict = {}

# Open csv file and save headers
f = open(wafer_file)
headers = f.readline().split(',')

# Iterate through all other lines in file and create a sub-dictionary for each unique pixel name
for line in f:
    detector_info = line.split(',')
    pixel_name = 'Pixel_'+detector_info[2]+'_'+str(int(detector_info[6])).zfill(2)+str(int(detector_info[7])).zfill(2)
    wafer_dict[pixel_name] = {}
f.close()

# Repeat to make a new ub-dictionary for each unique detector name
f = open(wafer_file)
f.readline()
for line in f:
    detector_info = line.split(',')
    pixel_name = 'Pixel_'+detector_info[2]+'_'+str(int(detector_info[6])).zfill(2)+str(int(detector_info[7])).zfill(2)
    detector_name = detector_info[3][0:3]
    wafer_dict[pixel_name][detector_name] = {}
    wafer_dict[pixel_name][detector_name]['+']={}
    wafer_dict[pixel_name][detector_name]['-']={}
f.close

# Loop through file one more time to save all data in this new dictionary
f = open(wafer_file)
f.readline()

# Setting variable types from looking at data in file

# these columns are integers
det_info_int = [1,6,7,8]

# these columns are floating point numbers
det_info_float = [4,5,10,11,12,13]

# keep everything else as string
# det_info_str = [0,2,3,9]

for line in f:
    detector_info = line.split(',')
    pixel_name = 'Pixel_'+detector_info[2]+'_'+str(int(detector_info[6])).zfill(2)+str(int(detector_info[7])).zfill(2)
    detector_name = detector_info[3][0:3]
    det_polarity = detector_info[3][3]
    for i in range(0,len(headers)):
        if i in det_info_int: 
            det_info = int(detector_info[i])
        elif i in det_info_float:
            det_info = float(detector_info[i])
        else:
            det_info = detector_info[i]
                
        wafer_dict[pixel_name][detector_name][det_polarity][headers[i]] = det_info

with open(save_file,'wb') as f2:
    pkl.dump(wafer_dict,f2)

