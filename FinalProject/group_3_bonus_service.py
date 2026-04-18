import os
import json
import threading
from flask import Flask, jsonify, send_from_directory, render_template_string
from concurrent.futures import ThreadPoolExecutor
from group_3_data_generator import Util

class BonusManagerAPI:
    """
    [Bonus: Implement Flask server as a Class]
    This service acts as the 'Service-level data' logger and export manager.
    """
    def __init__(self, port=5000):
        self.app = Flask(__name__)
        self.port = port
        self.data_log = []
        self.executor = ThreadPoolExecutor(max_workers=4) # Scalable threads
        self.export_dir = "group_3_exports"
        
        # Improve folder creation to avoid OS issues
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            # Responsive UI elements via simple HTML/CSS
            html = """
            <html>
                <head><title>Group 3 IoT Dashboard</title></head>
                <body style="font-family: sans-serif; padding: 20px;">
                    <h1>System Health Dashboard</h1>
                    <p>Total Records Logged: {{ count }}</p>
                    <button onclick="location.href='/export'">Export Data to File</button>
                    <div id="logs"></div>
                </body>
            </html>
            """
            return render_template_string(html, count=len(self.data_log))

        @self.app.route('/api/data')
        def get_data():
            # Inspecting headers/JSON payloads
            return jsonify(self.data_log[-10:]) # Return last 10 records

        @self.app.route('/export')
        def export_action():
            # Leverage background threads for IO-bound tasks
            self.executor.submit(self.save_to_disk)
            return "Exporting process started in background thread..."

    def log_message(self, data):
        """Called by the Subscriber to push data into the Flask system."""
        self.data_log.append(data)
        if len(self.data_log) > 1000: # Memory safeguard
            self.data_log.pop(0)

    def save_to_disk(self):
        """Safeguards for file transfer / OS exceptions]"""
        filename = f"vitals_export_{len(self.data_log)}.json"
        filepath = os.path.join(self.export_dir, filename)
        
        try:
            # Chunking/Scalable writes
            with open(filepath, 'w') as f:
                json.dump(self.data_log, f)
            print(f"Bonus: Successfully exported to {filepath}")
        except OSError as e:
            print(f"OS Error during export: {e}")

    def run(self):
        # Runs Flask in a thread so it doesn't block the main MQTT process
        threading.Thread(target=lambda: self.app.run(port=self.port, debug=False, use_reloader=False)).start()

# --- Integration Logic ---
# To make this work, add these lines to Subscriber's __init__:
# self.bonus_api = BonusManagerAPI()
# self.bonus_api.run()
#
# And add this to the Subscriber's on_message:
# self.bonus_api.log_message(data)