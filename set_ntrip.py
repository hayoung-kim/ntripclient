#! /usr/bin/env python3

## Get current lat, lon
import serial

with serial.Serial('/dev/ttyUSB0', 9800, timeout = 5) as ser:
    for i in range(50):
        line = ser.readline()
        line_ = str(line)
        line_parsed = line_.split(',')
        
        
        if 'GPGGA' in line_:            
            lat_str = line_parsed[2]
            lon_str = line_parsed[4]
            
            lat_str_deg = float(lat_str[0:2])
            lon_str_deg = float(lon_str[0:3])
            
            lat_str_min = float(lat_str[2:])
            lon_str_min = float(lon_str[3:])
            
            init_lat = lat_str_deg + lat_str_min/60.0
            init_lon = lon_str_deg + lon_str_min/60.0
            
            print('lat: ', init_lat, 'lon:', init_lon)

            break

## Parse NTRIP server lists


import subprocess


# In[2]:
print('getting ntrip server lists ........')

run_get_ntrip_lists = subprocess.check_output('./get_ntrip_lists.sh', universal_newlines=True).split('\n')


# In[3]:

mount_ = []
lat_ = []
lon_ = []


# In[4]:


for line in run_get_ntrip_lists:
    stream_info = line.split(';')
    
    if len(stream_info) < 10:
        continue
        
    if 'RTCM 3' not in stream_info[3]:
        continue
        
    mount_point, lat, lon, rtcm_ver = stream_info[1], stream_info[9], stream_info[10], stream_info[3]
    
    if not lat:
        # latitude info is empty
        continue
    
    
    mount_.append(mount_point)
    lat_.append(lat)
    lon_.append(lon)


# ## Get nearest mount point

# In[5]:

from math import sqrt



# In[7]:

min_dist = 99
for mount, lat, lon in zip(mount_, lat_, lon_):
    dlat = float(lat) - init_lat
    dlon = float(lon) - init_lon
    
    dist = sqrt(dlat**2 + dlon**2)
    
    if dist < min_dist:
        min_dist = dist
        nearest_mount = mount


# In[8]:

print('nearest mount:', nearest_mount)
print('minimum distance:', min_dist)


# ## Set options for ntripclient

# In[9]:

with open('/tmp/mountpoint','w') as f:
    f.write(nearest_mount)

