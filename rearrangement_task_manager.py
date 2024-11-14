import subprocess
from ai2thor.controller import Controller
from pynput import keyboard
from datetime import datetime
import time
import cv2
import os
from PIL import ImageTk, Image
import json
import numpy as np
from natsort import natsorted
import networkx as nx



import sequence_planner
import relation_graph
import set_objects_position
import find_difference_between_frames as fdbf



controller = Controller(
    agentMode="default",
    visibilityDistance=1.5,
    scene="FloorPlan1",

    gridSize=0.25,
    snapToGrid=True,
    rotateStepDegrees=90,

    renderDepthImage=True,
    renderInstanceSegmentation=True,

    width=720,#1920
    height=720,#950
    fieldOfView=90
)

object_dict ={
 0: 'Apple', 1: 'Apple_sliced', 2: 'Book', 3: 'Book_opened', 4: 'Bottle',
 5: 'Bottle_filled', 6: 'Bowl', 7: 'Bowl_filled', 8: 'Bread', 9: 'Bread_cooked_sliced',
 10: 'Bread_sliced', 11: 'ButterKnife', 12: 'Cabinet', 13: 'Cabinet_opened',
 14: 'CoffeeMachine', 15: 'CounterTop', 16: 'CreditCard', 17: 'Cup', 18: 'Cup_filled',
 19: 'DishSponge', 20: 'Drawer', 21: 'Drawer_opened', 22: 'Egg', 23: 'Egg_cooked_sliced',
 24: 'Egg_sliced', 25: 'Faucet', 26: 'Floor', 27: 'Fork', 28: 'Fridge', 29: 'Fridge_opened',
 30: 'GarbageCan', 31: 'HousePlant', 32: 'Kettle', 33: 'Knife', 34: 'Lettuce',
 35: 'Lettuce_sliced', 36: 'LightSwitch', 37: 'Microwave', 38: 'Microwave_opened',
 39: 'Mug', 40: 'Mug_filled', 41: 'Pan', 42: 'PaperTowelRoll', 43: 'PepperShaker',
 44: 'Plate', 45: 'Pot', 46: 'Pot_filled', 47: 'Potato', 48: 'Potato_cooked', 
 49: 'Potato_cooked_sliced', 50: 'Potato_sliced', 51: 'SaltShaker', 52: 'Shelf', 
 53: 'ShelvingUnit', 54: 'Sink', 55: 'SoapBottle', 56: 'Spatula', 57: 'Spoon', 
 58: 'Statue', 59: 'Stool', 60: 'StoveBurner', 61: 'StoveKnob', 62: 'Toaster',
 63: 'Tomato', 64: 'Tomato_sliced', 65: 'Vase', 66: 'Window', 67: 'WineBottle', 
 68: 'WineBottle_filled'}

reverse_action = {'MoveRight': 'MoveLeft',
                  'MoveLeft': 'MoveRight',
                  'MoveAhead': 'MoveBack',
                  'MoveBack': 'MoveAhead',
                  'LookDown': 'LookUp',
                  'LookUp': 'LookDown',
                  'RotateRight 10': 'RotateLeft 10',
                  'RotateLeft 10': 'RotateRight 10',
                  'Teleport': 'Teleport',
                  'Teleport2': 'Teleport2',
                  'Nothing' : 'Nothing'}


def find_key_by_object(obj, obj_dict):
    for key, value in obj_dict.items():
        if value == obj:
            return key
    return None

def get_next_value(d, current_key):
    keys = list(d.keys())
    try:
        current_index = keys.index(current_key)
        next_index = current_index + 1
        if next_index < len(keys):
            next_key = keys[next_index]
            return d[next_key]
        else:
            return None
    except ValueError:
        return None

def get_depth_value(xc, yc, depth_frame):
    xc = int(xc*720)
    yc = int(yc*720)
    return (depth_frame[xc, yc]/5)
       

def find_seq_tool(obj_num, obj_tools, task):
    obj_name = object_dict [obj_num]
    for successor in relation_graph.successors(obj_name):
        if relation_graph[obj_name][successor]['action'][0] == task:
            possible_tools = relation_graph[obj_name][successor]['action'][1]
    
    for i in range(len(possible_tools)):
        if possible_tools[i] == 'Hand':
            main_tool = 'Hand'
            break
        elif find_key_by_object(possible_tools[i], object_dict) in obj_tools:
            main_tool = possible_tools [i]
            break
    if main_tool:
        return main_tool
    else:
        return None
    
 
def adjust_seq_num(destination):
    global direction_flag
    global seq_num
    global sequence
    global frame_num
    temp_flagd = direction_flag
    direct = destination - frame_num  
    if direct < 0:
        direct += len(sequence)
    reverse = len(sequence) - direct
    if (direct <= reverse):
        direction_flag = True
    else:
        direction_flag = False     
    if temp_flagd != direction_flag:
        if temp_flagd:
            seq_num += 1
        else:
            seq_num -= 1    
                
                                         
