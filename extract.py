import cv2
import pytesseract
import csv

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_path = 'Lorem2.png'
image = cv2.imread(image_path)
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
target_sentence = 'Adsfadstdsat'
coordinates = []
for i in range(len(data['text'])):
     if data['text'][i].lower() == target_sentence.lower():
        x = data['left'][i]
        y = data['top'][i]
        width = data['width'][i]
        height = data['height'][i]
        coordinates.append((x, y, width, height))
csv_file_path = "Lorem2.csv"
if coordinates:
    for coord in coordinates:
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([target_sentence, coord[0], coord[1]])
        print(f"Coordinates of the sentence '{target_sentence}':")
        print(f"X={coord[0]}, Y={coord[1]}")

else:
    print(f"The sentence '{target_sentence}' was not found in the image.")
