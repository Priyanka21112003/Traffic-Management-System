import cv2
import numpy as np

# Load YOLOv4 network
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Initialize global counters for vehicle counts
two_wheeler_count = 0
car_count = 0
bus_count = 0
truck_count = 0

# List to store detected vehicle positions for tracking
tracked_positions = []

# Function to detect and count vehicles without double-counting
def detect_vehicle_yolo(frame, line_position, tracking_distance=50):
    global two_wheeler_count, car_count, bus_count, truck_count

    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers = net.getUnconnectedOutLayersNames()
    detections = net.forward(output_layers)

    new_positions = []  # Track current frame's new vehicle positions

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in ["car", "motorbike", "bus", "truck"]:
                # Get bounding box coordinates
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, w, h) = box.astype("int")
                x = int(centerX - w / 2)
                y = int(centerY - h / 2)

                # Check if vehicle has already been counted
                new_position = (centerX, centerY)
                if any(np.linalg.norm(np.array(new_position) - np.array(p)) < tracking_distance for p in tracked_positions):
                    continue  # Skip if position is close to previously detected vehicles

                # Draw bounding box and label
                color = (0, 255, 0) if classes[class_id] == "car" else (255, 0, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, classes[class_id], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Count vehicles if they cross the line
                if y + h > frame.shape[0] - line_position:
                    if classes[class_id] == "motorbike":
                        two_wheeler_count += 1
                    elif classes[class_id] == "car":
                        car_count += 1
                    elif classes[class_id] == "bus":
                        bus_count += 1
                    elif classes[class_id] == "truck":
                        truck_count += 1

                    # Add new position to tracking list to avoid double-counting
                    new_positions.append(new_position)

    # Update tracked positions for the current frame
    tracked_positions.extend(new_positions)

    # Display counts
    cv2.putText(frame, f"Two-Wheelers: {two_wheeler_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(frame, f"Cars: {car_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Buses: {bus_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Trucks: {truck_count}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame

# Video capture and processing loop
cap = cv2.VideoCapture('bikes.mp4')
line_position = 50

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result_frame = detect_vehicle_yolo(frame, line_position)
    cv2.imshow('Vehicle Detection', result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
