import math
import random

# based on lab 8 DataGenerator — sine + noise gives "random with a pattern"

class DataGenerator:
    def __init__(self, base=80, amplitude=8, period=30, noise_std=1.5,
                 wild_prob=0.0, skip_block_prob=0.0):
        self.base = base                   # centre of the sine (baseline bpm)
        self.amplitude = amplitude         # how far the sine swings up/down
        self.period = period               # ticks per full cycle
        self.noise_std = noise_std         # random jitter on top of the sine
        self.wild_prob = wild_prob         # chance of a spike (bonus)
        self.skip_block_prob = skip_block_prob   # chance of a sensor-offline burst (bonus)
        self._t = 0                        # tick counter, keeps counting up
        self._skip_left = 0                # ticks left in the current skip burst

    def random_values(self):
        # still inside a skip burst — return None so publisher drops this tick
        if self._skip_left > 0:
            self._skip_left -= 1
            self._t += 1
            return None

        # maybe start a new skip burst (sensor going offline for a few ticks)
        if self.skip_block_prob > 0 and random.random() < self.skip_block_prob:
            self._skip_left = random.randint(5, 15)
            self._t += 1
            return None

        # sine wave + gaussian noise — this is the "pattern with randomness"
        sine = self.amplitude * math.sin(2 * math.pi * self._t / self.period)
        value = self.base + sine + random.gauss(0, self.noise_std)
        self._t += 1

        # rare off-chart spike to simulate a sensor glitch
        if self.wild_prob > 0 and random.random() < self.wild_prob:
            value *= 3

        return int(value)

    @property
    def value_return(self):
        return self.random_values

    def plot_random_data(self, number_of_data_values: int = 30):
        for _ in range(number_of_data_values):
            v = self.random_values()
            print(v)


if __name__ == "__main__":
    generator = DataGenerator(wild_prob=0.05, skip_block_prob=0.05)
    generator.plot_random_data()
