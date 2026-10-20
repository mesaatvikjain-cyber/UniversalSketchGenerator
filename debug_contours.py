
import cv2
from image_processor import (
    load_and_prepare_image,
    detect_edges,
    extract_contours,
    simplify_contours,
)

image_path = r"C:\Users\amitj\Desktop\Projects\UniversalSketch\image.png"

image = load_and_prepare_image(image_path)
edges = detect_edges(image)

contours = extract_contours(edges)
simplified = simplify_contours(contours)

print("Image size:", image.shape[1], "x", image.shape[0])
print("Contours:", len(contours))
print("Simplified contours:", len(simplified))
print("Original points:", sum(len(c) for c in contours))
print("Simplified points:", sum(len(c) for c in simplified))

preview = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(preview, simplified, -1, (0, 255, 0), 1)

cv2.imshow("Simplified Contours", preview)
cv2.waitKey(0)
cv2.destroyAllWindows()
