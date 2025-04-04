import cv2
import numpy as np
import matplotlib.pyplot as plt

def capture_image(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        print("Failed to capture image.")
        return None

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def calculate_ndvi(nir_image, red_image):
    nir = nir_image.astype(float)
    red = red_image.astype(float)
    ndvi = (nir - red) / (nir + red + 1e-10)  # Avoid division by zero
    return ndvi

def display_ndvi(ndvi):
    plt.imshow(ndvi, cmap='RdYlGn')  # Green = healthy, Red = stressed
    plt.colorbar(label='NDVI Value')
    plt.title("NDVI Crop Health Analysis")
    plt.show()

if __name__ == "__main__":
    print("Capturing multispectral images...")
    rgb_image = capture_image(camera_id=0)  # Normal RGB camera
    nir_image = capture_image(camera_id=1)  # Near-infrared camera
    
    if rgb_image is not None and nir_image is not None:
        red_band = convert_to_grayscale(rgb_image)  # Extract Red channel
        nir_band = convert_to_grayscale(nir_image)  # Extract NIR channel
        
        ndvi_result = calculate_ndvi(nir_band, red_band)
        display_ndvi(ndvi_result)
    else:
        print("Error capturing multispectral images.")
