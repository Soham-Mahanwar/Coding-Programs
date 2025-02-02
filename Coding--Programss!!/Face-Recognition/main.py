import cv2
import os

# Load the Haar Cascade file
face_cascade = cv2.CascadeClassifier(r"D:\Soham\Coding--Programss!!\Face-Recognition\haarcascade_frontalface_default.xml")

# Check if the classifier loaded correctly
if face_cascade.empty():
    print("Error: Failed to load the Haar Cascade XML file.")
    exit()

# Start the webcam
webcam = cv2.VideoCapture(0)

# Create a directory to save photos (if it doesn't exist)
output_dir = "Captured_Photos"
os.makedirs(output_dir, exist_ok=True)

photo_count = 0  # Counter for photo filenames

while True:
    # Read frames from the webcam
    _, img = webcam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Display the frame
    cv2.imshow("Face Detection", img)

    # Capture keyboard input
    key = cv2.waitKey(10)

    if key == 27:  # ESC key to exit
        break
    elif key == ord('s'):  # 's' key to save photo
        photo_path = os.path.join(output_dir, f"photo_{photo_count}.jpg")
        cv2.imwrite(photo_path, img)
        print(f"Photo saved: {photo_path}")
        photo_count += 1

# Release the webcam and close the OpenCV windows
webcam.release()
cv2.destroyAllWindows()
