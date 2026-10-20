import cv2

import numpy as np


def load_and_prepare_image(image_path):
    loaded_image = cv2.imread(image_path)
    if loaded_image is not None:
        processed_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
        return processed_image
    else:
        raise FileNotFoundError(
            "No such image exist please choose correct path!")


def detect_edges(processed_image, low_threshold=None, high_threshold=None):
    if low_threshold is None and high_threshold is None:
        median = np.median(processed_image)
        sigma = 1/3
        low_thresh = int(max(1, (1.0 - sigma) * median))
        high_thresh = int(min(255, (1.0 + sigma) * median))
        high_thresh = max(low_thresh + 1, high_thresh)
    elif low_threshold is None or high_threshold is None:
        raise ValueError("Both Canny thresholds must be provided together.")
    else:
        low_thresh = int(low_threshold)
        high_thresh = int(high_threshold)
        if not 1 <= low_thresh < high_thresh <= 255:
            raise ValueError(
                "Canny thresholds must satisfy 1 <= low < high <= 255.")

    edges = cv2.Canny(processed_image, low_thresh, high_thresh)

    return edges


def extract_contours(edges_image):
    optimal_thresh, thresholded_image = cv2.threshold(
        edges_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(
        thresholded_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours


def simplify_contours(contours, epsilon_factor=0.002):
    simplified_contours = [
    ]
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        epsilon = perimeter*epsilon_factor
        approximated_contour = cv2.approxPolyDP(contour, epsilon, closed=True)
        simplified_contours.append(approximated_contour)

    return simplified_contours


def contours_to_paths(simplified_contours, width, height):
    paths = []

    for contour in simplified_contours:
        # 1. Reshape contour into pairs of x, y coordinates
        points = contour.reshape(-1, 2)

        path = []

        for point in points:
            x = point[0]
            y = point[1]

            # 2. Centre the coordinates and reverse the Y-axis
            turtle_x = x - width / 2
            turtle_y = height / 2 - y

            # 3. Add the transformed pair to path
            path.append((float(turtle_x), float(turtle_y)))

        paths.append(path)

    return paths
