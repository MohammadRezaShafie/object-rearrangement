import os
import json
import numpy as np
from natsort import natsorted

best_frames1 = {i: [0, 0] for i in range(69)}
best_frames2 = {i: [0, 0] for i in range(69)}


def calculate_atis(xc, yc, depth, conf, width, height, obj):
    center_diff = ((abs(0.5-xc)**2) + (abs(0.5-xc)**2))**(1/2)
    if conf < 0.60:    
        seize_mul = 1
    else:
        seize_mul = 4
    
    if conf < 0.6 and (obj == 27 or obj == 57 or obj == 33 or obj == 11 or obj == 56):
        return 0 

    return 4 * (1-depth) + seize_mul * (width * height * 10) + 2 * (1-center_diff) + 2 * conf

def list_atis(folder_path, best_frames):
# Get the list of files in the 'detections' folder
    file_list = natsorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.startswith('dframe_') and f.endswith('.txt')])
    # Iterate through your text files
    for file_index, filename in enumerate(file_list):
        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                # Split the line into values
                values = line.split()
                
                # Extract relevant values
                obj_number = int(values[0])
                xc = float(values[1])
                yc = float(values[2])
                width = float(values[3])
                height = float(values[4])
                conf = float(values[5])
                depth = float(values[6])

                # Calculate atis
                atis = calculate_atis(xc, yc, depth, conf, width, height, obj_number)

                # Check and update best_frames dictionary
                if obj_number in best_frames and atis > best_frames[obj_number][-1]:
                    best_frames[obj_number] = [file_index, atis]

    # Print the updated best_frames dictionary
    for key, value in best_frames.items():
        print(f"Object {key}: Best frame - File {value[0]}, Atis {value[1]}")

def find_diff(best_frames1,best_frames2):
    for key in best_frames1.keys():
        if abs(best_frames1[key][0] - best_frames2[key][0]) > 10:
            print(f"Object {key} is different.")
        
if __name__ == '__main__':
      
    folder_path = 'detections_1'
    list_atis(folder_path, best_frames1)
    print("_____________________________________________________________")
    folder_path = 'detections_11'
    list_atis(folder_path, best_frames2)
    print("_____________________________________________________________")
    find_diff(best_frames1,best_frames2)