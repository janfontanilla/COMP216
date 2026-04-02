import tkinter as tk
import threading
import random
import time


class DynamicChart:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Time Series Chart")
        self.root.geometry("600x400")
        
        # create a values list with random values
        self.values = [random.randint(10, 100) for _ in range(20)]  #initialize data list
    
    # part A: update data in a separate thread
    def update_data(self):
        while True:
            self.values.pop(0)  #remove the first item in the list
            self.values.append(random.randint(10, 100))  #add a new random value to the end of the list
            self.display_chart()  #display the list on the canvas
            time.sleep(0.5)  #sleep for 0.5 seconds
    
    def display_chart(self):
        pass

    def initUI(self):
        
        #self.entry.destroy()

        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()