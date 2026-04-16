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
        self.values = [random.randint(10, 100) for _ in range(20)] #initialize data list

        # canvas added
        self.canvas = tk.Canvas(self.root, width=600, height=350, bg="white")  # reduced height to make room
        self.canvas.pack()

        # start UI
        self.initUI()

    # part A: update data in a separate thread
    def update_data(self):
        while True:
            self.values.pop(0)
            self.values.append(random.randint(10, 100)) #add a new random value to the end of the list
            self.display_chart() #display the list on the canvas
            
            # ENTRY WIDGET 
            delay = float(self.entry.get()) if self.entry.get() else 0.5
            
            time.sleep(0.5)  # change to time.sleep(delay) if entry widget is active
    
    def display_chart(self):
        self.canvas.delete("all")
        for i in range(len(self.values) - 1):
            x1 = i * 25
            y1 = 300 - self.values[i]
            x2 = (i + 1) * 25
            y2 = 300 - self.values[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def initUI(self):
        
        # ENTRY WIDGET
        tk.Label(self.root, text="Update delay (seconds):").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(self.root, width=5)
        self.entry.pack(side=tk.LEFT)  

              
        self.entry.destroy()

        #threads
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True #runs thread outside of main 
        self.update_thread.start()

root = tk.Tk()
app = DynamicChart(root)
root.mainloop()
