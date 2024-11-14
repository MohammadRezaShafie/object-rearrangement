# Object Rearrangement in Dynamic Environments

This project automates the task of object rearrangement in a robotic simulation environment. By integrating object detection, scene navigation, and task planning, this project aims to create an efficient system for arranging objects based on predefined sequences and conditions in a simulated robotic environment.

## 📝 Table of Contents
- Features
- Prerequisites
- Problem Description
- Methodology
- Usage
- Project Structure
- Performance Analysis
- License

## ✨ Features
- **Dataset Collection**: Collects and saves bounding box data for detected objects and tracks object properties.
- **Robotic Scene Navigation**: A script dedicated to navigating through the simulated environment, adjusting object positions and states to prepare for future tasks.
- **Object Detection**: Utilizes YOLOv5 for accurate object detection with a custom detection pipeline adapted for specific task needs.
- **Task Management**: Automates and plans object rearrangement tasks within a sequence.
- **Flexible Action Handling**: Defines a set of basic actions for manipulating objects within the simulator.
- **Relation Graph Construction**: Builds a graph of object relationships to help with decision-making in rearrangement tasks.

## ✅ Prerequisites
Before running this project, ensure you have:
- **Python 3.7+**
- **PyTorch**: Required for YOLOv5 model inference.
- **OpenCV**: For image processing and handling video frames.
- **NumPy**: For numerical operations.
- **Matplotlib**: For data visualization.
  
