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
    'Egg': 22, #
    'Egg_cooked_sliced': 23, #
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
    'Mug_filled': 40, #
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

    width=720,
    height=720,
    fieldOfView=90
)


###### Used for ensuring that our dataset is not biased towards unimportant properties

# controller.step(
#     action="RandomizeMaterials",
#     useTrainMaterials=None,
#     useValMaterials=None,
#     useTestMaterials=None,
#     inRoomTypes=None
# )


###### Used for creating multiple instances of an object for dataset collection


# controller.step(
#     action="InitialRandomSpawn",
#     randomSeed=random.randint(0,8),
#     forceVisible=False,
#     numPlacementAttempts=5,
#     placeStationary=True,
#     numDuplicatesOfType = [{
#             "objectType": "Mug", 
#              "count" : 30
#     }
#     ,
#     {
#             "objectType": "Egg",
#              "count" : 30
#     }
#     ,
#     {
#             "objectType": "Bread",
#              "count" : 30
#     }
#     ],
#     excludedReceptacles=[],
#     excludedObjectIds=[]
# )


    
def execute_sequence():
    sequence = []
    with open('sequence.txt', 'r') as file:
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

        time.sleep(0.1)  
        event = controller.step('Pass') 
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cv2.imwrite(os.path.join('frames', f'frame_{current_time}.jpg'), frame_rgb)


def get_depth_value(xc, yc, depth_frame):
    xc = int(xc*720)
    yc = int(yc*720)
    if (depth_frame[xc, yc] < 7):
        return (depth_frame[xc, yc]/7)
    else:
        while (depth_frame[xc, yc] >= 7) and (xc <= 717) and (yc <= 717): 
            xc = xc + 1
            yc = yc + 1
        if (depth_frame[xc, yc] < 7):
            return (depth_frame[xc, yc]/7)
        else:
            while (depth_frame[xc, yc] >= 7) and (xc >= 3) and (yc >= 3): 
                xc = xc - 2
                yc = yc - 2
            if (depth_frame[xc, yc] < 7):
                return (depth_frame[xc, yc]/7)
    return 0.2



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

def cook_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="CookObject",
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
                fillLiquid="water",
                forceAction=False
                )
                event = controller.step(
                action="EmptyLiquidFromObject",
                objectId= picked_up_object_id,
                forceAction=False
                )
                break
                



def on_press(key):
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
        elif key.char == 'v':
            object_id = cook_action()
            if object_id:
                sequence.append("Cook " + object_id)
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
              
        event = controller.last_event
        frame = event.frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        frame_path = os.path.join('frames', f'frame_{current_time}.jpg')
        cv2.imwrite(os.path.join('frames', f'frame_{current_time}.jpg'), frame_rgb)
        file_name = os.path.splitext(frame_path)[0]
        text_file_path = file_name + '.txt'
        
        for obj_name, bounding_box in event.instance_detections2D.items():
            split_string = obj_name.split('|')
            obj_type = split_string[0]
            event = controller.last_event
            for obj in event.metadata["objects"]:
                if obj["objectId"] == obj_name:                   
                    if obj["isCooked"] == True:
                        obj_type = obj_type + "_cooked"
                    if obj["isFilledWithLiquid"] == True:
                        obj_type = obj_type + "_filled"
                    if obj["isSliced"] == True or "Sliced" in obj["objectId"]or "Cracked" in obj["objectId"]:
                        obj_type = obj_type + "_sliced"
                    if obj["isOpen"] == True:
                        obj_type = obj_type + "_opened"
                    break
            
            depth_frame = event.depth_frame
            x_mean = round(float((bounding_box[0] + bounding_box[2])) / 1440, 7)
            y_mean = round(float((bounding_box[1] + bounding_box[3])) / 1440, 7)
            x_diff = round(float(bounding_box[2] - bounding_box[0])/720, 7)
            y_diff = round(float(bounding_box[3] - bounding_box[1])/720, 7)
            depth = get_depth_value(x_mean, y_mean, depth_frame)
            
            if (depth <= 0.33) and (x_diff >= 0.037 or y_diff >= 0.037):
                print(obj_type)
                obj_id = object_dict.get(obj_type)
                if obj_id != None:
                    text_content = f"{obj_id} {x_mean} {y_mean} {x_diff} {y_diff}"
                    with open(text_file_path, 'a+') as text_file:
                        text_file.write(text_content + '\n')
            
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')
    if key == keyboard.Key.esc:  # Stop listener on pressing escape key
        with open('sequence.txt', 'w') as file:
            if sequence:
                for action in sequence:
                    file.write(action + '\n')
        return False
 
def delete_previous_frames():
    for filename in os.listdir("frames"):
        file_path = os.path.join("frames", filename)
        os.remove(file_path)
    
if __name__ == "__main__":
    
    ################################################# Can be used to collect data of a certain state of an object ##############################################
    # controller.step(action='SetObjectStates', SetObjectStates={'objectType': 'WineBottle', 'stateChange': 'canFillWithLiquid', 'isFilledWithLiquid': False})
    # controller.step(action='SetObjectStates', SetObjectStates={'objectType': 'Egg', 'stateChange': 'sliceable', 'isSliced': True})
    # controller.step(action='SetObjectStates', SetObjectStates={'objectType': 'Egg', 'stateChange': 'cookable', 'isCooked': True})   
    # controller.step(action='SetObjectStates', SetObjectStates={'objectType': 'Drawer', 'stateChange': 'openable', 'isOpen': True})
    # controller.step(action='SetObjectStates', SetObjectStates={'objectType': 'Book', 'stateChange': 'canFillWithLiquid', 'isFilledWithLiquid': True})  
    ############################################################################################################################################################
     
    sequence = []
    
    delete_previous_frames()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  
    event = controller.last_event
    
    # json_data = json.dumps(event.metadata)
    # with open("metadata.json", "w") as json_file:
    #     json_file.write(json_data)
        
    # depth_data = event.depth_frame[360][360]
    # np.savetxt('depth_data.txt', depth_data, fmt='%.6f')
    