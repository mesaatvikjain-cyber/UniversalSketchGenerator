
from image_processor import (
    load_and_prepare_image,
    detect_edges,
    extract_contours,
    simplify_contours,
    contours_to_paths,
)
from drawing_engine import draw_paths


image_path = r"C:\Users\amitj\Desktop\Projects\UniversalSketch\image.png"


# 1. Load and prepare the image
image = load_and_prepare_image(image_path)

# 2. Detect edges
edges = detect_edges(image)

# 3. Extract contours
contours = extract_contours(edges)

# 4. Simplify contours
simplified_contours = simplify_contours(contours)

# 5. Convert contours into Turtle paths
height, width = image.shape
paths = contours_to_paths(simplified_contours, width, height)

print("Image loaded successfully.")
print("Contours:", len(simplified_contours))
print("Paths:", len(paths))
all_points = [point for path in paths for point in path]

if all_points:
    x_values = [point[0] for point in all_points]
    y_values = [point[1] for point in all_points]

    print("Path count:", len(paths))
    print("Total points:", len(all_points))
    print("X bounds:", min(x_values), "to", max(x_values))
    print("Y bounds:", min(y_values), "to", max(y_values))

# 6. Draw the image
draw_paths(paths)
