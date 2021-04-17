class Clock:
    def __init__(self, clock):
        if not clock:
            self.clock = 1
        self.clock = clock

    def setClock(self, clock):
        self.clock = clock

    def getClock(self):
        return self.clock    

    #increment clock with inc amount
    def incrementClock(self, inc): 
        if not inc:
            inc = 1
        self.clock = self.clock + inc    
    