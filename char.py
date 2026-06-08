import functions 
import json
import numpy as np
import os

class Char_to_Object:
    def __init__(self, String, font_file="default_font.json"):
        self.obj = None 
        self.String = String
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, font_file)
        
        with open(font_path, 'r') as f:
            self.font_data = json.load(f)

    def make_object(self, scale_factor):
        if not self.String:
            return functions.Obj()
            
        char = self.String[0].upper()
        
        if char not in self.font_data:
            char = " "
            if char not in self.font_data:
                return functions.Obj()
            
        char_data = self.font_data[char]
        new_obj = functions.Obj()
        
        for p in char_data["points"]:
            scaled_p = np.array(p) * scale_factor
            new_obj.Points.append(functions.Point(scaled_p))
            
        for f in char_data["faces"]:
            new_obj.Faces.append(tuple(f))
            
        self.obj = new_obj
        return self.obj