from tkinter import Tk, Canvas, Frame, BOTH, W
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os


# display bar for network latency
# using the same sensor from Lab 8 (y = mx + c, so range is 30 to 80ms)
class DisplayBar(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title('Network Latency Monitor')
        self.pack(fill=BOTH, expand=1)

        # title label
        tk.Label(self, text='Network Latency (ms)',
                 font='Helvetica 14').pack(pady=10)

        # canvas to draw the bar gauge on
        self.canvas = Canvas(self, width=300, height=200)
        self.canvas.pack(fill=BOTH, expand=1)

        # draw with a starting value
        self.draw_bar(50)

        # ----------- ADDED PART (entry + button) -----------
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter latency (ms):").pack(side=tk.LEFT)

        self.entry = tk.Entry(input_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)

        tk.Button(input_frame, text="Update", command=self.update_value)\
            .pack(side=tk.LEFT)
        # ---------------------------------------------------

    def draw_bar(self, value):
        self.canvas.delete('all')  # clear old drawing

        # keep value within our sensor range
        if value < 30:
            value = 30
        if value > 80:
            value = 80

        # how much of the bar to fill (0.0 to 1.0)
        fill_pct = (value - 30) / (80 - 30)
        fill_width = 50 + fill_pct * 200  # bar goes from x=50 to x=250

        # green for normal, red for lag (75ms+ is lag from Lab 8)
        if value >= 75:
            color = 'red'
        else:
            color = 'green'

        # filled portion of bar
        self.canvas.create_rectangle(
            50, 30,                        # top left
            fill_width, 130,               # bottom right
            fill=color, outline='')

        # bar outline
        self.canvas.create_rectangle(
            50, 30,                        # top left
            250, 130,                      # bottom right
            outline='#222', width=2)

        # dashed line at 75ms threshold
        thresh_x = 50 + ((75 - 30) / (80 - 30)) * 200
        self.canvas.create_line(thresh_x, 25, thresh_x, 135,
                                fill='red', width=2,
                                dash=(4, 2))  # dashed line style

        # range labels along the bottom
        self.canvas.create_text(50, 150, text='30',
                                font='Helvetica 9')
        self.canvas.create_text(thresh_x, 150, text='75',
                                font='Helvetica 9', fill='red')
        self.canvas.create_text(250, 150, text='80',
                                font='Helvetica 9')

        # show the current value
        self.canvas.create_text(150, 170,
                                font='Helvetica 12',
                                text=f'{value} ms')

    # ----------- ADDED FUNCTION -----------
    def update_value(self):
        try:
            value = int(self.entry.get())
            self.draw_bar(value)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
    # -------------------------------------


root = Tk()
app = DisplayBar()
root.geometry('400x250+300+300')
root.mainloop()