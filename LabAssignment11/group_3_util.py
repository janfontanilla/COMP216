import os
import threading
# import paho.mqtt.client as mqtt #commented out to run main, uncomment when adding other components
import json
import random
from time import asctime   # returns current date/time as a readable string
from json import dumps, loads

class Util:
    def __init__(self):
        # start_id is a sequence counter — each new payload gets the next number.
        self.start_id = 111
 
        # Static patient info that will be embedded in every payload.
        # Kept here so both create_data() and the publisher share the same source.
        self.patient = {'name': 'John Doe', 'room': '204B'}
 
    def create_data(self) -> dict:
        """Build and return one payload dict representing a snapshot of patient vitals.
 
        Each call increments the ID so messages can be ordered/tracked.
        Vital signs use random.gauss(mean, std_dev) to simulate realistic
        fluctuation around a healthy baseline.
        """
        # Bump the ID before building the dict so the very first call gives 112.
        self.start_id += 1
 
        data = {
            'id': self.start_id,                        # sequential message number
            'patient': self.patient,                    # who this reading belongs to
            'time': asctime(),                          # human-readable timestamp
 
            # Vitals — gauss(mean, std_dev) keeps values near a realistic baseline.
            # int() truncates the float so we get whole-number readings.
            'heart_rate': int(random.gauss(80, 1)),             # normal resting ~60-100 bpm
            'respiratory_rate': int(random.gauss(12, 2)),       # normal ~12-20 breaths/min
            'heart_rate_variability': int(random.gauss(65, 5)), # higher HRV = healthier            
            'body_temperature': round(random.gauss(99, 0.5), 2),# round() keeps temperature to 2 decimal places (e.g. 98.76 °F)
 
            # Blood pressure is a nested dict because it has two related sub-values.
            # json.dumps() handles it automatically.
            'blood_pressure': {
                'systolic': int(random.gauss(105, 2)),   
                'diastolic': int(random.gauss(70, 1))    
            },
 
            # Randomly pick an activity to simulate a changing patient state.
            'activity': random.choice(['Resting', 'Walking', 'Sleeping'])
        }
        return data
 
    def print_data(self, data: dict) -> None:
        """Print each field of a payload dict in a labelled, human-readable format.
 
        Called by the Subscriber each time a message is received.
        Accepts the dict directly — the subscriber must json.loads() the raw
        message string before passing it here.
        """
        print(f"  Record ID       : {data['id']}")
        print(f"  Patient         : {data['patient']['name']} (Room {data['patient']['room']})")
        print(f"  Time            : {data['time']}")
        print(f"  Heart Rate      : {data['heart_rate']} bpm")
        print(f"  Respiratory Rate: {data['respiratory_rate']} breaths/min")
        print(f"  HRV             : {data['heart_rate_variability']} ms")
        print(f"  Body Temperature: {data['body_temperature']} °F")
        # Blood pressure is a nested dict, so we drill into it with two keys.
        print(f"  Blood Pressure  : {data['blood_pressure']['systolic']} / "
              f"{data['blood_pressure']['diastolic']} mmHg")
        print(f"  Activity        : {data['activity']}")
        print("=" * 40)
 
 
# This block only runs when you execute this file directly (e.g. python group_1_util.py).
# Will NOT run when the Publisher or Subscriber import this file — that's what
# "if __name__ == '__main__'" guards against. Just for quickly testing this
# component in isolation without needing the full MQTT setup.
if __name__ == '__main__':
    util = Util()
    for _ in range(3):
        payload = util.create_data()  # generate a fake vitals reading
        util.print_data(payload)      # display it
        print()
