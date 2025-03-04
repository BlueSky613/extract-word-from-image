import cv2
import pytesseract
import csv

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kk\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_path = 'Lorem2.png'
image = cv2.imread(image_path)
img_height, img_width, channels = image.shape
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
target_sentence = 'Adsfadstdsat'
words = target_sentence.split()
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
csv_file_path = "Lorem2.csv"
if coordinates:
    for coord in coordinates:
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([target_sentence, (coord[0] + coord[4] + coord[6])/2, img_height-(coord[1] + coord[3]/2)])
        print(f"Coordinates of the sentence '{target_sentence}':")
        print(f"X={coord[0]}, Y={coord[1]}")

else:
    print(f"The sentence '{target_sentence}' was not found in the image.")
