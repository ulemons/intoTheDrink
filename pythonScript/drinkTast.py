import threading
import random
import time


class generalThread (threading.Thread):
    
    def __init__(self ):
        threading.Thread.__init__(self)
        self.myInt = 0
    
    def getRandomValue(self):
        self.myInt = random.randint(0, 5)
        print "scrivo: "+ str(self.myInt)
    
    def run(self):

        while True:
            try:  
                self.getRandomValue()
                time.sleep(1)
            
            except KeyboardInterrupt:  
                GPIO.cleanup()
                break

if __name__ == '__main__':
    generalSensor1 = generalThread()
    generalSensor1.start()


    generalSensor2 = generalThread()
    generalSensor2.start()

    while True:
        print "leggo sensore 1: "+str(generalSensor1.myInt)
        print "leggo sensore 2: "+str(generalSensor2.myInt)
        time.sleep(1)