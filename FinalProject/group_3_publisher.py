import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json
import threading
import time
from group_3_util import Util

class PublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 3 - IoT Patient Vitals Publisher")
        self.util = Util()
        self.is_running = False
        self.corrupt_next = False
        
        # Implements MQTT Client with Error Handling & Callbacks
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

        # UI Setup: Publisher GUI
        tk.Label(root, text="MQTT Publisher Control", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Disconnected", fg="red")
        self.status_label.pack()

        self.delay_var = tk.StringVar(value="2.0")
        tk.Label(root, text="Transmission Delay (sec):").pack()
        tk.Entry(root, textvariable=self.delay_var, width=10).pack()

        # Interface to change parameters / Corrupt data
        tk.Button(root, text="Start Transmission", command=self.start_stream, bg="green", fg="white").pack(pady=5)
        tk.Button(root, text="Stop Transmission", command=self.stop_stream, bg="red", fg="white").pack(pady=5)
        tk.Button(root, text="Corrupt Next Message", command=self.trigger_corruption, bg="orange").pack(pady=5)

        self.log = tk.Text(root, height=10, width=50)
        self.log.pack(padx=10, pady=10)

    # MQTT Callbacks
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.log.insert(tk.END, "System: Connected to Broker successfully.\n")
        else:
            self.log.insert(tk.END, f"System: Connection failed with code {reason_code}\n")

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.log.insert(tk.END, "System: Disconnected from Broker.\n")

    def on_publish(self, client, userdata, mid, reason_codes, properties):
        pass # Optional: log successful message delivery

    # --- Core Logic ---
    def trigger_corruption(self):
        """[Final Project: Corrupt data manually via GUI]"""
        self.corrupt_next = True
        self.log.insert(tk.END, "System: Next payload queued for corruption!\n")
        self.log.see(tk.END)

    def start_stream(self):
        if not self.is_running:
            try:
                # Granular exceptions and safeguards
                self.client.connect("broker.emqx.io", 1883, 60)
                self.client.loop_start() # Start network loop in background
                self.is_running = True
                self.status_label.config(text="Status: Connected & Streaming", fg="green")
                
                # Leverage background threads for IO-bound tasks
                threading.Thread(target=self.publish_loop, daemon=True).start()
            except ConnectionRefusedError:
                messagebox.showerror("Connection Error", "Broker refused connection.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect: {e}")

    def stop_stream(self):
        self.is_running = False
        self.status_label.config(text="Status: Stopped", fg="red")
        self.client.loop_stop()
        self.client.disconnect()

    def publish_loop(self):
        """[Final Project: Get value from generator, package as dict, send data]"""
        while self.is_running:
            try:
                payload = self.util.create_data()
                
                if self.corrupt_next:
                    payload = self.util.mutate_data(payload)
                    self.corrupt_next = False
                
                message = json.dumps(payload)
                self.client.publish("group3/vitals", message)
                
                self.log.insert(tk.END, f"Published ID: {payload['id']} | HR: {payload['heart_rate']}\n")
                self.log.see(tk.END)
                
                # Dynamic sleep based on UI input
                time.sleep(float(self.delay_var.get()))
                
            except Exception as e:
                self.log.insert(tk.END, f"Publish Error: {e}\n")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()
