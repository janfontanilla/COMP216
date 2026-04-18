import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json
import smtplib
from email.mime.text import MIMEText
import threading
from group_3_util import Util

# SMTP Config
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587
USER_NAME = 'mohammadbaig.centennial@gmail.com' 
PASSWORD = 'gzriiybcrzagtsny'  
RECPT_EMAIL = 'mbaig77@my.centennialcollege.ca'

class SubscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 3 - Medical Monitor & Alerts")
        self.util = Util()
        self.last_id = None
        
        # Handle multiple lines being graphed
        self.hr_history = [] 
        self.rr_history = [] # Respiratory rate history
        self.max_history_len = 20

        # UI Setup: Subscriber GUI
        self.canvas_width, self.canvas_height = 600, 300
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)
        
        # Legend for multiple lines
        tk.Label(root, text="Legend: BLUE = Heart Rate (bpm) | RED = Respiratory Rate (breaths/min)", font=('Arial', 9)).pack()
        
        self.info_label = tk.Label(root, text="Waiting for connection...", font=('Arial', 12, 'bold'))
        self.info_label.pack(pady=5)

        self.alert_log = tk.Text(root, height=6, width=70, fg="red")
        self.alert_log.pack(pady=10)

        # MQTT Setup
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        
        try:
            self.client.connect("broker.emqx.io", 1883, 60)
            self.client.loop_start()
        except Exception as e:
            messagebox.showerror("Broker Error", f"Unable to connect to broker: {e}")

    # MQTT Callbacks 
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.log_alert("System: Connected to broker successfully.", color="green")
            # Handle multiple publishers/subscribers by using a specific topic
            self.client.subscribe("group3/vitals")
        else:
            self.log_alert(f"System: Connection failed! Code: {reason_code}")

    def on_subscribe(self, client, userdata, mid, reason_codes, properties):
        self.info_label.config(text="Subscribed to topic 'group3/vitals'. Waiting for data...")

    def on_message(self, client, userdata, msg):
        """Decode the message and decide how to process it"""
        try:
            data = json.loads(msg.payload.decode())
            
            # Detect missing transmission
            if self.last_id and data['id'] != self.last_id + 1:
                self.log_alert(f"MISSING DATA ALERT: Expected ID {self.last_id + 1}, received {data['id']}")
            self.last_id = data['id']

            # Detecting out-of-range (erroneous) data
            if data['heart_rate'] < 30 or data['body_temperature'] > 105:
                self.log_alert(f"CRITICAL VITAL: Temp {data['body_temperature']}°F, HR {data['heart_rate']} bpm!")
                # SMTP functionality via background thread
                threading.Thread(target=self.send_email_alert, args=(data,), daemon=True).start()

            # Manage history lists
            self.hr_history.append(data['heart_rate'])
            self.rr_history.append(data['respiratory_rate'])
            if len(self.hr_history) > self.max_history_len:
                self.hr_history.pop(0)
                self.rr_history.pop(0)

            # Update GUI safely from main thread
            self.root.after(0, self.update_ui, data)
        except json.JSONDecodeError:
            self.log_alert("Error: Received malformed JSON data.")

    # UI & Graphics Logic
    def log_alert(self, msg, color="red"):
        self.alert_log.insert(tk.END, f"{msg}\n")
        self.alert_log.see(tk.END)

    def update_ui(self, data):
        self.info_label.config(text=f"Patient: {data['patient']['name']} | HR: {data['heart_rate']} | Resp: {data['respiratory_rate']} | Temp: {data['body_temperature']}°F")
        self.draw_chart()

    def draw_chart(self):
        """Dynamic X and Y axis mapping & Multiple lines"""
        self.canvas.delete("all")
        if not self.hr_history: return

        # Combine arrays to find dynamic global min/max for the Y-axis
        all_vals = self.hr_history + self.rr_history
        min_val, max_val = min(all_vals) - 10, max(all_vals) + 10
        if min_val == max_val: max_val += 1 # Prevent division by zero
        
        # Draw dynamic Y-axis bounds
        self.canvas.create_text(20, 10, text=str(int(max_val)), fill="gray")
        self.canvas.create_text(20, self.canvas_height - 10, text=str(int(min_val)), fill="gray")

        # Calculate dynamic X step
        x_step = self.canvas_width / (self.max_history_len - 1)

        # Plot Heart Rate (Blue Line) & Respiratory Rate (Red Line)
        for i in range(len(self.hr_history) - 1):
            x1 = i * x_step
            x2 = (i + 1) * x_step
            
            # Dynamic Y mapping: Map value to pixel height
            y1_hr = self.canvas_height - ((self.hr_history[i] - min_val) / (max_val - min_val) * self.canvas_height)
            y2_hr = self.canvas_height - ((self.hr_history[i+1] - min_val) / (max_val - min_val) * self.canvas_height)
            self.canvas.create_line(x1, y1_hr, x2, y2_hr, fill="blue", width=2)

            y1_rr = self.canvas_height - ((self.rr_history[i] - min_val) / (max_val - min_val) * self.canvas_height)
            y2_rr = self.canvas_height - ((self.rr_history[i+1] - min_val) / (max_val - min_val) * self.canvas_height)
            self.canvas.create_line(x1, y1_rr, x2, y2_rr, fill="red", width=2, dash=(4, 2))

    # SMTP Service
    def send_email_alert(self, data):
        try:
            msg = MIMEText(f"Emergency Alert\n\nPatient: {data['patient']['name']}\nMessage ID: {data['id']}\nHeart Rate: {data['heart_rate']}\nTemp: {data['body_temperature']}°F\nStatus: OUT OF RANGE")
            msg['Subject'] = f"IoT Medical Alert - ID {data['id']}"
            msg['From'] = USER_NAME
            msg['To'] = RECPT_EMAIL
            
            server = smtplib.SMTP(SMTP_SERVER, PORT)
            server.starttls() # Secure the connection
            server.login(USER_NAME, PASSWORD)
            server.send_message(msg)
            server.quit()
            
            # Uses after() to update UI safely from thread
            self.root.after(0, self.log_alert, f"SMTP: Gmail Alert sent to {RECPT_EMAIL}", "green")
        except smtplib.SMTPAuthenticationError:
            self.root.after(0, self.log_alert, "SMTP Error: Gmail Authentication Failed (Check App Password)")
        except Exception as e:
            self.root.after(0, self.log_alert, f"SMTP Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriberGUI(root)
    root.mainloop()
