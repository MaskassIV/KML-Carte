import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageTk
import tkinter as tk

coords = [
    ("Marseille", 43.2965, 5.3698),
    ("Avignon", 43.9493, 4.8055),
    ("Arles", 43.67<66, 4.6278),
]

output_dir = "captures"
os.makedirs(output_dir, exist_ok=True)

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)


def capture_images():
    for nom, lat, lon in coords:
        url = f"https://earth.google.com/web/@{lat},{lon},500a,35y,0h,0t,0r"
        driver.get(url)
        time.sleep(8)  
        filename = f"{nom.lower().replace(' ', '_')}.png"
        driver.save_screenshot(os.path.join(output_dir, filename))
    driver.quit()

answers = []


def validate_images():
    image_files = [f"{nom.lower().replace(' ', '_')}.png" for nom, _, _ in coords]

    def on_yes():
        answers.append((coords[current[0]][0], "oui"))
        next_image()

    def on_no():
        answers.append((coords[current[0]][0], "non"))
        next_image()

    def next_image():
        current[0] += 1
        if current[0] < len(coords):
            update_image(current[0])
        else:
            root.destroy()
            with open("reponses.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ville", "reponse"])
                writer.writerows(answers)

    def update_image(index):
        img_path = os.path.join(output_dir, image_files[index])
        img = Image.open(img_path)
        img = img.resize((800, 600))
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk
        root.title(f"{coords[index][0]} ({index + 1}/{len(coords)})")

    root = tk.Tk()
    current = [0]
    label = tk.Label(root)
    label.pack()

    btn_yes = tk.Button(root, text="Oui", command=on_yes)
    btn_yes.pack(side="left", padx=20, pady=20)

    btn_no = tk.Button(root, text="Non", command=on_no)
    btn_no.pack(side="right", padx=20, pady=20)

    update_image(current[0])
    root.mainloop()

# Étapes du programme
capture_images()
validate_images()
