import subprocess
from ai2thor.controller import Controller
from pynput import keyboard
from datetime import datetime
import time
import cv2
import os
import tkinter as tk
from PIL import ImageTk, Image
import json
import numpy as np
from natsort import natsorted
import random

object_dict = {
 
    'Apple': 0, 
    'Apple_sliced': 1, 
    'Book': 2, 
    'Book_opened': 3, 
    'Bottle': 4, 
    'Bottle_filled': 5, 
    'Bowl': 6, 
    'Bowl_filled': 7, 
    'Bread': 8, 
    'Bread_cooked_sliced': 9, 
    'Bread_sliced': 10, 
    'ButterKnife': 11, 
    'Cabinet': 12, 
    'Cabinet_opened': 13, 
    'CoffeeMachine': 14, 
    'CounterTop': 15, 
    'CreditCard': 16, 
    'Cup': 17, 
    'Cup_filled': 18, 
    'DishSponge': 19, 
    'Drawer': 20, 
    'Drawer_opened': 21, 
    'Egg': 22, 
    'Egg_cooked_sliced': 23, 
    'Egg_sliced': 24, 
    'Faucet': 25, 
    'Floor': 26, 
    'Fork': 27, 
    'Fridge': 28, 
    'Fridge_opened': 29, 
    'GarbageCan': 30, 
    'HousePlant': 31, 
    'Kettle': 32, 
    'Knife': 33, 
    'Lettuce': 34, 
    'Lettuce_sliced': 35, 
    'LightSwitch': 36, 
    'Microwave': 37, 
    'Microwave_opened': 38, 
    'Mug': 39, 
    'Mug_filled': 40, 
    'Pan': 41, 
    'PaperTowelRoll': 42, 
    'PepperShaker': 43, 
    'Plate': 44, 
    'Pot': 45, 
    'Pot_filled': 46, 
    'Potato': 47, 
    'Potato_cooked': 48, 
    'Potato_cooked_sliced': 49, 
    'Potato_sliced': 50, 
    'SaltShaker': 51, 
    'Shelf': 52, 
    'ShelvingUnit': 53, 
    'Sink': 54, 
    'SoapBottle': 55, 
    'Spatula': 56, 
    'Spoon': 57, 
    'Statue': 58, 
    'Stool': 59, 
    'StoveBurner': 60, 
    'StoveKnob': 61, 
    'Toaster': 62, 
    'Tomato': 63, 
    'Tomato_sliced': 64, 
    'Vase': 65, 
    'Window': 66, 
    'WineBottle': 67, 
    'WineBottle_filled': 68
    
}

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

def set_object_poses_from_metadata(controller, metadata_path):
    with open(metadata_path, 'r') as json_file:
        metadata = json.load(json_file)

    object_poses = []
    
    for obj in metadata['objects']:
        object_name = obj['name']
        rotation = obj['rotation']
        position = obj['position']
        object_id = obj['objectId']

        object_pose = {
            'objectName': object_name,
            'rotation': rotation,
            'position': position
        }
        object_poses.append(object_pose)

        if obj["isBroken"] ==  True:
            controller.step(action="BreakObject",objectId=object_id,forceAction=True)
        if obj["isFilledWithLiquid"] ==  True:
            controller.step(action="FillObjectWithLiquid",objectId= object_id,fillLiquid="coffee",forceAction=True)
        if obj["isSliced"] ==  True:
            controller.step(action="SliceObject",objectId=object_id,forceAction=True)
        if obj["isOpen"] ==  True:     
            controller.step(action="OpenObject",objectId=object_id,openness=1,forceAction=True)
        if obj["isCooked"] ==  True:
            controller.step(action="CookObject",objectId=object_id,forceAction=True)
        
    if object_poses:
        controller.step(action='SetObjectPoses', objectPoses=object_poses)
        print("Object poses set successfully.")
    else:
        print("No poses to set for any object in the specified JSON.")
        
    for obj in metadata['objects']:
        object_name = obj['name']
        rotation = obj['rotation']
        position = obj['position']
        object_id = obj['objectId']

        object_pose = {
            'objectName': object_name,
            'rotation': rotation,
            'position': position
        }
        # controller.step(action='SetObjectStates', SetObjectStates={'objectType': object_type, 'stateChange': 'toggleable', 'isToggled': obj["isToggled"]})
        if obj["isBroken"] ==  True:
            controller.step(action="BreakObject",objectId=object_id,forceAction=True)
        if obj["isFilledWithLiquid"] ==  True:
            controller.step(action="FillObjectWithLiquid",objectId= object_id,fillLiquid="coffee",forceAction=True)
        if obj["isSliced"] ==  True:
            controller.step(action="SliceObject",objectId=object_id,forceAction=True)
        if obj["isOpen"] ==  True:     
            controller.step(action="OpenObject",objectId=object_id,openness=1,forceAction=True)
        if obj["isCooked"] ==  True:
            controller.step(action="CookObject",objectId=object_id,forceAction=True)





