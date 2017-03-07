# To begin the python script, we import 3 packages, OS, Glob and time
import os
import glob
import time
import datetime

log_period = 1 # second

# Where the .csv results will be stored
logging_folder = glob.glob('/home/pi/temp_sensor/output')[0]
dt = datetime.datetime.now()
file_name = "temp_log_{:%Y_%m_%d}.csv".format(dt)
logging_file = logging_folder + '/' + file_name

 # we need to run modprobe so we can load the correct modules for temp sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

 # We then declare 3 different variables that will point to the location of our sensor data.
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
# In the read_temp_raw function we open up the file that contains our temperature output. 
 # We read all the lines from this and then return it so the code that has called this function can use it. 
 # In this case the read_temp function calls this function
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

 # In the read_temp function we process the data from the read_temp_raw function. 
 # We first make sure that the first line contains YES. This means there will be a line with a temperature in it. 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()       
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
# We then convert the number into both a Celsius and Fahrenheit temperature. We return both of these to the code that 
# called this function. This is the print function located in the while loop.        
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Log  results to .csv file
def log_temp():
    temp_c, temp_f = read_temp()
    dt = datetime.datetime.now()
    f = open(logging_file, 'a')
    f.write('\n"{:%H:%M:%S}",'.format(dt))
    f.write(str(temp_c))
    f.close()
	
print("Logging to: " + logging_file)
while True:
    log_temp()
    print(read_temp()) 
    time.sleep(log_period)
