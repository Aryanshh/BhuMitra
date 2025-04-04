import time
import numpy as np
import board
import busio
import adafruit_mlx90640
import matplotlib.pyplot as plt
import cv2

def initialize_camera():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # Setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c)  # Initialize the thermal camera
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # Set refresh rate
    return mlx

def capture_frame(mlx):
    frame = np.zeros((24*32,))  # MLX90640 has 24x32 resolution
    try:
        mlx.getFrame(frame)  # Capture thermal frame
    except ValueError:
        pass  # Skip frame if error
    return np.reshape(frame, (24, 32))

def analyze_crop_health(thermal_image):
    avg_temp = np.mean(thermal_image)
    print(f"Average Crop Temperature: {avg_temp:.2f}°C")
    
    # Define temperature thresholds for healthy vs. stressed crops
    healthy_range = (20, 30)  # Example healthy crop temperature range
    
    if avg_temp < healthy_range[0]:
        print("Crops may be under-watered or stressed due to cold.")
    elif avg_temp > healthy_range[1]:
        print("Crops may be heat-stressed, check irrigation.")
    else:
        print("Crops are in a healthy temperature range.")

def display_thermal_image(thermal_image):
    plt.imshow(thermal_image, cmap='inferno')
    plt.colorbar(label='Temperature (°C)')
    plt.title("Thermal Crop Detection")
    plt.show()

if __name__ == "__main__":
    mlx = initialize_camera()
    print("Thermal camera initialized. Capturing crop data...")
    
    while True:
        thermal_image = capture_frame(mlx)
        analyze_crop_health(thermal_image)
        display_thermal_image(thermal_image)
        time.sleep(5)  # Delay between captures