def create_video_from_frames(output_video_path, frames_per_second):
    folder_path = 'frames' 
    files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    files.sort()  
    frame_width, frame_height = cv2.imread(os.path.join(folder_path, files[0])).shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frames_per_second, (frame_width, frame_height))

    frame_count = 0
    for file in files:
        frame = cv2.imread(os.path.join(folder_path, file))
        video_writer.write(frame)
        frame_count += 1

        if frame_count % frames_per_second == 0:
            video_writer.write(frame)
            frame_count += 1

    video_writer.release()
    print(f"Video created successfully at: {output_video_path}")
    
def execute_sequence():
    sequence = []
    with open('../pre-defined-paths/sequence_with_tasks.txt', 'r') as file:
        sequence = file.read().splitlines()

    for action in sequence:
        if action == "RotateLeft 10":
            controller.step(
                action="RotateLeft",
                degrees= 10
            )
        elif action == "RotateRight 10":
            controller.step(
                action="RotateRight",
                degrees= 10
            )
        elif action == "MoveHeldObjectDown":
            controller.step("MoveHeldObjectDown",moveMagnitude=0.1)
        elif action == "MoveHeldObjectLeft":
            controller.step("MoveHeldObjectLeft",moveMagnitude=0.1)
        elif action == "MoveHeldObjectRight":
            controller.step("MoveHeldObjectRight",moveMagnitude=0.1)
        elif action == "MoveHeldObjectUp":
            controller.step("MoveHeldObjectUp",moveMagnitude=0.1)
        elif action == "MoveHeldObjectAhead":
            controller.step("MoveHeldObjectAhead",moveMagnitude=0.1)
        elif action == "MoveHeldObjectBack":
            controller.step("MoveHeldObjectBack",moveMagnitude=0.1)
        elif action == "Nothing" or action == "Teleport2":
            pass
        elif action.startswith("Pickup"):
            global picked_up_object_id
            substrings = action.split()
            index = substrings.index("Pickup")
            object_id = substrings[index + 1]
            picked_up_object_id =  object_id
            event = controller.step(
                action="PickupObject",
                objectId= object_id,
                forceAction=False,
                manualInteract=False
            )
        elif action == "Drop":
            controller.step(
            action="DropHandObject",
            forceAction=True
            )   
        elif action == "Throw":
            controller.step(
            action="ThrowObject",
            moveMagnitude=150.0,
            forceAction=False
            ) 
        elif action == "Rotate":
            controller.step(
            action="RotateHeldObject",
            pitch=90,
            yaw=25,
            roll=45
            )   
        elif action == "Teleport":
            controller.step(
            action="Teleport",
            position=dict(x=1, y=0.9, z=-1.5),
            rotation=dict(x=0, y=180, z=0),
            horizon=0,
            standing=True)
        elif action == "FillIn":
            fill_in_action()
            
        elif action.startswith("Open"):
            substrings = action.split()
            index = substrings.index("Open")
            object_id = substrings[index + 1]
            event = controller.step(
                action="OpenObject",
                objectId=object_id,
                openness=1,
                forceAction=False
            )
        elif action.startswith("Close"):
            substrings = action.split()
            index = substrings.index("Close")
            object_id = substrings[index + 1]
            event = controller.step(
                action="CloseObject",
                objectId=object_id,
                forceAction=False
            )
        elif action.startswith("Break"):
            substrings = action.split()
            index = substrings.index("Break")
            object_id = substrings[index + 1]
            event = controller.step(
                action="BreakObject",
                objectId=object_id,
                forceAction=False
            )
        elif action.startswith("Slice"):
            substrings = action.split()
            index = substrings.index("Slice")
            object_id = substrings[index + 1]
            event = controller.step(
                action="SliceObject",
                objectId=object_id,
                forceAction=False
            )
        elif action.startswith("ToggleOn"):
            substrings = action.split()
            index = substrings.index("ToggleOn")
            object_id = substrings[index + 1]
            event = controller.step(
                action="ToggleObjectOn",
                objectId=object_id,
                forceAction=False
            )
        elif action.startswith("ToggleOff"):
            substrings = action.split()
            index = substrings.index("ToggleOff")
            object_id = substrings[index + 1]
            event = controller.step(
                action="ToggleObjectOff",
                objectId=object_id,
                forceAction=False
            )
        elif action.startswith("Fill"):
            substrings = action.split()
            index = substrings.index("Fill")
            object_id = substrings[index + 1]
            event = controller.step(
            action="FillObjectWithLiquid",
            objectId= object_id,
            fillLiquid="coffee",
            forceAction=False
        )
        elif action.startswith("Empty"):
            substrings = action.split()
            index = substrings.index("Empty")
            object_id = substrings[index + 1]
            event = controller.step(
            action="EmptyLiquidFromObject",
            objectId= object_id,
            forceAction=False
        )

        else:
            controller.step(action)
            
        global num_frames    
        if num_frames == 199:
            print(event.metadata["agent"])
        event = controller.last_event
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_path = os.path.join('frames', f'{num_frames}.jpg')
        cv2.imwrite(os.path.join('frames', f'{num_frames}.jpg'), frame_rgb)


        depth_data = event.depth_frame
        np.savetxt(f'frames/depth_{num_frames}.txt', depth_data, fmt='%.6f')
        num_frames += 1


