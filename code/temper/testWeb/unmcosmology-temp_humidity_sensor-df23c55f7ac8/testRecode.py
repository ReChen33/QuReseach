import sys, os
import time
directory = 'data'
fName = '{path}/{date}.txt'.format( path = directory, date = "123" )

if not os.path.exists(directory): 
    os.makedirs(directory)
    print("c")

file = open(fName,'w')
file.write( "123" )


