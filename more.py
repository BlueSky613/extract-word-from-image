import cv2
import pytesseract
import numpy as np
# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# Load the image
image_path = 'Lorem2.png'  # Update with your image path
image = cv2.imread(image_path)
# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Define the lower and upper bounds for red color in HSV
lower_red1 = np.array([0, 100, 100])    # Lower bound for red
upper_red1 = np.array([10, 255, 255])   # Upper bound for red
lower_red2 = np.array([160, 100, 100])  # Lower bound for red (second range)
upper_red2 = np.array([180, 255, 255])  # Upper bound for red (second range)
# Create masks for red color
mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)
# Apply the mask to the original image
red_text_image = cv2.bitwise_and(image, image, mask=red_mask)
# Convert to grayscale
gray_image = cv2.cvtColor(red_text_image, cv2.COLOR_BGR2GRAY)
# Use adaptive thresholding for better results
thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
# Denoise the image
denoised_image = cv2.GaussianBlur(thresh_image, (5, 5), 0)
# OCR using Tesseract
custom_config = r'--oem 3 --psm 6'  # Adjust PSM as needed
text = pytesseract.image_to_string(red_mask, config=custom_config)
data = pytesseract.image_to_data(red_mask, output_type=pytesseract.Output.DICT)
for i in range(len(data['text'])):
     print(text)