def select_element():
    try:
        selected_index = listbox.curselection()
        if selected_index:
            element = listbox.get(selected_index[0])
            root.quit()
            return element
    except tk.TclError:
        pass
    
def close_window():
    root.destroy()
    return None

def display_list(strings):
    global root, listbox
    root = tk.Tk()
    root.title("Select an Element")
    
    listbox = tk.Listbox(root)
    for string in strings:
        listbox.insert(tk.END, string)
    listbox.pack()

    select_button = tk.Button(root, text="Select", command=select_element)
    select_button.pack()

    close_button = tk.Button(root, text="Close", command=close_window)
    close_button.pack()

    root.mainloop()

def get_object_in_frame():
    object_ids = []
    for i in range(0, 10):
        i = i / 50
        for j in range(0, 10):
            j = j / 50
            query = controller.step(
                action="GetObjectInFrame",
                x=0.40+i,
                y=0.40+j,
                checkVisible=False
            )
            object_ids.append(query.metadata["actionReturn"])      
    object_ids = list(set(object_ids))
    print(object_ids)
    display_list(object_ids)
    object_id = select_element()
    try:
        root.destroy()
    except tk.TclError:
        pass
    return object_id
    
         
def rotate_left():
    controller.step(
    action="RotateLeft",
    degrees= 10
    )
       

def rotate_right():
    controller.step(
    action="RotateRight",
    degrees= 10
    )
    
  

def pickup_action():
    global picked_up_object_id
    object_id = get_object_in_frame()
    picked_up_object_id =  object_id
    event = controller.step(
        action="PickupObject",
        objectId= object_id,
        forceAction=False,
        manualInteract=False
    )


def drop_action():
    controller.step(
    action="DropHandObject",
    forceAction=True
    )   

