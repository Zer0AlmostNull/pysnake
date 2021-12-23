class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
    
    def __mul__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        return Point(x, y)
    
    def __div__(self, other):
        x = self.x / other.x
        y = self.y / other.y
        return Point(x, y)
    
    def __pow__(self, other):
        x = self.x ** other
        y = self.y ** other
        return Point(x, y)
    
    def __iter__(self):
        yield self.x
        yield self.y
    def copy(self):
        return Point(self.x, self.y)
        
    def __eq__(self, other):
        return (other.x == self.x and other.y == self.y)
    
    def __str__(self):
        return "({0},{1})".format(self.x, self.y)        
