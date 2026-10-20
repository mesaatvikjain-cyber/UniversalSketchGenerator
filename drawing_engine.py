from pathlib import Path
import tkinter as tk

from PIL import Image, ImageColor, ImageDraw, ImageTk


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800


def _scale_paths(paths):
    all_points = [point for path in paths for point in path]
    if not all_points:
        return [], 1

    x_values = [point[0] for point in all_points]
    y_values = [point[1] for point in all_points]
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    drawing_width = max_x - min_x
    drawing_height = max_y - min_y
    scale_x = 1100 / drawing_width if drawing_width > 0 else 1
    scale_y = 700 / drawing_height if drawing_height > 0 else 1
    scale = min(scale_x, scale_y)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    scaled_paths = [
        [
            (
                (x - center_x) * scale + CANVAS_WIDTH / 2,
                CANVAS_HEIGHT / 2 - (y - center_y) * scale,
            )
            for x, y in path
        ]
        for path in paths
    ]
    return scaled_paths, scale


def draw_paths(paths, pen_color="black", pen_size=2, master=None):
    image = _render_image(paths, pen_color, pen_size)
    if image is None:
        return

    preview_window = tk.Toplevel(master)
    preview_window.title("Sketch Preview")
    preview_window.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    photo = ImageTk.PhotoImage(image)
    preview = tk.Label(preview_window, image=photo, background="white")
    preview.image = photo
    preview.pack()


def _render_image(paths, pen_color, pen_size):
    scaled_paths, _ = _scale_paths(paths)
    if not scaled_paths or not any(scaled_paths):
        return None

    color = ImageColor.getrgb(pen_color)
    image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    for path in scaled_paths:
        if len(path) > 1:
            draw.line(
                path + [path[0]],
                fill=color,
                width=pen_size,
                joint="curve",
            )
        elif path:
            x, y = path[0]
            radius = max(1, pen_size // 2)
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=color,
            )
    return image


def save_paths(paths, file_path, pen_color="black", pen_size=2):
    scaled_paths, _ = _scale_paths(paths)
    if not scaled_paths or not any(scaled_paths):
        raise ValueError("There is no sketch to save.")

    output_path = Path(file_path)
    color = ImageColor.getrgb(pen_color)

    if output_path.suffix.lower() == ".eps":
        red, green, blue = (component / 255 for component in color)
        with output_path.open("w", encoding="ascii") as eps_file:
            eps_file.write(
                f"%!PS-Adobe-3.0 EPSF-3.0\n"
                f"%%BoundingBox: 0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}\n"
                f"{pen_size} setlinewidth\n"
                f"{red:.6f} {green:.6f} {blue:.6f} setrgbcolor\n"
            )
            for path in scaled_paths:
                if not path:
                    continue
                first_x, first_y = path[0]
                eps_file.write(
                    f"newpath {first_x:.3f} {CANVAS_HEIGHT - first_y:.3f} moveto\n"
                )
                for x, y in path[1:]:
                    eps_file.write(f"{x:.3f} {CANVAS_HEIGHT - y:.3f} lineto\n")
                eps_file.write("closepath stroke\n")
            eps_file.write("showpage\n%%EOF\n")
        return

    if output_path.suffix.lower() != ".png":
        raise ValueError("Sketches can be saved only as PNG or EPS files.")

    image = _render_image(paths, pen_color, pen_size)
    image.save(output_path)
