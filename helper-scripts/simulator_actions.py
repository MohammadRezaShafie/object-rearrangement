import tkinter as tk

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

def fill_action():
    object_id = get_object_in_frame()
    event = controller.step(
    action="FillObjectWithLiquid",
    objectId= object_id,
    fillLiquid="water",
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