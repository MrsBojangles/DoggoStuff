import requests
import io
from PIL import Image, ImageTk
import tkinter as tk

DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

def fetch_dog_image():
    """Fetch a random dog image from the Dog CEO API and return raw image bytes."""
    try:
        response = requests.get(DOG_API_URL, timeout=10)
        response.raise_for_status()
        img_url = response.json()["message"]

        img_response = requests.get(img_url, timeout=10)
        img_response.raise_for_status()
        return img_response.content
    except Exception as e:
        print(f"Error fetching dog image: {e}")
        return None

def show_new_dog():
    """Fetch a new dog and display it in the GUI."""
    img_data = fetch_dog_image()
    if img_data:
        image = Image.open(io.BytesIO(img_data))
        image = image.resize((400, 400))  # make it a consistent size
        photo = ImageTk.PhotoImage(image)

        label.config(image=photo)
        label.image = photo  # keep a reference!
    else:
        label.config(text="Could not load doggo 😢")

# --- GUI setup ---
root = tk.Tk()
root.title("Doggo Randomizer 🐶")
root.geometry("450x500")

label = tk.Label(root, text="Click the button for a doggo!", font=("Arial", 14))
label.pack(pady=20)

button = tk.Button(root, text="🐾 Show me a doggo!", command=show_new_dog, font=("Arial", 14))
button.pack(pady=20)

# Start by showing one immediately
show_new_dog()

root.mainloop()
