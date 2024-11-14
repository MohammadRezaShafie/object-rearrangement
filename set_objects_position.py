import json

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
