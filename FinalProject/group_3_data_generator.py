import json
import random
from time import asctime

class Util:
    def __init__(self):
        self.start_id = 100
        self.patient = {'name': 'John Doe', 'room': '204B'}
 
    def create_data(self) -> dict:
        """Generates realistic patient vitals using Gaussian distribution."""
        self.start_id += 1
        return {
            'id': self.start_id,
            'patient': self.patient,
            'time': asctime(),
            'heart_rate': int(random.gauss(75, 5)),
            'respiratory_rate': int(random.gauss(16, 2)),
            'heart_rate_variability': int(random.gauss(50, 10)),
            'body_temperature': round(random.gauss(98.6, 0.5), 1),
            'blood_pressure': {
                'systolic': int(random.gauss(120, 10)),
                'diastolic': int(random.gauss(80, 5))
            },
            'activity': random.choice(['Resting', 'Sleeping', 'Walking'])
        }

    def mutate_data(self, data: dict) -> dict:
        """Intentionally corrupts data for testing anomaly detection."""
        # Simulate a sensor error (extremely high temperature or negative heart rate)
        data['heart_rate'] = -1 
        data['body_temperature'] = 115.0
        return data

    @staticmethod
    def print_data(data):
        print(f"[{data['id']}] {data['time']} | HR: {data['heart_rate']} | Temp: {data['body_temperature']}°F")
