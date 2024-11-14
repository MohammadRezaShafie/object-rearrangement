import subprocess
import os
import numpy as np
from natsort import natsorted


command = [
    'python',
    'custom_detect.py',
    '--weights',
    'task_model.pt',
    '--img-size',
    '640',
    '--conf',
    '0.5',
    '--source',
    'test4.jpg',
    '--save-txt',
    '--d_id',
    '0'
]


def get_depth_value(xc, yc, depth_frame):
    xc = int(xc*720)
    yc = int(yc*720)
    if (depth_frame[xc, yc] < 7):
        return (depth_frame[xc, yc]/7)
    else:
        while (depth_frame[xc, yc] >= 7) and (xc <= 717) and (yc <= 717): 
            xc = xc + 2
            yc = yc + 2
        if (depth_frame[xc, yc] < 7):
            return (depth_frame[xc, yc]/7)
        else:
            while (depth_frame[xc, yc] >= 7) and (xc >= 3) and (yc >= 3): 
                xc = xc - 2
                yc = yc - 2
            if (depth_frame[xc, yc] < 7):
                return (depth_frame[xc, yc]/7)
    return 0.2
            
if __name__ == "__main__":
    
    print("Entering Classification Phase 1:")
    folder_path = "frames_1/"
    files = os.listdir(folder_path)
    num_files = int((len(files)/2))
    
    for i in range(num_files):


        jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
        jpg_paths = natsorted([os.path.join(folder_path, f) for f in jpg_files])
        command[9] = jpg_paths[i]
        command[12] = str(i)
        subprocess.run(command)
    
    print("Entering Classification Phase 2:")
    dframe_folder = "detections/"
    depth_folder = "frames_1/"
    
    dframe_files = sorted([f for f in os.listdir(dframe_folder) if f.startswith("dframe_") and f.endswith(".txt")])
    depth_files = sorted([f for f in os.listdir(depth_folder) if f.startswith("depth_") and f.endswith(".txt")])


    for dframe_file, depth_file in zip(dframe_files, depth_files):
        dframe_path = os.path.join(dframe_folder, dframe_file)
        depth_path = os.path.join(depth_folder, depth_file)

        # Read the dframe file
        with open(dframe_path, 'r') as dframe_file:
            lines = dframe_file.readlines()

        # Load the depth frame
        depth_frame = np.loadtxt(depth_path)

        with open(dframe_path, 'w') as updated_dframe_file:
            for line in lines:
                values = [float(val) for val in line.split()]
                values[0] = int(values[0])
                xc, yc = values[1], values[2]

                # Get the depth value
                depth_value = get_depth_value(xc, yc, depth_frame)

                # Add the depth value to the line
                values.append(depth_value)
                updated_line = " ".join(map(str, values)) + "\n"
                updated_dframe_file.write(updated_line)
                