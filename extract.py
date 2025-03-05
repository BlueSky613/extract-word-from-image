import cv2
import pytesseract
import csv
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_path = 'Lorem1.png'
image = cv2.imread(image_path)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])
mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)
red_text_image = cv2.bitwise_and(image, image, mask=red_mask)
gray_image = cv2.cvtColor(red_text_image, cv2.COLOR_BGR2GRAY)
thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
denoised_image = cv2.GaussianBlur(thresh_image, (5, 5), 0)
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(red_mask, config=custom_config)
target_sentence = text.split('\n')
img_height, img_width, channels = image.shape
data = pytesseract.image_to_data(red_mask, output_type=pytesseract.Output.DICT)
for j in range(len(target_sentence)):
    if target_sentence[j] != "":
        words = target_sentence[j].split()
        print(words)
        coordinates = []
        for i in range(len(data['text'])):
            if data['text'][i].lower() == words[0].lower():
                if data['text'][i + len(words) - 1].lower() == words[len(words) - 1].lower():
                    x1 = data['left'][i]
                    y1 = data['top'][i]
                    width1 = data['width'][i]
                    height1 = data['height'][i]
                    x2 = data['left'][i + len(words) - 1]
                    y2 = data['top'][i + len(words) - 1]
                    width2 = data['width'][i + len(words) - 1]
                    height2 = data['height'][i + len(words) - 1]
                    coordinates.append((x1, y1, width1, height1, x2, y2, width2, height2))
                    break
        csv_file_path = "Lorem1.csv"
        if coordinates:
            for coord in coordinates:
                with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([target_sentence[j], (coord[0] + coord[4] + coord[6])/2, img_height-(coord[1] + coord[3]/2)])
                print(f"Coordinates of the sentence '{words}':")
                print(f"X={coord[0]}, Y={coord[1]}")

        else:
            print(f"The sentence '{target_sentence}' was not found in the image.")
    else:
        continue
