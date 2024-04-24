import easyocr
import cv2
import os
from tqdm import tqdm
import numpy as np
import json
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
with open('data.json', 'r') as file:
    data = json.load(file)
    print(data[-1])
s = ""
t = data[-1]
    #mixed_data/frames_Sequoia Capital
    #count = 0
path = f"mixed_data/frames_{t['Author']}/{t['Title']}"
for img in tqdm(os.listdir(path), desc=f'Processing images for {t["Author"]}'):
    img_path = os.path.join(path,img)
    result = reader.readtext(img_path)
    # Load the image
    #image = cv2.imread("mixed_data/frames_Sequoia Capital/frame0049.png")
    # Draw bounding boxes on the image
    for box in result:
        # Extract coordinates, label, and confidence
        points, label, _ = box
        s = s+label
    #     # Convert points to numpy array
    #     points = np.array(points)
    #     # Define the color of the rectangle in BGR format (Blue, Green, Red)
    #     color = (0, 255, 0)  # Green color

    #     # Define the thickness of the rectangle border
    #     thickness = 2

    #     # Draw the rectangle on the image
    #     cv2.rectangle(image, (int(points[0][0]),int(points[0][1])), (int(points[2][0]),int(points[2][0])), color, thickness)
    #     # Draw the bounding box
    #     #cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
    #     # Put label on the bounding box
    #     #cv2.putText(image, label, (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # # # Display the image
    # # cv2.imwrite(os.path.join("temp_output", f"image_with_bounding_boxes{count}.jpg"), image)
    # # count+=1
print(s)
with open(f"mixed_data/output_{t['Author']}/" + f"ocr_{t['Title']}_text.txt", "w") as file:
    file.write(s)
file.close()

    # cv2.imshow("Image with Bounding Boxes", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
