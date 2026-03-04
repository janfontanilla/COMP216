import random
import matplotlib.pyplot as plt

class DataGenerator: 
    def random_values(self) -> float:
        return random.uniform(0.0, 1.0)
    
    @property
    def value_return(self):
        return self.random_values

    def plot_random_data(self, number_of_data_values: int = 50):
        y_data = [self.random_values() for _ in range(number_of_data_values)]
        x_data = [self.random_values() for _ in range(number_of_data_values)]

        plt.plot(x_data, y_data, 'r+')
        plt.show()

if __name__ == "__main__": 
    generator = DataGenerator()
    generator.plot_random_data()