def throw_action():
    controller.step(
    action="ThrowObject",
    moveMagnitude=150.0,
    forceAction=False
    ) 
    
def rotate_action():
    controller.step(
        action="RotateHeldObject",
        pitch=90,
        yaw=25,
        roll=45
    )   

def open_action():   
    object_id = get_object_in_frame()
    event = controller.step(
        action="OpenObject",
        objectId=object_id,
        openness=1,
        forceAction=False
    )
    return object_id

def close_action():   
    object_id = get_object_in_frame()
    controller.step(
        action="CloseObject",
        objectId=object_id,
        forceAction=False
    )
    return object_id

def break_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="BreakObject",
    objectId=object_id,
    forceAction=False
    )
    return object_id

def slice_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="SliceObject",
    objectId=object_id,
    forceAction=False
    )
    return object_id

def toggle_on_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="ToggleObjectOn",
    objectId= object_id,
    forceAction=False
    )
    return object_id

def toggle_off_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="ToggleObjectOff",
    objectId= object_id,
    forceAction=False
    )
    return object_id
def cook_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="CookObject",
    objectId=object_id,
    forceAction=False)
    return object_id

def fill_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="FillObjectWithLiquid",
    objectId= object_id,
    fillLiquid="coffee",
    forceAction=False
    )
    return object_id

def empty_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="EmptyLiquidFromObject",
    objectId= object_id,
    forceAction=False
    )
    return object_id

def fill_in_action():
    controller.step(
        action="RotateHeldObject",
        pitch=0,
        yaw=0,
        roll= -80
    )   
    event = controller.last_event
    for i in range (len(event.metadata["objects"])):
        if(event.metadata["objects"][i]["objectId"] == picked_up_object_id):
            picked_object_pos = event.metadata["objects"][i]["position"]
            break
    for j in range (len(event.metadata["objects"])):
        if((event.metadata["objects"][j]["position"]["x"] <= (picked_object_pos["x"] + 0.2) 
            and event.metadata["objects"][j]["position"]["x"] >= (picked_object_pos["x"] - 0.2))
            and (event.metadata["objects"][j]["position"]["y"] <= (picked_object_pos["y"] + 0.2) 
            and event.metadata["objects"][j]["position"]["y"] >= (picked_object_pos["y"] - 0.2))
            and event.metadata["objects"][j]["position"]["z"] < (picked_object_pos["z"])
            and event.metadata["objects"][j]["canFillWithLiquid"] == True
            and event.metadata["objects"][j]["isFilledWithLiquid"] == False):
                object_id = event.metadata["objects"][j]["objectId"]
                event = controller.step(
                action="FillObjectWithLiquid",
                objectId= object_id,
                fillLiquid="coffee",
                forceAction=False
                )
                event = controller.step(
                action="EmptyLiquidFromObject",
                objectId= picked_up_object_id,
                forceAction=False
                )
                break
                



