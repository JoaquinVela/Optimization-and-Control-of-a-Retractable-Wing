class wingGeometry:
    def __init__(self, span, chord):
        self.span = span 
        self.chord = chord 

    def area(self):
        return self.span * self.chord
    
    def aspectRatio(self): 
        return self.span**2 / self.area()
    
