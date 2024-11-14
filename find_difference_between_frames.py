from natsort import natsorted
import os
import networkx as nx

def find_key_by_object(obj, obj_dict):
    for key, value in obj_dict.items():
        if value == obj:
            return key
    return None

def calculate_best_frame(xc, yc, depth, conf, width, height, obj):
    center_diff = ((abs(0.5-xc)**2) + (abs(0.5-xc)**2))**(1/2)
    if conf < 0.60:    
        seize_mul = 1
    else:
        seize_mul = 4
    
    if conf < 0.6 and (obj == 27 or obj == 57 or obj == 33 or obj == 11 or obj == 56):
        return 0 

    return 4 * (1-depth) + seize_mul * (width * height * 10) + 2 * (1-center_diff) + 2 * conf


def find_best_frames(folder_path, best_frames):
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

                # Calculate best frame
                best_value = calculate_best_frame(xc, yc, depth, conf, width, height, obj_number)

                # Check and update best_frames dictionary
                if obj_number in best_frames and best_value > best_frames[obj_number][1]:
                    best_frames[obj_number] = [file_index, best_value, xc, yc, depth]
                    
 
def find_diff(best_frames1,best_frames2):
    seq_objs = [33, 11, 60, 54, 25, 14, 62]
    seq_dict = {}
    diff_dict = {}
    for key in best_frames1.keys():
        if key in seq_objs and (best_frames1[key][0]!= 0 or best_frames2[key][0]!= 0):
            seq_dict[key] = [best_frames1[key][0], best_frames2[key][0], best_frames1[key][2], best_frames1[key][3]
                              ,best_frames2[key][2], best_frames2[key][3], best_frames2[key][4]]           
        if abs(best_frames1[key][0] - best_frames2[key][0]) > 10:
            diff_dict[key] = [best_frames1[key][0], best_frames2[key][0], best_frames1[key][2], best_frames1[key][3]
                              ,best_frames2[key][2], best_frames2[key][3], best_frames2[key][4]]
    return diff_dict, seq_dict



def find_path_between_objects(start_obj, end_obj, G):
    if start_obj not in G.nodes or end_obj not in G.nodes:
        return False
    try:
        forward_path = nx.algorithms.shortest_paths.generic.shortest_path(G, start_obj, end_obj)
        if forward_path: 
            edges_list = [G[forward_path[i]][forward_path[i+1]]['action'] for i in range(len(forward_path)-1)] 
            if edges_list == []:
                return False
            actions_list = []
            for edge in range (len(edges_list)):
                actions_list.append(edges_list[0][0])
            return actions_list
        else: 
            return False
    except nx.NetworkXNoPath: 
        return False


def find_actions(best_frames1, best_frames2, object_dict, diff_obj, G):
    for i in diff_obj:
        obj1 = diff_obj[i]
        for j in diff_obj:
            obj2 = diff_obj[j]
            start_obj_name = object_dict[i]
            end_obj_name = object_dict[j]
            path = find_path_between_objects(start_obj_name, end_obj_name , G)     
            if (path != False) and (obj2[2] != 0) and (obj2[3] != 0) and (obj1[2] != 0) and (obj1[3] != 0) and (len(start_obj_name) < len(end_obj_name)):
                obj1[0] = 0
                obj1[2] = 0
                obj1[3] = 0
                
    for i in diff_obj:
        obj1 = diff_obj[i]
        for j in diff_obj:
            obj2 = diff_obj[j]
            start_obj_name = object_dict[i]
            end_obj_name = object_dict[j]
            path = find_path_between_objects(start_obj_name, end_obj_name , G)     
            if (path != False) and (obj2[4] != 0) and (obj2[5] != 0) and (obj1[4] != 0) and (obj1[5] != 0) and (len(start_obj_name) < len(end_obj_name)):
                obj1[1] = 0
                obj1[4] = 0
                obj1[5] = 0                
            
                   
    action_dict = {}
    items_to_remove = []
    sliced_objects = {}
    for start in diff_obj:
        path = False
        start_obj = diff_obj[start]
        start_obj_name = object_dict[start]
        if (start_obj[0] == 0 and start_obj[2] == 0 and start_obj[3] == 0) and (start not in  items_to_remove):
            for end in diff_obj:
                end_obj = diff_obj[end]
                if (end_obj[1] == 0 and end_obj[4] == 0 and end_obj[5] == 0) and (end not in  items_to_remove):
                    end_obj_name = object_dict[end]
                    path = find_path_between_objects(end_obj_name, start_obj_name , G)
                    if path != False:
                        action_dict[end] = path
                        end_obj[1] = start_obj[1]
                        end_obj[4] = start_obj[4]
                        end_obj[5] = start_obj[5]
                        end_obj[6] = start_obj[6]
                        items_to_remove.append(start)
                        break 
            for predecessor in G.predecessors(start_obj_name):
                if G[predecessor][start_obj_name]['action'] [0] == 'slice':
                    predecessor_id = find_key_by_object(predecessor, object_dict)
                    sliced_objects[predecessor_id] = [best_frames1[predecessor_id][0], start_obj[1],
                                                best_frames1[predecessor_id][2],best_frames1[predecessor_id][3],
                                                start_obj[4], start_obj[5], start_obj[6]]
                    items_to_remove.append(start)
                    
        elif (start_obj[1] == 0 and start_obj[4] == 0 and start_obj[5] == 0) and (start not in  items_to_remove):
            for end in diff_obj:
                end_obj = diff_obj[end]
                if (end_obj[0] == 0 and end_obj[2] == 0 and end_obj[3] == 0) and (end not in  items_to_remove):
                    end_obj_name = object_dict[end]
                    path = find_path_between_objects(start_obj_name,end_obj_name  , G)
                    if path != False:
                        action_dict[start] = path
                        start_obj[1] = end_obj[1]
                        start_obj[4] = end_obj[4]
                        start_obj[5] = end_obj[5]
                        start_obj[6] = end_obj[6]
                        items_to_remove.append(end)
                        break 
                            
    for item in items_to_remove:
        diff_obj.pop(item)
    for obj_id in sliced_objects:
        obj_prop = sliced_objects[obj_id]
        diff_obj[obj_id] = [obj_prop[0], obj_prop[1],
                                obj_prop[2], obj_prop[3],
                                obj_prop[4], obj_prop[5], obj_prop[6]]
        action_dict[obj_id] = ['slice']
    return action_dict      