def on_press(key):
    global num_frames  
    try:
        if key.char == 'w':
            controller.step("MoveAhead")
            sequence.append("MoveAhead") 
        elif key.char == 's':
            controller.step("MoveBack")
            sequence.append("MoveBack") 
        elif key.char == 'a':
            controller.step("MoveLeft")
            sequence.append("MoveLeft")
        elif key.char == 'd':
            controller.step("MoveRight")
            sequence.append("MoveRight") 
        elif key.char == 'i':
            controller.step("LookUp")
            sequence.append("LookUp")
        elif key.char == 'k':
            controller.step("LookDown")
            sequence.append("LookDown")
        elif key.char == 'j':
            rotate_left()
            sequence.append("RotateLeft 10")
        elif key.char == 'l':
            rotate_right()
            sequence.append("RotateRight 10") 
            
        elif key.char == 'e':
            pickup_action()       
            if picked_up_object_id:
                sequence.append("Pickup " + picked_up_object_id)
        elif key.char == 'q':
            drop_action()  
            sequence.append("Drop") 
        elif key.char == 'z':
            throw_action()
            sequence.append("Throw") 
        elif key.char == 'r':
            rotate_action()
            sequence.append("Rotate") 
        elif key.char == 'o':
            object_id = open_action()
            if object_id:
                sequence.append("Open " + object_id)
        elif key.char == 'u':
            object_id = close_action()
            if object_id:
                sequence.append("Close " + object_id)
        elif key.char == 'b':
            object_id = break_action()
            if object_id:
                sequence.append("Break " + object_id)
        elif key.char == 'n':
            object_id = slice_action()
            if object_id:
                sequence.append("Slice " + object_id)
        elif key.char == 't':
            object_id = toggle_on_action()
            if object_id:
                sequence.append("ToggleOn " + object_id)    
        elif key.char == 'g':
            object_id = toggle_off_action()
            if object_id:
                sequence.append("ToggleOff " + object_id)       
        elif key.char == 'f':
            object_id = fill_action()
            if object_id:
                sequence.append("Fill " + object_id)    
        elif key.char == 'v':
            object_id = empty_action()
            if object_id:
                sequence.append("Empty " + object_id) 
        elif key.char == 'c':
            object_id = cook_action()
            if object_id:
                sequence.append("Cook " + object_id) 
        elif key.char == 'y':
            sequence.append("FillIn") 
            fill_in_action() 
        elif key.char == '.':
            controller.step(
            action="Teleport",
            position=dict(x=1, y=0.9, z=-1.5),
            rotation=dict(x=0, y=180, z=0),
            horizon=0,
            standing=True)
            sequence.append("Teleport") 
        elif key.char == '/':
            set_object_poses_from_metadata(controller, "metadata12.json")
        
        elif key.char == '2':
            controller.step("MoveHeldObjectDown",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectDown") 
        elif key.char == '4':
            controller.step("MoveHeldObjectLeft",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectLeft") 
        elif key.char == '6':
            controller.step("MoveHeldObjectRight",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectRight")
        elif key.char == '8':
            controller.step("MoveHeldObjectUp",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectUp") 
        elif key.char == '9':
            controller.step("MoveHeldObjectAhead",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectAhead") 
        elif key.char == '3':
            controller.step("MoveHeldObjectBack",moveMagnitude=0.1)
            sequence.append("MoveHeldObjectBack") 
           
        elif key.char == 'p':
            execute_sequence()
            num_frames -= 1
        

  
        event = controller.last_event
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_path = os.path.join('frames', f'{num_frames}.jpg')
        cv2.imwrite(os.path.join('frames', f'{num_frames}.jpg'), frame_rgb)

        depth_data = event.depth_frame
        np.savetxt(f'frames/depth_{num_frames}.txt', depth_data, fmt='%.6f')
        num_frames += 1
    
            
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')
    if key == keyboard.Key.esc:  
        with open('sequence.txt', 'w') as file:
            if sequence:
                for action in sequence:
                    file.write(action + '\n')
        curr_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_video_path = f'video_{curr_time}.mp4' 
        frames_per_second = 4
        create_video_from_frames(output_video_path, frames_per_second)
        return False
 
def delete_previous_frames():
    for filename in os.listdir("frames"):
        file_path = os.path.join("frames", filename)
        os.remove(file_path)
 
def get_depth_value(xc, yc, depth_frame):
    xc = int(xc*720)
    yc = int(yc*720)
    return (depth_frame[xc, yc]/5)
 
num_frames = 0

def count_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        return f"File not found: {file_path}"
    


if __name__ == "__main__":
    file_path = 'pre-defined-paths/sequence_with_tasks.txt'
    action_num = count_lines(file_path)
    sequence = []
 
    # delete_previous_frames()
    # Used for setting the pre-defined scene
    # set_object_poses_from_metadata(controller,"metadata3.json")
 
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  

    # Used for saving the current scene metadata
    # event = controller.last_event 
    # json_data = json.dumps(event.metadata)
    # with open("metadata12.json", "w") as json_file:
    #     json_file.write(json_data)
        
                
    

