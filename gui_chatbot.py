#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
import threading

# Add helper-scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'helper-scripts'))

try:
    from chatbot import send_to_chatbot_api, handle_chatbot_command
    from ai2thor.controller import Controller
    CHATBOT_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    CHATBOT_AVAILABLE = False

class AI2ThorChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI2Thor Chatbot Interface")
        self.root.geometry("800x600")
        
        # Store initialization messages
        self.init_messages = []
        
        # Setup UI first
        self.setup_ui()
        
        # Initialize AI2Thor controller after UI is ready
        self.controller = None
        if CHATBOT_AVAILABLE:
            try:
                self.controller = Controller(
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
                self.add_message("System: AI2Thor environment initialized successfully!")
            except Exception as e:
                self.add_message(f"System: Error initializing AI2Thor: {e}")
                self.controller = None
        
    def setup_ui(self):
        # Chat display area
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_window = scrolledtext.ScrolledText(
            self.chat_frame, 
            width=80, 
            height=25, 
            state='normal',
            wrap=tk.WORD
        )
        self.chat_window.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Entry field
        self.entry = tk.Entry(self.input_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind('<Return>', lambda event: self.process_command())
        self.entry.focus()
        
        # Send button
        self.send_button = tk.Button(
            self.input_frame, 
            text="Send", 
            command=self.process_command,
            font=("Arial", 12)
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Clear chat button
        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear Chat",
            command=self.clear_chat
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Status label
        self.status_label = tk.Label(
            self.button_frame,
            text=f"Status: {'Ready' if CHATBOT_AVAILABLE else 'Chatbot unavailable'}",
            fg="green" if CHATBOT_AVAILABLE else "red"
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_message("System: Welcome to AI2Thor Chatbot Interface!")
        if CHATBOT_AVAILABLE:
            self.add_message("System: You can give natural language commands like 'move forward', 'turn left', 'pick up object', etc.")
        else:
            self.add_message("System: Chatbot functionality is not available. Please check imports.")
    
    def add_message(self, message):
        self.chat_window.insert(tk.END, message + "\n")
        self.chat_window.see(tk.END)
        self.root.update()
    
    def clear_chat(self):
        self.chat_window.delete(1.0, tk.END)
        self.add_message("System: Chat cleared.")
    
    def process_command(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
            
        self.entry.delete(0, tk.END)
        self.add_message(f"You: {user_input}")
        
        if not CHATBOT_AVAILABLE:
            self.add_message("AI: Chatbot is not available. Please check the installation.")
            return
        
        # Disable send button during processing
        self.send_button.config(state='disabled')
        self.status_label.config(text="Status: Processing...", fg="orange")
        
        # Process command in a separate thread to avoid blocking UI
        threading.Thread(target=self.process_command_thread, args=(user_input,), daemon=True).start()
    
    def process_command_thread(self, user_input):
        try:
            # Send to chatbot API
            response = send_to_chatbot_api(user_input)
            
            if response:
                # Update UI in main thread
                self.root.after(0, self.add_message, f"AI: {response}")
                
                # Try to execute the command if controller is available
                if self.controller:
                    try:
                        # Execute the command immediately in this thread
                        result = handle_chatbot_command(response.lower(), self.controller)
                        # Update UI with result
                        self.root.after(0, self.add_message, f"System: Command executed successfully! {result}")
                        # Force UI update
                        self.root.after(0, self.root.update)
                    except Exception as e:
                        self.root.after(0, self.add_message, f"System: Error executing command: {e}")
            else:
                self.root.after(0, self.add_message, "AI: Sorry, I couldn't process your request.")
                
        except Exception as e:
            self.root.after(0, self.add_message, f"System: Error: {e}")
        
        finally:
            # Re-enable send button
            self.root.after(0, self.send_button.config, {'state': 'normal'})
            self.root.after(0, self.status_label.config, {'text': 'Status: Ready', 'fg': 'green'})
    
    def run(self):
        try:
            self.root.mainloop()
        finally:
            if self.controller:
                self.controller.stop()

if __name__ == "__main__":
    app = AI2ThorChatbotGUI()
    app.run()
