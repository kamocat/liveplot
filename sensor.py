import time
import random

class Sensor:
    def __iter__(self):
        #Initialization
        return self
    
    def __next__(self):
        #time.sleep(1)
        return [time.time(), random.randrange(1), random.randrange(10), random.randrange(20)]

'''Fake class that returns a dict'''
def Series(label: str, scale: str):
    return {'scale':scale, 'label':label}

legend = [
        Series("seconds", "time"),
        Series("cpu", "acceleration"),
        Series("RPM", "rotation"),
        Series("Upper", "temperature"),
]