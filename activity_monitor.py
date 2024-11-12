import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import json
from collections import defaultdict

# MQTT Configuration
MQTT_BROKER = "192.168.1.114"
MQTT_PORT = 1883
MQTT_TOPIC = "gaming/monitor"

# Data structure to store current process data
current_process_data = defaultdict(dict)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    pc_id = data['pc_id']
    
    for process in data.get('processes', []):
        if process['cpu_percent'] > 1:  # Only consider processes using more than 1% CPU
            current_process_data[pc_id][process['name']] = process['cpu_percent']
        elif process['name'] in current_process_data[pc_id]:
            del current_process_data[pc_id][process['name']]  # Remove process if it drops below 1%
    
    app.update_charts()

# MQTT Client setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

class ProcessMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Monitor")
        self.geometry("800x600")
        self.charts = {}
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.update_charts()

    def update_charts(self):
        for pc_id, processes in current_process_data.items():
            if pc_id not in self.charts:
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=pc_id)
                fig, ax = plt.subplots()
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                self.charts[pc_id] = (fig, ax, canvas)
            
            fig, ax, canvas = self.charts[pc_id]
            ax.clear()
            
            process_names = list(processes.keys())
            cpu_percents = list(processes.values())
            
            ax.barh(process_names, cpu_percents)
            
            ax.set_title(f'Current CPU Usage for {pc_id}')
            ax.set_xlabel('CPU %')
            ax.set_ylabel('Process')
            ax.tick_params(axis='y', labelsize=8)  # Set smaller font size for process labels
            canvas.draw()

# Initialize and run the app
app = ProcessMonitorApp()
app.mainloop()
