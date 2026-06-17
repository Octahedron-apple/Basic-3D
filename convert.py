import sys
import json
import os

def convert_obj_to_json(obj_filepath, json_filepath):
    points = []
    faces = []
    
    if not os.path.exists(obj_filepath):
        print(f"Error: File '{obj_filepath}' not found.")
        sys.exit(1)
        
    print(f"Reading {obj_filepath}...")
    with open(obj_filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                points.append([x, y, z])
            elif parts[0] == 'f':
                face_indices = []
                for p in parts[1:]:
                    v_idx = int(p.split('/')[0])
                    if v_idx < 0:
                        v_idx = len(points) + v_idx
                    else:
                        v_idx -= 1
                    face_indices.append(v_idx)
                
                if len(face_indices) >= 3:
                    for i in range(1, len(face_indices) - 1):
                        faces.append([face_indices[0], face_indices[i], face_indices[i+1]])

    data = {
        "points": points,
        "faces": faces
    }
    
    with open(json_filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully converted '{obj_filepath}' to '{json_filepath}'")
    print(f"Total Points (Vertices): {len(points)}")
    print(f"Total Faces (Triangles): {len(faces)}")

if __name__ == "__main__":
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_obj_to_json(input_file, output_file)
