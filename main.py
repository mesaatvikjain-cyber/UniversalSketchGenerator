import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

import cv2
from PIL import Image, ImageTk

from drawing_engine import draw_paths, save_paths
from image_processor import (
    contours_to_paths,
    detect_edges,
    extract_contours,
    load_and_prepare_image,
    simplify_contours,
)


window = tk.Tk()
window.title("Image to Live Sketch")
window.geometry("700x850")

image_path_variable = tk.StringVar()
mode_variable = tk.StringVar(value="Contour Sketch")
pen_color_variable = tk.StringVar(value="black")
pen_size_variable = tk.IntVar(value=2)
low_threshold_variable = tk.IntVar(value=50)
high_threshold_variable = tk.IntVar(value=150)
latest_paths = []


def adjust_low_threshold(value):
    low_threshold = int(float(value))
    if low_threshold >= high_threshold_variable.get():
        high_threshold_variable.set(low_threshold + 1)


def adjust_high_threshold(value):
    high_threshold = int(float(value))
    if high_threshold <= low_threshold_variable.get():
        low_threshold_variable.set(high_threshold - 1)


def select_image():
    global latest_paths
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All Files", "*.*"),
        ],
    )

    if not file_path:
        return

    try:
        with Image.open(file_path) as pil_image:
            pil_image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(pil_image.copy())
    except OSError as error:
        messagebox.showerror("Unable to open image", str(error))
        return

    image_path_variable.set(file_path)
    latest_paths = []
    label.config(image=photo)
    label.image = photo


def create_sketch():
    global latest_paths
    latest_paths = []
    image_path = image_path_variable.get()
    if not image_path:
        messagebox.showwarning("No image selected", "Select an image first.")
        return

    try:
        image = load_and_prepare_image(image_path)
        edges = detect_edges(
            image,
            low_threshold_variable.get(),
            high_threshold_variable.get(),
        )
        contours = extract_contours(edges)

        if mode_variable.get() == "Contour Sketch":
            contours = simplify_contours(contours)

        height, width = image.shape
        paths = contours_to_paths(contours, width, height)
    except (FileNotFoundError, ValueError, cv2.error) as error:
        messagebox.showerror("Unable to create sketch", str(error))
        return

    if not any(paths):
        messagebox.showinfo(
            "No contours found",
            "No edges were detected in the selected image.",
        )
        return

    latest_paths = paths
    draw_paths(
        paths,
        pen_color_variable.get(),
        pen_size_variable.get(),
        master=window,
    )


def choose_pen_color():
    _, color = colorchooser.askcolor(
        color=pen_color_variable.get(),
        title="Choose sketch color",
    )
    if color:
        pen_color_variable.set(color)
        color_button.config(text=color, foreground=color)


def save_sketch(extension):
    if not latest_paths:
        messagebox.showwarning(
            "No sketch to save",
            "Create a sketch before saving it.",
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save sketch",
        defaultextension=extension,
        filetypes=[(f"{extension[1:].upper()} image", f"*{extension}")],
    )
    if not file_path:
        return

    try:
        save_paths(
            latest_paths,
            file_path,
            pen_color_variable.get(),
            pen_size_variable.get(),
        )
    except (OSError, ValueError) as error:
        messagebox.showerror("Unable to save sketch", str(error))
        return

    messagebox.showinfo("Sketch saved", f"Saved sketch to:\n{file_path}")


mode_selector = ttk.Combobox(
    window,
    textvariable=mode_variable,
    values=["Contour Sketch", "Detailed Edge Sketch"],
    state="readonly",
)
mode_selector.pack(pady=15)

select_button = tk.Button(window, text="Select Image", command=select_image)
select_button.pack(pady=10)

change_button = tk.Button(window, text="Change Image", command=select_image)
change_button.pack(pady=10)

controls = ttk.LabelFrame(window, text="Sketch settings", padding=10)
controls.pack(fill="x", padx=30, pady=10)

ttk.Label(controls, text="Canny low threshold").pack(anchor="w")
low_threshold_scale = tk.Scale(
    controls,
    from_=1,
    to=254,
    orient="horizontal",
    resolution=1,
    variable=low_threshold_variable,
    command=adjust_low_threshold,
)
low_threshold_scale.pack(fill="x")

ttk.Label(controls, text="Canny high threshold").pack(anchor="w")
high_threshold_scale = tk.Scale(
    controls,
    from_=2,
    to=255,
    orient="horizontal",
    resolution=1,
    variable=high_threshold_variable,
    command=adjust_high_threshold,
)
high_threshold_scale.pack(fill="x")

ttk.Label(controls, text="Line thickness").pack(anchor="w")
thickness_scale = tk.Scale(
    controls,
    from_=1,
    to=10,
    orient="horizontal",
    resolution=1,
    variable=pen_size_variable,
)
thickness_scale.pack(fill="x")

color_button = tk.Button(
    controls,
    text="black",
    foreground="black",
    command=choose_pen_color,
)
color_button.pack(pady=5)

create_button = tk.Button(window, text="Create Sketch", command=create_sketch)
create_button.pack(pady=10)

save_png_button = tk.Button(
    window,
    text="Save as PNG",
    command=lambda: save_sketch(".png"),
)
save_png_button.pack(pady=5)

save_eps_button = tk.Button(
    window,
    text="Save as EPS",
    command=lambda: save_sketch(".eps"),
)
save_eps_button.pack(pady=5)

label = tk.Label(window)
label.pack(pady=20)

window.mainloop()
