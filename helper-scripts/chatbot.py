import google.generativeai as genai
import os
import time
import re
from datetime import datetime

# Create conversation histories directory if it doesn't exist
CONVERSATION_HISTORIES_DIR = "conversation_histories"
if not os.path.exists(CONVERSATION_HISTORIES_DIR):
    os.makedirs(CONVERSATION_HISTORIES_DIR)

# Generate filename with current date and time
def get_conversation_history_file():
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(CONVERSATION_HISTORIES_DIR, f"conversation_history_{current_date}.txt")

# Use a session-based filename (created once per session)
CONVERSATION_HISTORY_FILE = get_conversation_history_file()

def load_background_context():
    """
    Load background context from file.
    """
    context_file = os.path.join(os.path.dirname(__file__), "background_context.txt")
    try:
        with open(context_file, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return """You are an AI assistant that helps with scene navigation in a virtual environment. 
Available commands: move ahead, move back, move left, move right, rotate left, rotate right, look up, look down, pickup, drop."""

def load_conversation_history():
    """
    Load conversation history from file.
    """
    if os.path.exists(CONVERSATION_HISTORY_FILE):
        with open(CONVERSATION_HISTORY_FILE, 'r', encoding='utf-8') as file:
            return file.read()
    return ""

def save_conversation_history(history):
    """
    Save conversation history to file.
    """
    with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as file:
        file.write(history)

def append_to_conversation_history(text):
    """
    Append text to conversation history file.
    """
    with open(CONVERSATION_HISTORY_FILE, 'a', encoding='utf-8') as file:
        file.write(text + "\n")

def clear_conversation_history():
    """
    Clear the conversation history file.
    """
    if os.path.exists(CONVERSATION_HISTORY_FILE):
        os.remove(CONVERSATION_HISTORY_FILE)
        print("Conversation history cleared.")
    else:
        print("No conversation history file found.")

def get_api_key():
    """
    Retrieve API key from file, or prompt user if not found.
    """
    api_key_file = os.path.join(os.path.dirname(__file__), "api_key.txt")
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    else:
        api_key = input("Enter your Google Generative AI API key: ").strip()
        with open(api_key_file, 'w', encoding='utf-8') as f:
            f.write(api_key)
        return api_key

def send_to_chatbot_api(user_input, use_history=True):
    """
    Sends user input to the Google Generative AI API and retrieves the response.
    Maintains conversation history in a file.
    """
    api_key = get_api_key()
    genai.configure(api_key=api_key)

    try:
        # Load conversation history
        conversation_history = ""
        if use_history:
            conversation_history = load_conversation_history()
        
        # Add background context for scene navigation (only if history is empty)
        if use_history and not conversation_history.strip():
            background_context = load_background_context()
            append_to_conversation_history(f"System: {background_context}")
            conversation_history = load_conversation_history()
        
        # Limit conversation history to avoid API limits (keep last 10 exchanges)
        if use_history and conversation_history:
            lines = conversation_history.strip().split('\n')
            if len(lines) > 20:  # Keep system message + last 19 lines (about 10 exchanges)
                lines = lines[:1] + lines[-19:]  # Keep first line (system) + last 19
                conversation_history = '\n'.join(lines)
                save_conversation_history(conversation_history)
        
        # Append user input to history
        if use_history:
            append_to_conversation_history(f"User: {user_input}")
            conversation_history = load_conversation_history()
        
        # For navigation commands, use background context + direct approach
        background_context = load_background_context()
        direct_navigation_prompt = f"""{background_context}
                                    The user said: "{user_input}"
                                    Respond with the appropriate action command from these options, KEEPING ANY NUMBERS OR DEGREES:
                                    - move ahead (or move forward) - add number if specified (e.g., "move ahead 5")
                                    - move back - add number if specified  
                                    - move left - add number if specified
                                    - move right - add number if specified
                                    - rotate left (or turn left) - add number or degrees if specified (e.g., "rotate left 90 degrees")
                                    - rotate right (or turn right) - add number or degrees if specified
                                    - look up - add number if specified (each counts as one look increment)
                                    - look down - add number if specified (each counts as one look increment)
                                    - pickup (for picking up objects)
                                    - drop (for dropping objects)

                                    IMPORTANT: If the user specifies a number or degrees, include it in your response.
                                    Examples:
                                    - User: "move forward 3 steps" → Response: "move ahead 3"
                                    - User: "rotate left 90 degrees" → Response: "rotate left 90 degrees"
                                    - User: "look up 2" → Response: "look up 2"
                                    - User: "turn right 5" → Response: "rotate right 5"

                                    Just respond with the action command including any numbers, nothing else."""
                                            
        # Always use direct prompt for better reliability with numbers/degrees
        prompt = direct_navigation_prompt
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Append AI response to history
        if use_history:
            append_to_conversation_history(f"Assistant: {response.text}")
        
        return response.text
    except Exception as e:
        print(f"Error communicating with Google Generative AI API: {e}")
        # Fallback: try without history
        if use_history:
            print("Retrying without conversation history...")
            return send_to_chatbot_api(user_input, use_history=False)
        return None

def handle_chatbot_command(command, controller):
    """
    Maps chatbot commands to scene navigation actions.
    Handles multiple steps, degrees, and compound commands with step-by-step execution.
    """
    command = command.lower().strip()
    
    # Handle compound commands (separated by "then", "and", "after", etc.)
    compound_separators = [" then ", " and ", " after that ", " next "]
    commands = [command]
    
    for separator in compound_separators:
        if separator in command:
            commands = command.split(separator)
            break
    
    results = []
    
    for single_command in commands:
        single_command = single_command.strip()
        result = execute_single_command(single_command, controller)
        results.append(result)
        time.sleep(0.5)  # Brief pause between compound commands
    
    return " | ".join(results)

def execute_single_command(command, controller):
    """
    Execute a single navigation command.
    """
    # Extract numbers from command
    numbers = re.findall(r'\d+', command)
    
    # Rotation commands first - handle both steps and degrees (check these BEFORE movement)
    if "rotate left" in command or "turn left" in command:
        if "degree" in command:
            # Convert degrees to steps (10 degrees per step)
            degrees = int(numbers[0]) if numbers else 10
            steps = max(1, degrees // 10)
            # Limit maximum steps to prevent infinite loops
            steps = min(steps, 36)  # Max 360 degrees
        else:
            steps = int(numbers[0]) if numbers else 1
            steps = min(steps, 36)  # Max 36 steps
        return execute_multiple_rotations(controller, "RotateLeft", steps, "Rotated left")
    elif "rotate right" in command or "turn right" in command:
        if "degree" in command:
            # Convert degrees to steps (10 degrees per step)
            degrees = int(numbers[0]) if numbers else 10
            steps = max(1, degrees // 10)
            # Limit maximum steps to prevent infinite loops
            steps = min(steps, 36)  # Max 360 degrees
        else:
            steps = int(numbers[0]) if numbers else 1
            steps = min(steps, 36)  # Max 36 steps
        return execute_multiple_rotations(controller, "RotateRight", steps, "Rotated right")
    
    # Movement commands (check these AFTER rotation to avoid conflicts)
    elif any(phrase in command for phrase in ["move ahead", "go forward", "move forward"]) or (command == "forward" or command == "ahead"):
        steps = int(numbers[0]) if numbers else 1
        return execute_multiple_steps(controller, "MoveAhead", steps, "Moved forward")
    elif any(phrase in command for phrase in ["move back", "go back", "move backward"]) or (command == "backward" or command == "back"):
        steps = int(numbers[0]) if numbers else 1
        return execute_multiple_steps(controller, "MoveBack", steps, "Moved backward")
    elif any(phrase in command for phrase in ["move left", "go left"]) or command == "left":
        steps = int(numbers[0]) if numbers else 1
        return execute_multiple_steps(controller, "MoveLeft", steps, "Moved left")
    elif any(phrase in command for phrase in ["move right", "go right"]) or command == "right":
        steps = int(numbers[0]) if numbers else 1
        return execute_multiple_steps(controller, "MoveRight", steps, "Moved right")
    
    # Look commands
    elif "look up" in command:
        steps = int(numbers[0]) if numbers else 1
        for _ in range(steps):
            controller.step("LookUp")
            time.sleep(0.1)
        return f"Looked up {steps} time(s)"
    elif "look down" in command:
        steps = int(numbers[0]) if numbers else 1
        for _ in range(steps):
            controller.step("LookDown")
            time.sleep(0.1)
        return f"Looked down {steps} time(s)"
    
    # Object manipulation
    elif any(word in command for word in ["pickup", "pick up", "grab"]):
        try:
            msg = pickup_action(controller)
            return msg
        except Exception as e:
            return f"Failed to pick up object: {e}"
    elif any(word in command for word in ["drop", "put down"]):
        try:
            drop_action(controller)
            return "Dropped object"
        except Exception as e:
            return f"Failed to drop object: {e}"
    
    else:
        return f"Unknown command: {command}"

def execute_multiple_steps(controller, action, steps, message):
    """
    Execute movement commands multiple times with small delays.
    """
    for i in range(steps):
        controller.step(action)
        time.sleep(0.2)  # Small delay between steps to see movement
    return f"{message} {steps} step(s)"

def execute_multiple_rotations(controller, action, rotations, message):
    """
    Execute rotation commands multiple times (10 degrees each) with optimized delays.
    """
    # For large rotations, use shorter delays to prevent infinite loop feeling
    delay = 0.05 if rotations > 10 else 0.1
    
    for i in range(rotations):
        controller.step(action, degrees=10)
        time.sleep(delay)  # Shorter delay for large rotations
    return f"{message} {rotations * 10} degrees ({rotations} step(s))"

def pickup_action(controller):
    # Gather visible objects in frame (center region sampling similar to scene_navigator)
    objects = get_objects_in_frame(controller)
    if not objects:
        info = "No visible objects to pick up"
        append_to_conversation_history(f"System: {info}")
        return info
    # Map object metadata
    event = controller.last_event
    id_map = {o["objectId"]: o for o in event.metadata.get("objects", [])}
    # Choose first pickupable object
    target_id = None
    for oid in objects:
        meta = id_map.get(oid, {})
        if meta.get("pickupable") and not meta.get("isPickedUp"):
            target_id = oid
            break
    if target_id is None:
        target_id = objects[0]
    try:
        controller.step(
            action="PickupObject",
            objectId=target_id,
            forceAction=False,
            manualInteract=False
        )
        info = f"Visible objects: {', '.join(objects)} | Picked up: {target_id}"
    except Exception as e:
        info = f"Visible objects: {', '.join(objects)} | Pickup failed: {e}"
    append_to_conversation_history(f"System: {info}")
    return info

def drop_action(controller):
    controller.step(
        action="DropHandObject",
        forceAction=True
    )

def get_objects_in_frame(controller):
    """Scan the center of the frame and return a list of unique visible objectIds."""
    seen = set()
    # Ensure we have a recent event
    try:
        _ = controller.last_event
    except Exception:
        try:
            controller.step("Pass")
        except Exception:
            return []
    for i in range(10):
        for j in range(10):
            xi = 0.40 + (i / 50.0)
            yi = 0.40 + (j / 50.0)
            try:
                query = controller.step(action="GetObjectInFrame", x=xi, y=yi, checkVisible=False)
                oid = query.metadata.get("actionReturn")
                if oid:
                    seen.add(oid)
            except Exception:
                continue
    return list(seen)

def get_object_in_frame(controller):
    # Deprecated placeholder retained for compatibility
    objs = get_objects_in_frame(controller)
    return objs[0] if objs else None
