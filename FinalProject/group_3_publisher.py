import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json
import threading
import time
import random
from group_3_data_generator import DataGenerator
from group_3_util import Util

# MQTT client + callbacks
# threading + entry-driven delay

class PublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 3 - IoT Patient Vitals Publisher")

        # default generator — params are editable at runtime from the GUI
        self.generator = DataGenerator()
        self.util = Util(self.generator)
        self.is_running = False
        self.corrupt_next = False

        # MQTT client with v2 callbacks
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

        # UI Setup: Publisher GUI
        tk.Label(root, text="MQTT Publisher Control", font=('Arial', 14, 'bold')).pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Disconnected", fg="red")
        self.status_label.pack()

        # topic entry so multiple publishers can use sub-topics (e.g. group3/vitals/bedA)
        topic_frame = tk.Frame(root)
        topic_frame.pack(pady=5)
        tk.Label(topic_frame, text="Topic:").pack(side="left")
        self.topic_var = tk.StringVar(value="group3/vitals")
        tk.Entry(topic_frame, textvariable=self.topic_var, width=25).pack(side="left")

        self.delay_var = tk.StringVar(value="2.0")
        tk.Label(root, text="Transmission Delay (sec):").pack()
        tk.Entry(root, textvariable=self.delay_var, width=10).pack()

        # parameter interface — change the generator settings while running
        params = tk.LabelFrame(root, text="Generator Parameters")
        params.pack(padx=10, pady=5, fill="x")
        self.param_vars = {
            'base': tk.StringVar(value="80"),              # baseline heart rate
            'amplitude': tk.StringVar(value="8"),          # sine swing
            'period': tk.StringVar(value="30"),            # ticks per cycle
            'noise_std': tk.StringVar(value="1.5"),        # jitter
            'wild_prob': tk.StringVar(value="0.0"),        # spike rate (bonus)
            'skip_block_prob': tk.StringVar(value="0.0"),  # skip-burst rate (bonus)
        }
        for i, (name, var) in enumerate(self.param_vars.items()):
            tk.Label(params, text=name).grid(row=i, column=0, sticky="e", padx=2)
            tk.Entry(params, textvariable=var, width=8).grid(row=i, column=1, padx=2)
        tk.Button(params, text="Apply Params", command=self.apply_params).grid(
            row=len(self.param_vars), column=0, columnspan=2, pady=3)

        # quick toggles for the two bonus behaviours (easier to show on the demo video)
        self.wild_on = tk.BooleanVar(value=False)
        self.skip_on = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Wild values ON", variable=self.wild_on,
                       command=self.toggle_wild).pack()
        tk.Checkbutton(root, text="Skip blocks ON", variable=self.skip_on,
                       command=self.toggle_skip).pack()

        # live readout of the active generator settings — updates on Apply / toggle
        self.params_readout = tk.Label(root, text="", fg="blue", font=('Arial', 9))
        self.params_readout.pack()
        self.refresh_readout()

        tk.Button(root, text="Start Transmission", command=self.start_stream, bg="green", fg="white").pack(pady=5)
        tk.Button(root, text="Stop Transmission", command=self.stop_stream, bg="red", fg="white").pack(pady=5)
        tk.Button(root, text="Inject Wild Value Now", command=self.trigger_corruption, bg="orange").pack(pady=5)

        self.log = tk.Text(root, height=10, width=50)
        self.log.pack(padx=10, pady=10)

    def apply_params(self):
        # rebuild the generator with the values from the entry boxes
        try:
            kwargs = {k: float(v.get()) for k, v in self.param_vars.items()}
            kwargs['period'] = int(kwargs['period'])       # period is a tick count
            self.generator = DataGenerator(**kwargs)
            self.util.generator = self.generator           # swap so start_id keeps counting
            self.log.insert(tk.END, f"System: params applied -> {kwargs}\n")
            self.log.see(tk.END)
            self.refresh_readout()
        except ValueError as e:
            messagebox.showerror("Parameter Error", f"Invalid number: {e}")

    def toggle_wild(self):
        # flip the wild-value rate live, and keep the entry box in sync
        self.generator.wild_prob = 0.02 if self.wild_on.get() else 0.0
        self.param_vars['wild_prob'].set(str(self.generator.wild_prob))
        self.refresh_readout()

    def toggle_skip(self):
        # flip the skip-block rate live, and keep the entry box in sync
        self.generator.skip_block_prob = 0.01 if self.skip_on.get() else 0.0
        self.param_vars['skip_block_prob'].set(str(self.generator.skip_block_prob))
        self.refresh_readout()

    def refresh_readout(self):
        # show the generator's active settings so the demo can prove Apply did something
        g = self.generator
        self.params_readout.config(
            text=f"active: base={g.base} amp={g.amplitude} period={g.period} "
                 f"noise={g.noise_std} wild={g.wild_prob} skip={g.skip_block_prob}")

    # MQTT Callbacks
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.log.insert(tk.END, "System: Connected to Broker successfully.\n")
        else:
            self.log.insert(tk.END, f"System: Connection failed with code {reason_code}\n")

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.log.insert(tk.END, "System: Disconnected from Broker.\n")

    def on_publish(self, client, userdata, mid, reason_codes, properties):
        pass

    def trigger_corruption(self):
        # flag so the next payload gets mutated
        self.corrupt_next = True
        self.log.insert(tk.END, "System: Next payload queued for corruption!\n")
        self.log.see(tk.END)

    def start_stream(self):
        if not self.is_running:
            try:
                self.client.connect("broker.emqx.io", 1883, 60)
                self.client.loop_start()                    # network loop runs in background
                self.is_running = True
                self.status_label.config(text="Status: Connected & Streaming", fg="green")
                threading.Thread(target=self.publish_loop, daemon=True).start()  # keeps GUI responsive
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
        while self.is_running:
            try:
                payload = self.util.create_data()
                if payload is None:
                    # generator said skip this tick — log and move on
                    self.log.insert(tk.END, "System: sensor skip (no data this tick)\n")
                    self.log.see(tk.END)
                    time.sleep(float(self.delay_var.get()))
                    continue

                if self.corrupt_next:
                    payload = self.util.mutate_data(payload)
                    self.corrupt_next = False

                message = json.dumps(payload)
                topic = self.topic_var.get() or "group3/vitals"

                # miss about 1 in every 100 transmissions at random
                if random.random() < 0.01:
                    self.log.insert(tk.END, f"DROPPED ID {payload['id']} (1/100)\n")
                else:
                    self.client.publish(topic, message)
                    self.log.insert(tk.END, f"Published ID: {payload['id']} | HR: {payload['heart_rate']} -> {topic}\n")

                self.log.see(tk.END)
                time.sleep(float(self.delay_var.get()))

            except Exception as e:
                self.log.insert(tk.END, f"Publish Error: {e}\n")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()
