import smtplib
from email.mime.text import MIMEText
from tkinter import Tk, Canvas, Frame, BOTH
import tkinter as tk
from tkinter import messagebox
import threading

SMTP_SERVER = 'smtp.mailgun.org'   
PORT = 587
USER_NAME = 'mohammadbaig@sandboxd26a75a6d36f488a98c409657038597a.mailgun.org'   
PASSWORD = ''

SENDER_EMAIL = 'mbaig77@my.centennialcollege.ca'
RECPT_EMAIL = ['mbaig77@my.centennialcollege.ca', 'mohammadbaig.centennial@gmail.com']

# Send an out-of-range alert email. Runs in a background thread.
def send_alert_email(value):

    if value < 30:
        reason = f'{value} ms is BELOW the minimum threshold of 30 ms.'
    else:
        reason = f'{value} ms is ABOVE the maximum threshold of 80 ms.'

    html_message = f'''<html>
<body>
<h3>&#9888; Network Latency Alert</h3>
<p>An out-of-range value was entered in the Network Latency Monitor.</p>
<p><b>Value entered:</b> {value} ms<br>
<b>Normal range:</b> 30 – 80 ms<br>
<b>Detail:</b> {reason}</p>
<p>Please review the sensor or the input.</p>
<hr>
<small>COMP216 – Network Latency Monitor</small>
</body>
</html>'''

    email_content = MIMEText(html_message, 'html')
    email_content['From']    = SENDER_EMAIL
    email_content['To']      = ', '.join(RECPT_EMAIL)
    email_content['Subject'] = f'[ALERT] Latency out of range: {value} ms'

    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as smtp:
            smtp.starttls()
            smtp.login(USER_NAME, PASSWORD)
            smtp.sendmail(SENDER_EMAIL, RECPT_EMAIL, email_content.as_string())
        print(f'Alert email sent for value: {value} ms')
    except Exception as e:
        print(f'Email error: {e}')


# ── GUI ───────────────────────────────────────────────────────────────────────
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

        # status bar at the bottom
        self.status_var = tk.StringVar(value='')
        tk.Label(self, textvariable=self.status_var,
                 font='Helvetica 8', bg='#f0f2f5',
                 fg='#888888').pack(pady=(0, 6))
        # --------------------------------------

    def draw_bar(self, value):
        self.canvas.delete('all')

        # keep value within our sensor range
        if value < 30:
            value = 30
        if value > 80:
            value = 80

        fill_pct   = (value - 30) / (80 - 30)
        fill_width = 50 + fill_pct * 200

        if value >= 75:
            color = '#e05252'
        elif value >= 65:
            color = '#e0a852'
        else:
            color = '#4caf50'

        # grey track
        self.canvas.create_rectangle(50, 50, 250, 110,
                                     fill='#dde1e7', outline='')
        # filled bar
        self.canvas.create_rectangle(50, 50, fill_width, 110,
                                     fill=color, outline='')
        # outline
        self.canvas.create_rectangle(50, 50, 250, 110,
                                     outline='#aaaaaa', width=1)

        # tick marks
        for t in [40, 50, 60, 70]:
            tx = 50 + ((t - 30) / 50) * 200
            self.canvas.create_line(tx, 47, tx, 53, fill='#999999', width=1)
            self.canvas.create_text(tx, 43, text=str(t),
                                    font='Helvetica 7', fill='#999999')

        # dashed threshold line at 75 ms
        thresh_x = 50 + ((75 - 30) / 50) * 200
        self.canvas.create_line(thresh_x, 44, thresh_x, 116,
                                fill='#cc3333', width=2, dash=(4, 2))

        # range labels
        self.canvas.create_text(50,       124, text='30 ms',
                                font='Helvetica 8', fill='#555555')
        self.canvas.create_text(thresh_x, 124, text='75 ms ⚠',
                                font='Helvetica 8', fill='#cc3333')
        self.canvas.create_text(250,      124, text='80 ms',
                                font='Helvetica 8', fill='#555555')

        # large value readout
        self.canvas.create_text(150, 150, font='Helvetica 18 bold',
                                fill=color, text=f'{value} ms')

        # status label
        if value >= 75:
            status = 'HIGH LATENCY'
        elif value >= 65:
            status = 'CAUTION'
        else:
            status = 'Normal'
        self.canvas.create_text(150, 170, font='Helvetica 9',
                                fill=color, text=status)

    def update_value(self):
        try:
            value = int(self.entry.get())
            self.draw_bar(value)

            # trigger alert email if value is outside sensor range
            if value < 30 or value > 80:
                self.status_var.set('Out of range — sending alert email...')
                # run in background thread so the GUI doesn't freeze
                t = threading.Thread(target=self._send_and_update, args=(value,), daemon=True)
                t.start()
            else:
                self.status_var.set('')

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid whole number")

    # Send the email then update the status label from the main thread.
    def _send_and_update(self, value):
        send_alert_email(value)
        self.status_var.set(f'Alert email sent for {value} ms')


root = Tk()
app = DisplayBar()
root.geometry('400x330+300+300')
root.mainloop()