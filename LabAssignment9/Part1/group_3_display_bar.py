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
        self.master.configure(bg='#f0f2f5')
        self.configure(bg='#f0f2f5')
        self.pack(fill=BOTH, expand=1)

        # title label
        tk.Label(self, text='Network Latency Monitor',
                 font='Helvetica 15 bold',
                 bg='#f0f2f5', fg='#1a1a2e').pack(pady=(14, 2))

        tk.Label(self, text='Sensor range: 30 – 80 ms  |  Threshold: 75 ms',
                 font='Helvetica 9',
                 bg='#f0f2f5', fg='#666666').pack(pady=(0, 6))

        # canvas to draw the bar gauge on
        self.canvas = Canvas(self, width=340, height=180,
                             bg='#f0f2f5', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        # draw with a starting value
        self.draw_bar(50)

        # ----------- entry + button -----------
        input_frame = tk.Frame(self, bg='#f0f2f5')
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter latency (ms):",
                 bg='#f0f2f5', fg='#1a1a2e',
                 font='Helvetica 10').pack(side=tk.LEFT)

        self.entry = tk.Entry(input_frame, width=7,
                              font='Helvetica 11',
                              relief='solid', bd=1)
        self.entry.pack(side=tk.LEFT, padx=6)
        self.entry.bind('<Return>', lambda e: self.update_value())

        tk.Button(input_frame, text="Update",
                  font='Helvetica 10 bold',
                  bg='#4a90d9', fg='white',
                  activebackground='#357abd',
                  relief='flat', padx=10, pady=3,
                  cursor='hand2',
                  command=self.update_value).pack(side=tk.LEFT)
        # --------------------------------------

    def draw_bar(self, value):
        self.canvas.delete('all')

        # keep value within our sensor range
        value = max(30, min(value, 80))



        # how much of the bar to fill (0.0 to 1.0)
        fill_pct = (value - 30) / (80 - 30)
        fill_width = 50 + fill_pct * 200  # bar goes from x=50 to x=250

        # green for normal, amber for caution, red for lag
        if value >= 75:
            color = '#e05252'
        elif value >= 65:
            color = '#e0a852'
        else:
            color = '#4caf50'

        # light grey track behind the bar
        self.canvas.create_rectangle(
            50, 50, 250, 110,
            fill='#dde1e7', outline='')

        # filled portion of bar
        self.canvas.create_rectangle(
            50, 50,
            fill_width, 110,
            fill=color, outline='')

        # bar outline
        self.canvas.create_rectangle(
            50, 50, 250, 110,
            outline='#aaaaaa', width=1)

        # tick marks at 40, 50, 60, 70
        for t in [40, 50, 60, 70]:
            tx = 50 + ((t - 30) / 50) * 200
            self.canvas.create_line(tx, 47, tx, 53,
                                    fill='#999999', width=1)
            self.canvas.create_text(tx, 43, text=str(t),
                                    font='Helvetica 7', fill='#999999')

        # dashed threshold line at 75 ms
        thresh_x = 50 + ((75 - 30) / 50) * 200
        self.canvas.create_line(thresh_x, 44, thresh_x, 116,
                                fill='#cc3333', width=2,
                                dash=(4, 2))

        # range labels along the bottom
        self.canvas.create_text(50, 124, text='30 ms',
                                font='Helvetica 8', fill='#555555')
        self.canvas.create_text(thresh_x, 124, text='75 ms ⚠',
                                font='Helvetica 8', fill='#cc3333')
        self.canvas.create_text(250, 124, text='80 ms',
                                font='Helvetica 8', fill='#555555')

        # show the current value (large, coloured)
        self.canvas.create_text(150, 150,
                                font='Helvetica 18 bold',
                                fill=color,
                                text=f'{value} ms')

        # status label
        if value >= 75:
            status = 'HIGH LATENCY'
        elif value >= 65:
            status = 'CAUTION'
        else:
            status = 'Normal'
        self.canvas.create_text(150, 170,
                                font='Helvetica 9',
                                fill=color,
                                text=status)

    # ----------- update function -----------
    def update_value(self):
        try:
            value = int(self.entry.get())
            self.draw_bar(value)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid whole number")
    # ----------------------------------------


root = Tk()
app = DisplayBar()
root.geometry('400x310+300+300')
root.mainloop()
