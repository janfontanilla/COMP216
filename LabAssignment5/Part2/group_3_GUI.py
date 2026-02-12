import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Centennial College')
        self.geometry("600x500")

        # Header
        header_font = ('Arial', 20, 'bold')
        tk.Label(self, text='ICET Student Survey', font=header_font)\
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Full name
        tk.Label(self, text='Full name').grid(row=1, column=0, sticky='w', padx=10)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.grid(row=1, column=1, padx=10)

        # Residency radio buttons
        tk.Label(self, text='Residency').grid(row=2, column=0, sticky='w', padx=10)
        self.residency_var = tk.StringVar()

        tk.Radiobutton(self, text='Domestic', variable=self.residency_var, value='dom')\
            .grid(row=2, column=1, sticky='w')

        tk.Radiobutton(self, text='International', variable=self.residency_var, value='intl')\
            .grid(row=3, column=1, sticky='w')

        # Program combobox
        tk.Label(self, text='Program').grid(row=4, column=0, sticky='w', padx=10)
        self.program_combo = ttk.Combobox(self,
                                          values=['AI', 'Gaming', 'Health', 'Software'])
        self.program_combo.grid(row=4, column=1, padx=10)

        # Courses checkboxes
        tk.Label(self, text='Courses').grid(row=5, column=0, sticky='w', padx=10)

        self.comp100 = tk.StringVar()
        self.comp213 = tk.StringVar()
        self.comp120 = tk.StringVar()

        tk.Checkbutton(self, text='Programming I',
                       variable=self.comp100,
                       onvalue='COMP100',
                       offvalue='').grid(row=5, column=1, sticky='w')

        tk.Checkbutton(self, text='Web Page Design',
                       variable=self.comp213,
                       onvalue='COMP213',
                       offvalue='').grid(row=6, column=1, sticky='w')

        tk.Checkbutton(self, text='Software Engineering',
                       variable=self.comp120,
                       onvalue='COMP120',
                       offvalue='').grid(row=7, column=1, sticky='w')

        # Reset button
        tk.Button(self, text='Reset', command=self.reset_form)\
            .grid(row=8, column=0, pady=15, padx=5, sticky='w')

        # Ok button - Mohammad
        tk.Button(self, text='OK', command=self.ok_action)\
            .grid(row=8, column=1, pady=15)

        # Exit button - Mohammad
        tk.Button(self, text='Exit', command=self.destroy)\
            .grid(row=8, column=2, pady=15, padx=5, sticky='e')

        self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.residency_var.set('dom')
        self.program_combo.current(0)
        self.comp100.set('')
        self.comp213.set('')
        self.comp120.set('')

    # Retrieves information to display in popup
    # Mohamamd
    def ok_action(self):
        name = self.name_entry.get()
        residency = self.residency_var.get()
        program = self.program_combo.get()
        courses = ", ".join(filter(None, [
            self.comp120.get(),
            self.comp100.get(),
            self.comp213.get()
        ]))

        if not courses:
            courses = "None"

        # Displays information in popup
        message = (
            f"{name}\n{residency}\n{program}\n{courses}"
        )

        messagebox.showinfo("Information", message)

if __name__ == "__main__":
    app = GUI()
    app.mainloop()