### How to Set Up the Project
1. **Clone the YOLOv5 Repository**:
   This project relies on YOLOv5, so make sure to clone the official YOLOv5 repository first from [YOLOv5 GitHub Repository](https://github.com/ultralytics/yolov5).
   
   ```bash
   git clone https://github.com/ultralytics/yolov5
   ```

2. **Copy This Repository's Contents**:
   After cloning the YOLOv5 repository, copy the contents of this repository into the folder where YOLOv5 is located.
3. **Install Dependencies**:
   After cloning both repositories and copying the files, install the required dependencies for YOLOv5. In the terminal, navigate to the YOLOv5 folder and run:
   
   ```bash
   pip install -U -r requirements.txt
   ```

## 🧩 Problem Description
The problem addressed by this project involves automating the process of detecting and rearranging objects in a robotic system. The task is to detect objects within a scene, analyze their properties, and execute a sequence of actions to manipulate the scene to meet predefined goals. This includes not only detecting objects but also optimizing the sequence of tasks and actions to be performed in the simulation.

Key components of the project include:
- **Object Detection**: Detect objects in frames using the YOLOv5 model.
- **Scene Navigation**: Move objects around the scene and adjust their states to prepare for the next task.
- **Sequence Planning**: Plan and execute tasks by determining the optimal sequence of object manipulations.


## 🔍 Methodology

### Object Detection
The **YOLOv5** model is used for object detection in the given scene. The **`custom_detect.py`** script modifies the original `detect.py` from YOLOv5 to tailor it for this project. It uses the custom-trained weights (**`task_model.pt`**) for detecting objects in the environment and saves the detection results in two folders: **`detections_1`** and **`detections_2`**.

### Scene Navigation and Object Rearrangement
The **`scene_navigator.py`** script enables the manipulation of the scene by navigating through the objects and adjusting their positions and states. This script is essential for setting up the environment in such a way that the rearrangement tasks can be completed.

### Dataset Collection and Bounding Box Analysis
The **`bounding_box_plotter.py`** script is responsible for collecting data by saving the bounding box coordinates of objects in each frame after performing actions in the simulator. This tool also allows the agent to ignore objects outside the frame or far from the agent, ensuring that only relevant objects are processed.

### Task Planning and Sequence Management
The **`sequence_planner.py`** script is used for planning the sequence of actions required to rearrange the objects in the desired way. It interacts with the **`relation_graph.py`**, which constructs a graph of object relationships to help plan and execute tasks efficiently.

### Relation Graph Construction
The **`find_object_properties.py`** script extracts essential properties of the objects in the scene, which are used to build a relation graph. This graph helps in decision-making when planning tasks, taking into account how objects are related to one another in the context of the scene.

## 💡 Usage

### Running the Project
1. **Define Initial and Goal States**: Use the `scene_navigator.py` to set the initial state of the scene and define the goal state. Then run the script again for both the pre-change and post-change scenes. The agent will naviagte the scene in the pre-defined route and saves frames of both scenes.
2. **Object Detection**: Run the `final_detection.py` script to perform object detection of all frames using the custom YOLOv5 model and save their results in detection folders.
3. **Scene Navigation**: Run the 'rearrangement_task_manager.py' script to perfrorm object rearrangement within the scene.


## 📁 Project Structure

```
/Object-Rearrangement-Task-Planning

├── models
       ├── first_dataset_model.pt
       ├── second_dataset_model.pt
       ├── task_model.pt

├── dataset-collection-tools
       ├── bounding_box_plotter.py
       ├── find_object_properties.py

├── helper-scripts
       ├── calculate_best_associated_frames.py
       ├── scene_navigator.py
       ├── simulator_actions.py

├── pred-defined-paths
       ├── sequence.txt
       ├── sequence_ground_truth.txt
       ├── sequence_with_tasks.txt

├── scenes-metadata
       ├── scene-metadata.json

├── LICENSE
├── README.md

├── custom_detect.py
├── final_detection.py
├── find_difference_between_frames.py
├── rearrangement_task_manager.py
├── relation_graph.py
├── sequence_planner.py
├── set_objects_position.py
└── README.md
```

### Folder and File Descriptions:

- **models/**: Contains the pre-trained models (`first_dataset_model.pt`, `second_dataset_model.pt`, `task_model.pt`) for object detection.
- **dataset-collection-tools/**: Includes scripts for collecting bounding box data and finding object properties during scene interactions.
- **helper-scripts/**: Contains utility scripts for calculating frame associations, scene navigation, and defining simulator actions.
- **pred-defined-paths/**: Stores predefined paths like `sequence.txt`, `sequence_ground_truth.txt`, and `sequence_with_tasks.txt` for sequence planning.
- **scenes-metadata/**: Contains metadata for the scenes, stored in `scene-metadata.json`.
- **custom_detect.py**: A modified version of YOLOv5's `detect.py` used for the specific detection tasks in this project.
- **final_detection.py**: Runs the object detection over a sequence of frames and stores the results.
- **find_difference_between_frames.py**: Compares changes between frames of pre-change and post-change scenes for task tracking and analysis.
- **rearrangement_task_manager.py**: Coordinates and manages the rearrangement tasks for the objects in the scene.
- **relation_graph.py**: Builds and maintains a graph of object relationships, used for planning tasks based on object properties.
- **sequence_planner.py**: Plans and organizes the sequence of actions for object rearrangement.
- **set_objects_position.py**: Defines the positions of objects within the simulator based on a previous metadata.


## 📊 Performance Analysis
**The performance of the algorithm has not been tested for rearrangement tasks, yet.** However, in order to evaluate the model’s effectiveness in detecting and tracking object relocation, an experiment was conducted using the AI2-THOR simulation environment. The experiment involved 9 randomly generated scenes and a default scene, with each scene containing between 60 and 80 objects. In total, 614 objects across all scenes were examined to determine whether they had been relocated. The intelligent agent followed a fixed route through each environment, comparing all 9 scenes against the default scene.
### Performance Metrics
The performance metrics for the object relocation tracking algorithm of this experiment were as follows:

| Metric      | Value    |
|-------------|----------|
| **Precision** | 95.8%   |
| **Recall**    | 96.8%   |
| **Accuracy**  | 97.7%   |

The results demonstrate the effectiveness of the best-associated frame selection algorithm in detecting spatial changes in the scene. The high precision, recall, and accuracy indicate that the algorithm is highly reliable in tracking object relocations with minimal false positives and false negatives.

## 📝 License
This project uses the YOLOv5 model, which is licensed under the [GPL-3.0 License](https://opensource.org/licenses/GPL-3.0). For more information on the YOLOv5 license and usage, please refer to the official [YOLOv5 GitHub repository](https://github.com/ultralytics/yolov5).

