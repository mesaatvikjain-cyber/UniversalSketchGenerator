
import cv2
from image_processor import load_and_prepare_image, detect_edges, extract_contours

image_path = r"C:\Users\amitj\Desktop\Projects\UniversalSketch\image.png"

# Stage 1: Load the image
image = load_and_prepare_image(image_path)

print("Image shape:", image.shape)
print("Pixel range:", image.min(), "to", image.max())

# Stage 2: Detect edges
edges = detect_edges(image)

print("Edge pixels:", cv2.countNonZero(edges))

# Stage 3: Extract contours
contours = extract_contours(edges)

print("Contours detected:", len(contours))
print("Total contour points:", sum(len(c) for c in contours))

# Display intermediate results
cv2.imshow("1 - Prepared Grayscale Image", image)
cv2.imshow("2 - Detected Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
