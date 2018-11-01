#!/usr/bin/python
import urllib.request
import os, sys
from gmap_utils import *

import time
import random
import json

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

    start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)
    print(start_x, start_y, "    ", stop_x, stop_y)
    print ("x range", start_x, stop_x)
    print ("y range", start_y, stop_y)
    total = abs(start_x - stop_x) * abs(stop_y - start_y)
    print("total", total)
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    headers = { 'User-Agent' : user_agent }
    now = 0
    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):
            url = None
            filename = None
            #https://www.google.cn/maps/vt?lyrs=s@817&gl=cn&x=1&y=2&z=2
            #https://www.google.cn/maps/vt?lyrs=s@817&gl=cn&x=3417&y=1607&z=12
            urlf1 = "http://mt0.google.cn/vt/lyrs=s@817&gl=cn&x=%d&y=%d&z=%d"
            urlf2 = "https://www.google.cn/maps/vt?lyrs=s@817&gl=cn&x=%d&y=%d&z=%d"

            if satellite:        
                url = urlf2 % (x,y,zoom)   #kh?v=87&hl=en&x=%d&y=%d&z=%d" % (x, y, zoom
                filename = "maps/%d/%d_%d_%d_s.jpg" % (zoom, zoom, x, y)
              
            if not os.path.isdir("maps/%d" % zoom) :
                os.mkdir("maps/%d" % zoom)

            if not os.path.exists(filename):
                
                bytes = None
                
                try:
                    print("start request ", url)
                    req = urllib.request.Request(url, data=None, headers=headers)
                    response = urllib.request.urlopen(req)
                    bytes = response.read()
                except Exception as e:
                    print ("--", filename, "->", e)
                    sys.exit(1)
                
                if bytes.startswith("<html>".encode('utf-8')):
                    print ("-- forbidden", filename)
                    sys.exit(1)
                
                print ("-- saving", filename)
                now = now + 1
                print("progress -- %d/%d"%(now,total))
                f = open(filename,'wb')
                f.write(bytes)
                f.close()
                
                time.sleep(1 + random.random())
            else:
                now = now + 1
                print(filename, "already exist")

if __name__ == "__main__":

    #longtitude  经度
    #latitude  纬度
    '''
    zoom = 15
    
    lat_start, lon_start = 46.53, 6.6
    lat_stop, lon_stop = 46.49, 6.7
        
    download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)
    '''

    for i in range(len(sys.argv)):
        print ("arg", i, sys.argv[i])
    if(sys.argv[1] != None):
        f = open(sys.argv[1],mode="r",encoding='utf-8')
        content = f.read()
        cfg = json.loads(content)
        lon_start = cfg["startx"]
        lon_stop = cfg["stopx"]

        lat_start = cfg["starty"]
        lat_stop = cfg["stopy"]

        zoom = cfg["zoom"]
        download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)