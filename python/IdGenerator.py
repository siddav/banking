class IdGenerator:    
    def __init__(self, seed):        
        self.seed = seed    

    # return the next sequence number
    def nextNumber(self):
        self.seed = self.seed + 1
        return self.seed