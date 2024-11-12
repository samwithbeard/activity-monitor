import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import json
from collections import defaultdict, deque
import time

# MQTT Configuration
MQTT_BROKER = "192.168.1.114"
MQTT_PORT = 1883
MQTT_TOPIC = "gaming/monitor"

# Data structure to store current and historical process data
current_process_data = defaultdict(dict)
historical_process_data = defaultdict(lambda: defaultdict(lambda: deque(maxlen=20)))

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    pc_id = data['pc_id']
    timestamp = time.time()
    
    for process in data.get('processes', []):
        if process['cpu_percent'] > 1:  # Only consider processes using more than 1% CPU
            current_process_data[pc_id][process['name']] = process['cpu_percent']
            historical_process_data[pc_id][process['name']].append((timestamp, process['cpu_percent']))
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
        self.geometry("1000x800")
        self.charts = {}
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.update_charts()

    def update_charts(self):
        for pc_id, processes in current_process_data.items():
            if pc_id not in self.charts:
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=pc_id)
                
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                self.charts[pc_id] = (fig, ax1, ax2, canvas, None)
                
                def on_click(event):
                    legend = self.charts[pc_id][4]
                    if legend is not None:
                        legend.set_visible(not legend.get_visible())
                        canvas.draw()
                
                canvas.mpl_connect("button_press_event", on_click)
            
            fig, ax1, ax2, canvas, _ = self.charts[pc_id]
            ax1.clear()
            ax2.clear()
            
            # Plot historical data as area chart
            for process_name, data in historical_process_data[pc_id].items():
                timestamps, cpu_percents = zip(*data)
                ax1.fill_between(timestamps, cpu_percents, label=process_name, alpha=0.5)
            
            ax1.set_title(f'Historical CPU Usage for {pc_id}')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('CPU %')
            legend = ax1.legend(loc='upper right', fontsize='small')
            legend.set_visible(False)  # Hide the legend initially
            self.charts[pc_id] = (fig, ax1, ax2, canvas, legend)
            
            # Plot current CPU usage as bar chart
            process_names = list(processes.keys())
            cpu_percents = list(processes.values())
            
            ax2.barh(process_names, cpu_percents)
            
            ax2.set_title(f'Current CPU Usage for {pc_id}')
            ax2.set_xlabel('CPU %')
            ax2.set_ylabel('Process')
            ax2.tick_params(axis='y', labelsize=8)  # Set smaller font size for process labels
            
            canvas.draw()

# Initialize and run the app
app = ProcessMonitorApp()
app.mainloop()
