# import cv2
# import pytesseract
# import numpy as np
# # Set the path to the Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# # Load the image
# image_path = 'Lorem2.png'  # Update with your image path
# image = cv2.imread(image_path)
# # Convert the image to HSV color space
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# # Define the lower and upper bounds for red color in HSV
# lower_red1 = np.array([0, 100, 100])    # Lower bound for red
# upper_red1 = np.array([10, 255, 255])   # Upper bound for red
# lower_red2 = np.array([160, 100, 100])  # Lower bound for red (second range)
# upper_red2 = np.array([180, 255, 255])  # Upper bound for red (second range)
# # Create masks for red color
# mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
# mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
# red_mask = cv2.bitwise_or(mask1, mask2)
# # Apply the mask to the original image
# red_text_image = cv2.bitwise_and(image, image, mask=red_mask)
# # Convert to grayscale
# gray_image = cv2.cvtColor(red_text_image, cv2.COLOR_BGR2GRAY)
# # Use adaptive thresholding for better results
# thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                      cv2.THRESH_BINARY, 11, 2)
# # Denoise the image
# denoised_image = cv2.GaussianBlur(thresh_image, (5, 5), 0)
# # OCR using Tesseract
# custom_config = r'--oem 3 --psm 6'  # Adjust PSM as needed
# text = pytesseract.image_to_string(red_mask, config=custom_config)
# data = pytesseract.image_to_data(red_mask, output_type=pytesseract.Output.DICT)
# for i in range(len(data['text'])):
#      print(text.split('\n'))

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load the image
image = cv2.imread('Lorem1.png')

# Convert the image to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range for red color and create mask
lower_red = (0, 100, 100)
upper_red = (10, 255, 255)
mask1 = cv2.inRange(hsv_image, lower_red, upper_red)

lower_red = (160, 100, 100)
upper_red = (180, 255, 255)
mask2 = cv2.inRange(hsv_image, lower_red, upper_red)

# Combine masks
mask = mask1 + mask2

# Apply mask to get only red color parts
red_only = cv2.bitwise_and(image, image, mask=mask)

# Convert image to RGB (for pytesseract compatibility)
rgb_image = cv2.cvtColor(red_only, cv2.COLOR_BGR2RGB)

# Perform OCR
custom_config = r'--oem 3 --psm 6'  # using tesseract config for better recognition
details = pytesseract.image_to_data(rgb_image, output_type=pytesseract.Output.DICT, config=custom_config)

# Iterate through detected text boxes and print their positions
n_boxes = len(details['text'])
for i in range(n_boxes):
    if int(details['conf'][i]) > 60:  # Confidence threshold
        (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
        print(f"Detected word: {details['text'][i]} at X: {x}, Y: {y}")

# Optionally display the image with detected words highlighted
for i in range(n_boxes):
    if int(details['conf'][i]) > 60:
        (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('Red Text Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
