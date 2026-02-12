import tkinter as tk
from tkinter import ttk

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Centennial College')
        self.geometry("600x500")

        # Header
        header_font = ('Arial', 20, 'bold')
        tk.Label(self, text='ICET Student Survey', font=header_font)\
            .place(relx=0.5, rely=0.1, anchor='center') 

        # Full name
        tk.Label(self, text='Full name').place(relx=0, rely=0.2, anchor='w')
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.place(relx=0.5, rely=0.2, anchor='center')

        # Residency radio buttons
        tk.Label(self, text='Residency').place(relx=0, rely=0.27, anchor='w')
        self.residency_var = tk.StringVar()

        tk.Radiobutton(self, text='Domestic', variable=self.residency_var, value='dom')\
            .place(relx=0.41, rely=0.27, anchor='center')

        tk.Radiobutton(self, text='International', variable=self.residency_var, value='intl')\
            .place(relx=0.422, rely=0.32, anchor='center')

        # Program combobox
        tk.Label(self, text='Program').place(relx=0, rely=0.37, anchor='w')
        self.program_combo = ttk.Combobox(self,
                                          values=['AI', 'Gaming', 'Health', 'Software'])
        self.program_combo.place(relx=0.47, rely=0.38, anchor='center')

        # Courses checkboxes
        tk.Label(self, text='Courses').place(relx=0, rely=0.42, anchor='w')

        self.comp100 = tk.StringVar()
        self.comp213 = tk.StringVar()
        self.comp120 = tk.StringVar()

        tk.Checkbutton(self, text='Programming I',
                       variable=self.comp100,
                       onvalue='COMP100',
                       offvalue='').place(relx=0.43, rely=0.45, anchor='center')

        tk.Checkbutton(self, text='Web Page Design',
                       variable=self.comp213,
                       onvalue='COMP213',
                       offvalue='').place(relx=0.44, rely=0.5, anchor='center')

        tk.Checkbutton(self, text='Software Engineering',
                       variable=self.comp120,
                       onvalue='COMP120',
                       offvalue='').place(relx=0.455, rely=0.55, anchor='center')

        # Reset button
        tk.Button(self, text='Reset', command=self.reset_form, width=20)\
            .place(relx=0.1, rely=0.8, anchor='w')

        self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.residency_var.set('dom')
        self.program_combo.current(0)
        self.comp100.set('')
        self.comp213.set('')
        self.comp120.set('')


if __name__ == "__main__":
    app = GUI()
    app.mainloop()