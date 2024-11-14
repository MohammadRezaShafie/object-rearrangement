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


### This script opens a scene in the simulator and finds the essential properties used for relation graph construction

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



if __name__ == "__main__":
    controller.step(
    action="MoveAhead",
    moveMagnitude=None
)
    event = controller.last_event
    slicable_objects = set()
    cookable_objects = set()
    openable_objects = set()
    fillable_objects = set()

    for obj in event.metadata["objects"]:
        obj_name = obj["objectType"]

        if obj.get("sliceable", False):
            slicable_objects.add(obj_name)

        if obj.get("cookable", False):
            cookable_objects.add(obj_name)

        if obj.get("openable", False):
            openable_objects.add(obj_name)

        if obj.get("canFillWithLiquid", False):
            fillable_objects.add(obj_name)

    print("Slicable Objects:", list(slicable_objects))
    print("Cookable Objects:", list(cookable_objects))
    print("Openable Objects:", list(openable_objects))
    print("Fillable Objects:", list(fillable_objects))

        
        
        