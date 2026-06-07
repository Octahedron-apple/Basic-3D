import functions 

class Char_to_Object:
    def __init__(self, String):
        self.obj = None 
        self.String = String

    def make_object(self,scale_factor):
        obj = functions.Obj()
        