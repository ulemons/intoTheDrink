from __future__ import print_function
from pathlib import Path

import threading
import random
import time

import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from picamera import PiCamera
import json
import serial



class cameraThread (threading.Thread):
    
    def __init__(self ):
        threading.Thread.__init__(self)
        self.color = '#fed332'
        self.camera = PiCamera()
        self.camera.resolution = (200,200)
    
    def readValue(self):

        self.camera.capture('/home/pi/Desktop/CameraImg/photo.png')
        time.sleep(0.1)
        NUM_CLUSTERS = 5

        im = Image.open('/home/pi/Desktop/CameraImg/photo.png')
        im = im.resize((150, 150))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

        #print('finding clusters')
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        #print('cluster centres:\n', codes)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        #print('most frequent is %s (#%s)' % (peak, colour))
        self.color = '#'+colour[2:]
        
        #self.color = peak
    
    def run(self):

        while True:
            try:
                self.readValue()
                time.sleep(1)
            except KeyboardInterrupt:  
                break
            except:
                print('something went wrong in cameraThread but fuck all this is an Hackathon!')
        

class liquidTemperatureThread (threading.Thread):
    
    def __init__(self ):
        threading.Thread.__init__(self)
        self.temperature = '0'
    
    def readValue(self):
        #vado in /sys/devices/w1_bus_master1/28-00000625c0e2/w1_slave
        content = Path('/sys/devices/w1_bus_master1/28-00000625c0e2/w1_slave').read_text()
        #prendo valore dopo =
        temp = content.split('=')[2]
        self.temperature = int(temp[:2])+int(temp[2:4])/100
        
    def run(self):

        while True:
            try:  
                self.readValue()
                time.sleep(1)
            except KeyboardInterrupt:  
                break
            except: 
                print('something went wrong in liquidTemperatureThread but fuck all this is an Hackathon!')
                

class nodeMcuThread (threading.Thread):
    
    def __init__(self ):
        threading.Thread.__init__(self)
        self.ph = 0.0
        self.torb = 0.0
        self.co2 = 0.0
        self.alchol = 0.0
        self.level = 0.0
        self.org = 0.0
        
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    
    def readValues(self):
        line = self.ser.readline()
        #print("RAW LINE: "+str(line))
        jsonMetrics = json.loads(line)
        #print("JSON: "+str(jsonMetrics))
        self.ph = jsonMetrics['ph'] != None and float(jsonMetrics['ph']) or 0.0
        self.torb = jsonMetrics['torb'] != None and float(jsonMetrics['torb']) or 0.0
        self.co2 = jsonMetrics['co2']!= None and jsonMetrics['co2']['co2']!= None and float(jsonMetrics['co2']['co2']) or 0.0
        self.org = jsonMetrics['co2']!= None and jsonMetrics['co2']['org']!= None and float(jsonMetrics['co2']['org']) or 0.0
        self.alchol = jsonMetrics['alchol'] != None and float(jsonMetrics['alchol']) or 0.0
        self.level = jsonMetrics['level'] != None and float(jsonMetrics['level']) or 0.0
        
    def run(self):

        while True:
            try:  
                self.readValues()
                time.sleep(0.5)
    
            except KeyboardInterrupt:  
                break
            
            except: 
                print('something went wrong in nodeMcuThread but fuck all this is an Hackathon! ')
                
    
def writeToFile(dictToWrite):
    #f = open('/home/pi/Desktop/SensorsInfo/metrics.txt', "w")
    f = open('/home/pi/intoTheDrink/frontEnd/intoTheDrink/src/assets/metrics.json','w')
    f.write(str(dictToWrite).replace("'","\""))
    f.close()

if __name__ == '__main__':

    cameraSensor = cameraThread()
    temperatureSensor = liquidTemperatureThread()
    nodeMcu = nodeMcuThread()

    cameraSensor.start()
    temperatureSensor.start()
    nodeMcu.start()
    
    while True:
        time.sleep(10)
        try:
            metrics = {
                "camera" : str(cameraSensor.color),
                "temp" : str(temperatureSensor.temperature),
                "ph": str(nodeMcu.ph),
                "torb": str(nodeMcu.torb),
                "co2": str(nodeMcu.co2),
                "org": str(nodeMcu.org),
                "alchol": str(nodeMcu.alchol),
                "level": str(nodeMcu.level)
            }
            
            print(metrics)
        
            writeToFile(metrics)
        except Exception: 
            print('something went wrong in main but fuck all this is an Hackathon! ')
            traceback.print_exc()
        