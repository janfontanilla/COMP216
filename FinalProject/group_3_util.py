import random
from time import asctime   # readable date/time string


class Util:
    def __init__(self, generator=None):
        self.generator = generator          # DataGenerator instance (pass in from publisher)
        self.start_id = 111                 # sequence counter — each payload gets the next number
        self.patient = {'name': 'Jan Fontanilla', 'room': '204B'}   # patient info embedded in every payload

    def create_data(self) -> dict:
        # grab the next heart-rate value from the generator
        value = self.generator.random_values()
        if value is None:
            return None                     # sensor offline / skip tick — publisher will not send

        self.start_id += 1                  # bump id so the first call gives 112

        data = {
            'id': self.start_id,
            'patient': self.patient,
            'time': asctime(),              # human-readable timestamp
            'heart_rate': value,            # pattern + noise from DataGenerator
            'respiratory_rate': int(random.gauss(12, 2)),        # normal ~12-20 breaths/min
            'heart_rate_variability': int(random.gauss(65, 5)),  # higher hrv = healthier
            'body_temperature': round(random.gauss(99, 0.5), 2), # 2 decimal places, e.g. 98.76
            'blood_pressure': {
                'systolic': int(random.gauss(105, 2)),
                'diastolic': int(random.gauss(70, 1))
            },
            'activity': random.choice(['Resting', 'Walking', 'Sleeping'])
        }
        return data

    def mutate_data(self, data: dict) -> dict:
        # manual corruption for the wild-value button
        data['heart_rate'] = -1
        data['body_temperature'] = 115.0
        return data

    def print_data(self, data: dict) -> None:
        print(f"  Record ID       : {data['id']}")
        print(f"  Patient         : {data['patient']['name']} (Room {data['patient']['room']})")
        print(f"  Time            : {data['time']}")
        print(f"  Heart Rate      : {data['heart_rate']} bpm")
        print(f"  Respiratory Rate: {data['respiratory_rate']} breaths/min")
        print(f"  HRV             : {data['heart_rate_variability']} ms")
        print(f"  Body Temperature: {data['body_temperature']} °F")
        print(f"  Blood Pressure  : {data['blood_pressure']['systolic']} / "
              f"{data['blood_pressure']['diastolic']} mmHg")
        print(f"  Activity        : {data['activity']}")
        print("=" * 40)


# quick test — only runs when this file is executed directly
if __name__ == '__main__':
    from group_3_data_generator import DataGenerator
    util = Util(DataGenerator())
    for _ in range(3):
        payload = util.create_data()
        if payload is None:
            print("(skip tick)")
            continue
        util.print_data(payload)
        print()
