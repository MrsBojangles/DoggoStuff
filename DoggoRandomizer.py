import requests
import io
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog

DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

def fetch_dog_image():
    try:
        resp = requests.get(DOG_API_URL, timeout=10)
        resp.raise_for_status()
        img_url = resp.json()["message"]

        img_resp = requests.get(img_url, timeout=10)
        img_resp.raise_for_status()
        return img_resp.content, img_url
    except Exception as e:
        print("Fetch error:", e)
        return None, None

def extract_breed_from_url(url):
    try:
        parts = url.split('/breeds/')[1]
        slug = parts.split('/')[0]          # e.g., "bordercollie" or "greatdane"
        words = slug.replace('-', ' ').split()
        # If it’s e.g. "border collie", flip to "Border Collie"
        if len(words) > 1:
            words = words[::-1]             # reverse order
        return " ".join(word.title() for word in words)
    except Exception:
        return "Unknown"

def show_new_dog():
    img_data, img_url = fetch_dog_image()
    if not img_data:
        messagebox.showerror("Error", "Could not load a dog image. Check your connection.")
        image_label.config(image='', text="Could not load doggo 😢")
        breed_label.config(text="Breed: -")
        return

    img = Image.open(io.BytesIO(img_data))
    img.thumbnail((400, 400))           # preserve aspect ratio
    photo = ImageTk.PhotoImage(img)

    image_label.config(image=photo, text='')
    image_label.image = photo           # keep reference
    root.current_image_data = img_data  # store raw bytes for save
    root.current_image_url = img_url

    breed_label.config(text=f"Breed: {extract_breed_from_url(img_url)}")

def save_current_image():
    data = getattr(root, "current_image_data", None)
    if not data:
        messagebox.showinfo("No Image", "No image to save — fetch one first!")
        return
    path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                        filetypes=[("JPEG","*.jpg"),("PNG","*.png")])
    if path:
        with open(path, "wb") as f:
            f.write(data)
        messagebox.showinfo("Saved", f"Saved to {path}")

# GUI setup
root = tk.Tk()
root.title("Doggo Randomizer 🐶")
root.geometry("500x650")

image_label = tk.Label(root, text="Click the button for a doggo!", font=("Arial", 14))
image_label.pack(pady=10)

breed_label = tk.Label(root, text="Breed: -", font=("Arial", 12))
breed_label.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

show_btn = tk.Button(btn_frame, text="🐾 New doggo", command=show_new_dog, font=("Arial", 12))
show_btn.pack(side="left", padx=6)

save_btn = tk.Button(btn_frame, text="💾 Save", command=save_current_image, font=("Arial", 12))
save_btn.pack(side="left", padx=6)

# show one at startup
show_new_dog()

root.mainloop()
