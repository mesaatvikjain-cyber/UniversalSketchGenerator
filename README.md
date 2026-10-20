# UniversalSketch

UniversalSketch turns an image into a contour sketch using OpenCV and displays
the result in a Tkinter preview window.

## Requirements

- Python 3
- OpenCV (`opencv-python`)
- NumPy
- Pillow
- Tkinter (usually included with the standard Python installation)

Install the Python packages with:

```powershell
python -m pip install opencv-python numpy Pillow
```

## Run

Open PowerShell in the project folder and run:

```powershell
python main.py
```

## Use

1. Click **Select Image** and choose a JPG, JPEG, PNG, or BMP image.
2. Choose a sketch mode:
   - **Contour Sketch** simplifies contours to reduce drawing detail.
   - **Detailed Edge Sketch** keeps the detected contour points.
3. Adjust the Canny low and high thresholds to change which edges are detected.
   The low threshold remains below the high threshold.
4. Choose the line thickness and pen color.
5. Click **Create Sketch** to open a preview.
6. Click **Save as PNG** or **Save as EPS** to export the sketch.

The image is converted to grayscale and blurred before Canny edge detection.
The preview and PNG export use a white background.
