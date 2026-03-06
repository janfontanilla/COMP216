import random
import matplotlib.pyplot as plt

'''
Lab 8 - Data Generator
Simulation of a Network Latency sensor.
'''
class DataGenerator:
    # Private method that generates a normalized value (0 to 1)
    def _random_values(self) -> float:
        return random.uniform(0.0, 1.0)
    
    # Public property that provides access to the random values
    @property
    def value_return(self):
        # Calculate latency using the formula provided in the assignment: y = mx + c
        # This shifts the base range to what we want to measure for
        m = 50
        c = 30
        x = self._random_values()
        return (m * x) + c

    def plot_random_data(self):
        # The number of values to plot for along the x- and y-axes
        number_of_data_values=100
        y_data = [self.value_return for _ in range(number_of_data_values)]
        x_data = [i * 5 for i in range(number_of_data_values)] # Formula to change x-axis scale based on number_of_data_values

        # Create a list of colors: for latency over threshold, and normal otherwise
        point_colors = ['red' if ms > 75 else 'green' for ms in y_data]
        
        plt.figure(figsize=(12, 5))
        
        # Use scatter since newtork pings are disrete individual events
        plt.scatter(x_data, y_data, c=point_colors, s=30, edgecolors='black', linewidth=0.5)
        
        # Horizontal line to visually mark the threshold for lag
        plt.axhline(y=75, color='red', linestyle='--', alpha=0.4, label='Lag Threshold (75ms)')
        
        # Title and labels
        plt.title("Real-time Network Latency Monitor (pings)")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Latency (ms)")
        
        # Chart definitions
        plt.xlim(0, 500)
        plt.ylim(0, 100)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend()

        # Display the result
        plt.show()

if __name__ == "__main__":
    # Create the generator instance and trigger visualization 
    generator = DataGenerator()
    generator.plot_random_data()