def reach_frame(des_frame):
    global sequence
    global frame_num 
    global seq_num
    global direction_flag
    if frame_num == des_frame:
        return
    
    direct = des_frame - frame_num
    if direct < 0:
        direct += len(sequence)
    reverse = len(sequence) - direct
    if (direct <= reverse):
        direction_flag = True
    else:
        direction_flag = False
    
    
    while (frame_num != des_frame):
    
        # For the case that we have to reverse from start
        if frame_num == 0 and direction_flag == False:
            frame_num = len(sequence) - 1
            seq_num = len(sequence)     
            
        if direction_flag:
            frame_num += 1 
            seq_num += 1
        else:
            frame_num -= 1 
            seq_num -= 1    
        # Choosing the action based on direction
        if direction_flag:
            action = sequence[seq_num] 
        else:
            action = reverse_action[sequence[seq_num]]      

        if action == "Teleport":
            controller.step(
            action="Teleport",
            position=dict(x=1, y=0.9, z=-1.5),
            rotation=dict(x=0, y=180, z=0),
            horizon=0,
            standing=True) 
                       
        elif action == 'Teleport2':
            controller.step(
            action="Teleport",
            position=dict(x=1.25, y=0.900999903678894, z=-1.75),
            rotation=dict(x = -0.0, y = 180.0000457763672, z = 0.0),
            horizon=1.5309450418499182e-06,
            standing=True) 
                 
        elif action == "RotateLeft 10":
            controller.step(
                action="RotateLeft",
                degrees= 10
            )

        elif action == "RotateRight 10":
            controller.step(
                action="RotateRight",
                degrees= 10
            )

        elif action == "Nothing":
            pass
        else:
            controller.step(action)    
        
        print(action + " " + str(seq_num + 1) + " " + str(frame_num))
        event = controller.last_event
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_path = os.path.join('frames', f'{frame_num}.jpg')
        curr_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cv2.imwrite(os.path.join('frames', f'{curr_time}_{frame_num}.jpg'), frame_rgb)
        
    
   
      
    print("Reached Destination Frame.")
    
    
    
def slice_objects(actions_obj):   
    for key, value in actions_obj.items():
        if 'slice' in value:
            reach_frame(best_frames1[key][0])
            controller.step(action='SetObjectStates', SetObjectStates={'objectType': object_dict[key], 'stateChange': 'sliceable', 'isSliced': True})

    
    return
            
