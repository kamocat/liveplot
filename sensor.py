import asyncio
import time
import random

'''Fake class that returns a dict'''
def Series(label: str, scale: str):
    return {'scale':scale, 'label':label}

class RandomWalk:
    def __init__(self, rate=0.1):
        self.a = rate
        self.y = 0
    @property
    def value(self):
        x = random.gauss(sigma=20)
        self.y += self.a*(x-self.y)
        return round(self.y,2)

class Sensor:
    def __init__(self):
        #Initialization
        self.r1 = RandomWalk(0.1)
        self.r2 = RandomWalk(0.01)
        self.r3 = RandomWalk(0.05)
        self.file = None
        self.delimiter = ','
        self.want_abort = False
        self.delay = 1
        self.legend = [
            Series("seconds", "time"),
            Series("Rand1", "temperature"),
            Series("Rand2", "temperature"),
            Series("Rand3", "temperature"),
        ]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        #time.sleep(1)
        return [time.time(), self.r1.value, self.r2.value, self.r3.value]
    
    async def run(self):
        for vals in self:
            if self.file is not None:
                self.file.write(self.delimiter.join(vals)+'\n')
                self.file.flush()
            asyncio.sleep(self.delay)
            if self.want_abort:
                break
        self.file.close()
    
    def log(self, fname):
        if self.file is not None:
            file.close()
        try:
            self.file = open(fname, 'w')
        except OSError as e:
            print(e)
            self.file = None
            return False
        h = [x["label"] for x in self.legend]
        self.file.write(self.delimiter.join(h)+'\n')
        self.file.flush()