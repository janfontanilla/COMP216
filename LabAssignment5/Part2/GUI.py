import tkinter as tk
from tkinter import ttk, messagebox

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Centennial College')
        self.geometry("600x500")

        # Go through all the rows and columns and give them weight to make them move
        for row in range(9):
            self.rowconfigure(row, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Header
        header_font = ('Arial', 20, 'bold')
        tk.Label(self, text='ICET Student Survey', font=header_font).grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

        # Full name
        tk.Label(self, text='Full name').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)

        # Residency radio buttons
        tk.Label(self, text='Residency').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.residency_var = tk.StringVar()

        tk.Radiobutton(self, text='Domestic',
                       variable=self.residency_var, value='dom')\
            .grid(row=2, column=1, sticky='w', padx=10)

        tk.Radiobutton(self, text='International',
                       variable=self.residency_var, value='intl')\
            .grid(row=3, column=1, sticky='w', padx=10)

        # Program combobox
        tk.Label(self, text='Program').grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.program_combo = ttk.Combobox(self,
                                          values=['AI', 'Gaming', 'Health', 'Software'])
        self.program_combo\
            .grid(row=4, column=1, sticky='ew', padx=10, pady=5)

        # Courses checkboxes
        tk.Label(self, text='Courses').grid(row=5, column=0, sticky='w', padx=10, pady=5)

        self.comp100 = tk.StringVar()
        self.comp213 = tk.StringVar()
        self.comp120 = tk.StringVar()

        tk.Checkbutton(self, text='Programming I',
                       variable=self.comp100,
                       onvalue='COMP100',
                       offvalue='')\
            .grid(row=5, column=1, sticky='w', padx=10)

        tk.Checkbutton(self, text='Web Page Design',
                       variable=self.comp213,
                       onvalue='COMP213',   
                       offvalue='')\
            .grid(row=6, column=1, sticky='w', padx=10)

        tk.Checkbutton(self, text='Software Engineering',
                       variable=self.comp120,
                       onvalue='COMP120',   
                       offvalue='')\
            .grid(row=7, column=1, sticky='w', padx=10)

        # Button row (Reset, OK, Exit)
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15, padx=10, sticky='ew')
        # Make buttons spread out and resize with the window
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)

        # Reset button
        tk.Button(btn_frame, text='Reset', command=self.reset_form, width=20)\
            .grid(row=0, column=0, sticky='w', padx=10)
        
        # OK button - Mohammad
        tk.Button(btn_frame, text='OK', command=self.ok_action, width=20)\
            .grid(row=0, column=1, sticky='ew', padx=10)
        
        # Exit button - Mohammad
        tk.Button(btn_frame, text='Exit', command=self.destroy, width=20)\
            .grid(row=0, column=2, sticky='e', padx=10)

        self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, "John Doe")

        self.residency_var.set('dom')

        self.program_combo.current(0)

        self.comp100.set('COMP100')
        self.comp213.set('COMP213')
        self.comp120.set('COMP120')

    # Retrieves information to display in popup
    # Mohammad
    def ok_action(self):
        # Safely gather values for the popup, avoiding raw None
        name = self.name_entry.get() or "N/A"

        residency_code = self.residency_var.get()
        if residency_code == 'dom':
            residency = 'Domestic'
        elif residency_code == 'intl':
            residency = 'International'
        else:
            residency = 'N/A'

        program = self.program_combo.get() or "N/A"

        courses = ", ".join(filter(None, [
            self.comp120.get(),
            self.comp100.get(),
            self.comp213.get()
        ]))
        if not courses:
            courses = "None"

        # Displays information in popup
        message = (
            f"Name: {name}\n"
            f"Residency: {residency}\n"
            f"Program: {program}\n"
            f"Courses: {courses}"
        )

        messagebox.showinfo("Information", message)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()