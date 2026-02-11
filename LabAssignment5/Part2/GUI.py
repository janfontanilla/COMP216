import tkinter as tk

window = tk.Tk()

header_text_font = ('Arial', 20, 'bold')

win_def_size = window.geometry("500x400")

label = tk.Label(window, text='ICET Student Survey', font=header_text_font).place(relx=0.5, rely=0.1, anchor='center')


win_title = window.title('Centennial College')

window.mainloop()