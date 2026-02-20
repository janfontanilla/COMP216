import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from PIL import Image, ImageTk
import io

SERVER_URL = "http://127.0.0.1:5000"


class ImageClient(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Image Client")
        self.geometry("600x500")

        # dropdown
        tk.Label(self, text="Available Images").pack()
        self.image_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.image_var)
        self.dropdown.pack()

        # dropdown for image formats
        tk.Label(self, text="Select Format").pack()
        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(
            self, 
            textvariable=self.format_var, 
            values=["png", "jpeg", "webp", "bmp"]
        )
        self.format_dropdown.pack()
        self.format_dropdown.set("jpeg")  # default

        # buttons
        tk.Button(self, text="Fetch Images", command=self.fetch_images).pack()
        tk.Button(self, text="Load Selected Image", command=self.load_image).pack()
        tk.Button(self, text="Load in Format", command=self.load_in_format).pack()
        tk.Button(self, text="Upload Image", command=self.upload_image).pack()
        tk.Button(self, text="Delete Image", command=self.delete_image).pack()

        # image display
        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.info_label = tk.Label(self, text="")
        self.info_label.pack()

    def fetch_images(self):
        try:
            response = requests.get(f"{SERVER_URL}/image-list")
            data = response.json()
            images = data.get("images", [])
            self.dropdown['values'] = images

            if images:
                self.dropdown.set(images[0])
            else:
                self.dropdown.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_image(self):
        try:
            filename = self.image_var.get()
            response = requests.get(f"{SERVER_URL}/get-image/{filename}")

            data = response.json()
            image_bytes = requests.get(data["url"]).content

            img = Image.open(io.BytesIO(image_bytes))
            img = img.resize((300, 300))
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            self.info_label.config(text=f"Format: {data['format']} Size: {data['size']}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # function to load the image in specified format
    def load_in_format(self):
        try:
            filename = self.image_var.get()
            fmt = self.format_var.get()
    
            response = requests.get(
                f"{SERVER_URL}/convert-image/{filename}?format={fmt}"
            )
            data = response.json()
    
            image_bytes = requests.get(data["url"]).content
            img = Image.open(io.BytesIO(image_bytes))
            img = img.resize((300, 300))
            photo = ImageTk.PhotoImage(img)
    
            self.image_label.config(image=photo)
            self.image_label.image = photo
    
            self.info_label.config(
                text=f"Format: {data['format']} Size: {data['size']}"
            )
    
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename()
            files = {'file': open(file_path, 'rb')}
            requests.post(f"{SERVER_URL}/uploads", files=files)
            messagebox.showinfo("Success", "Image uploaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_image(self):
        try:
            filename = self.image_var.get()
            requests.delete(f"{SERVER_URL}/delete-image/{filename}")
            messagebox.showinfo("Deleted", f"{filename} deleted")
            self.fetch_images()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ImageClient()
    app.mainloop()
