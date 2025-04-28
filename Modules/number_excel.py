import csv
import os
import datetime
import cv2
import requests

# Function to get the plate text using Plate Recognizer API
def recognize_plate(frame):
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    response = requests.post(
        'api url will be here',
        files=dict(upload=img_bytes),
        data=dict(regions='fr'),
        headers={'Authorization': 'Token ' + 'api code'}
    )

    result = response.json()
    if 'results' in result and len(result['results']) > 0:
        plate = result['results'][0]['plate']
        box = result['results'][0]['box']
        xmins, ymins, ymaxs, xmaxs = box['xmin'], box['ymin'], box['ymax'], box['xmax']
        return plate, (xmins, ymins, xmaxs, ymaxs)
    return None, None

# Function to process and save the plate info
def main():
    # Define the video path and CSV file path
    video_path = 'heyyy.mp4'  # Update with your video file path
    csv_path = "D:\Traafic\minor\ANPR Dataset\number.csv"
    plates_dir = "D:\Traafic\minor\ANPR Dataset\Plates"

    # Ensure the Plates directory exists
    if not os.path.exists(plates_dir):
        os.makedirs(plates_dir)

    # Check if the CSV file exists and create it if necessary
    if not os.path.isfile(csv_path):
        try:
            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Time", "Plate"])
        except Exception as e:
            print(f"Error creating CSV file: {e}")
            return

    # Start the video capture
    cap = cv2.VideoCapture(video_path)

    count = 0
    max_attempts = 5  # Limit to 5 successful recognitions

    while True:
        ret, frame = cap.read()

        if not ret:
            print("End of video or error.")
            break

        plate, box = recognize_plate(frame)

        if plate:
            count += 1
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H-%M-%S")  # Replace colons with hyphens for valid filenames

            # Draw bounding box and plate text on the frame
            if box:
                xmins, ymins, xmaxs, ymaxs = box
                cv2.rectangle(frame, (xmins, ymins), (xmaxs, ymaxs), (255, 0, 0), 2)
                cv2.putText(frame, plate.lower(), (xmins, ymins - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Resize the frame to make it more visible
            frame_resized = cv2.resize(frame, (800, 600))  # You can change the dimensions here

            # Display the resized frame
            cv2.imshow('Video Plate Recognition', frame_resized)

            # Write the plate data to the CSV file
            try:
                with open(csv_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([f"Plate {count}", date_str, time_str, plate.lower()])
                print(f"Saved Plate {count}: {plate.lower()} on {date_str} at {time_str}")
            except Exception as e:
                print(f"Error saving to CSV: {e}")

            # Save the plate image
            if box:
                xmins, ymins, xmaxs, ymaxs = box
                img_roi = frame[ymins:ymaxs, xmins:xmaxs]  # Crop the region of interest (plate)
                
                # Ensure the path exists and save the cropped plate image
                img_path = os.path.join(plates_dir, f"image_{count}_{date_str}_{time_str}.jpg")
                print(f"Attempting to save plate image at: {img_path}")  # Debug print

                # Save the image and check if it was successful
                if cv2.imwrite(img_path, img_roi):
                    print(f"Plate image successfully saved at: {img_path}")
                else:
                    print(f"Failed to save plate image at: {img_path}")

            # Break after 5 successful attempts
            if count >= max_attempts:
                print("5 plates detected, exiting...")
                break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
