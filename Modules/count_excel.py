import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# Video file path
cap = cv2.VideoCapture("bikes.mp4")

min_width_react = 80  # min width rectangle
min_height_react = 80  # min height rectangle

count_line_position = 550
algo = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True)

def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

detect = []
offset = 6  # Offset for counting line sensitivity
counter = 0

# Create a DataFrame to store the count
df = pd.DataFrame(columns=["date", "time", "count"])

while True:
    ret, frame1 = cap.read()
    
    # Check if the frame was read correctly
    if not ret:
        break

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    img_sub = algo.apply(blur) 
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw counting line
    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)
    
    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue
            
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)
        
        for (cx, cy) in detect:
            if cy < (count_line_position + offset) and cy > (count_line_position - offset):
                counter += 1
                detect.remove((cx, cy))
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                # Use pd.concat instead of append (as append is deprecated)
                new_row = pd.DataFrame({"date": [date], "time": [time], "count": [counter]})
                df = pd.concat([df, new_row], ignore_index=True)

                # Save the dataframe to an Excel file
                df.to_excel(r"D:\Traafic\minor\ANPR Dataset\vehicle_count.xlsx", index=False)
                
    # Display vehicle count on the frame
    cv2.putText(frame1, "VEHICLE COUNT : " + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    
    # Show the video frame
    cv2.imshow("Video Original", frame1)
    
    # Exit the loop if 'q' is pressed
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
        
# Release resources
cv2.destroyAllWindows()
cap.release()