def execute_task(curr_obj, prop_obj, actions_obj, obj_tools):
    tool_flag = False
    pick_flag = False
    tool_name = ''
    global frame_num
    global seq_num
    global direction_flag
    global sequence
    
    reach_frame(prop_obj[0])
        
    if (frame_num == prop_obj[0]):
        
        # Get the object_id from object_name using metadata of our current frame
        objects_id = []
        for i in range(10):
            query = controller.step(
                action="GetObjectInFrame",
                x= prop_obj[2] - i / 100,
                y= prop_obj[3],
                checkVisible=False
            )
            if query.metadata["actionReturn"] != None:
                objects_id.append(query.metadata["actionReturn"])
        for j in range(10):
            query = controller.step(
                action="GetObjectInFrame",
                x= prop_obj[2] ,
                y= prop_obj[3]- j / 100,
                checkVisible=False
            )
            if query.metadata["actionReturn"] != None:
                objects_id.append(query.metadata["actionReturn"])
            
        main_obj = object_dict[curr_obj].split('_')[0]    
        if main_obj == 'Knife':
            main_obj = 'ButterKnife'          

        for i in range(len(objects_id)):
            temp_obj = objects_id[i].split('|')[0]
            if temp_obj == main_obj:
                object_id = objects_id[i]
                break
        
        # Doing the needed tasks for each object           
        if curr_obj in actions_obj:
            for task in actions_obj[curr_obj]:
                tool_name = find_seq_tool(curr_obj, obj_tools, task)
                print(tool_name)
                if tool_name == 'Hand':
                    pass
                elif tool_name == 'Knife':
                    pass
                else:
                    tool_key = find_key_by_object(tool_name, object_dict)
                    tool_frame = obj_tools[tool_key][1]
                    tool_flag = True
                    if pick_flag == False:
                        event = controller.step(
                            action="PickupObject",
                            objectId= object_id,
                            forceAction=True,
                            manualInteract=False
                        )
                        pick_flag = True
                        adjust_seq_num(tool_frame)
                    reach_frame(tool_frame)
                        
                if task == 'open':
                    controller.step(action="OpenObject",objectId=object_id,forceAction=True)         
                elif task == 'close':
                    controller.step(action="CloseObject",objectId=object_id,forceAction=True)                     
                elif task == 'fill':
                    controller.step(action="FillObjectWithLiquid",objectId= object_id,fillLiquid="coffee",forceAction=True)                   
                elif task == 'empty':
                    controller.step(action="EmptyLiquidFromObject",objectId=object_id,forceAction=True)                 
                elif task == 'cook':
                    controller.step(action="CookObject",objectId=object_id,forceAction=True)                      
                elif task == 'slice':  
                    # controller.step(action="SliceObject",objectId=object_id,forceAction=True)   
                    query = controller.step(
                        action="GetObjectInFrame",
                        x= (prop_obj[2] + 0.05),
                        y= prop_obj[3],
                        checkVisible=False)
                    object_id = query.metadata["actionReturn"]
                    
                if pick_flag == True:
                        adjust_seq_num(prop_obj[1])
                        reach_frame(prop_obj[1])   
                        
        if (abs(prop_obj[0] - prop_obj[1]) > 9) and pick_flag == False:
            event = controller.step(
                action="PickupObject",
                objectId= object_id,
                forceAction=False,
                manualInteract=False
            )    
            pick_flag = True
            adjust_seq_num(prop_obj[1])

    if main_obj == "Knife" or main_obj == "ButterKnife":
        slice_objects(actions_obj)
        
    # Going to the place where we have to place the object
    if pick_flag == True and tool_flag == False:
        reach_frame(prop_obj[1])           
    
    
    if (frame_num == prop_obj[1] or frame_num == prop_obj[0]) and (pick_flag == True or tool_flag == True):       
        if (curr_obj == 27 or curr_obj == 57 or curr_obj == 33 or curr_obj == 11 or curr_obj == 56):             
            controller.step(
                action="RotateHeldObject",
                pitch=0,
                yaw=90,
                roll=0
        )   
        mov_val = abs(0.5 - prop_obj[4])       
        if prop_obj[4] <= 0.5:
            controller.step("MoveHeldObjectLeft",moveMagnitude = mov_val)

        else:
            controller.step("MoveHeldObjectRight",moveMagnitude = mov_val)

        mov_val = abs(0.5 - prop_obj[5])       
        if prop_obj[5]<= 0.33:
            controller.step("MoveHeldObjectUp",moveMagnitude=mov_val + 0.25)
        else:
            controller.step("MoveHeldObjectUp",moveMagnitude=(0.5 * mov_val) + 0.1)  
            controller.step("MoveHeldObjectDown",moveMagnitude=mov_val)     
            
        if prop_obj[6]< 0.1:
            controller.step("MoveHeldObjectAhead",moveMagnitude=0.3)
        elif prop_obj[6]< 0.2:
            controller.step("MoveHeldObjectAhead",moveMagnitude=0.4)        
        elif prop_obj[6]< 0.3:
            controller.step("MoveHeldObjectAhead",moveMagnitude=0.5)     
            
        controller.step(
        action="DropHandObject",
        forceAction=True
        )   
        pick_flag = False
        
        next_obj = get_next_value(diff_obj, curr_obj)
        if next_obj == None:
            return
        adjust_seq_num(next_obj[0])
        
        event = controller.last_event
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_path = os.path.join('frames', f'{frame_num}.jpg')
        curr_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cv2.imwrite(os.path.join('frames', f'{curr_time}_{frame_num}.jpg'), frame_rgb)

    print('')

 
 
# SOME IMPORTANT GLOBAL VARIABLES
relation_graph = relation_graph.create_relation_graph()
direction_flag = False
seq_num = 0   
frame_num = 0
best_frames1 = {i: [0, 0, 0, 0, 0] for i in range(69)}
best_frames2 = {i: [0, 0, 0, 0, 0] for i in range(69)}
sequence = []
knife_moved = False
with open('sequence_with_tasks.txt', 'r') as file:
    sequence = file.read().splitlines()  
seq_length = len(sequence)
    
    
if __name__ == "__main__":

    set_objects_position.set_object_poses_from_metadata(controller, "metadata.json")
       
    folder_path = 'detections_1'
    fdbf.find_best_frames(folder_path, best_frames1)
    folder_path = 'detections_2'
    fdbf.find_best_frames(folder_path, best_frames2)
    diff_obj, obj_tools = fdbf.find_diff(best_frames1, best_frames2)  
    actions_obj = fdbf.find_actions(best_frames1, best_frames2, object_dict, diff_obj, relation_graph)
            
    lookahead = 8  
    remaining_objects = list(diff_obj.keys())
    optimal_order, min_total_distance = sequence_planner.greedy_lookahead(0, remaining_objects, diff_obj, seq_length, lookahead)
    diff_obj = {obj_id: diff_obj[obj_id] for obj_id in optimal_order}

    if abs(obj_tools[33][0] - obj_tools[33][1]) > 10 and abs(obj_tools[33][0] - obj_tools[33][1] - seq_length) > 10 :
        knife_moved = True
        ### CODE SHOULD BE ADDED FOR FALSE
    
    for curr_obj in diff_obj.keys():
        obj_prop = diff_obj[curr_obj]
        execute_task(curr_obj, obj_prop, actions_obj, obj_tools)   
        
                