import face_recognition
import cv2

# Open webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Cannot open webcam")
    exit()

print("✅ Webcam detected")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Convert frame from BGR to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations
    face_locations = face_recognition.face_locations(rgb_frame)

    # Draw rectangles around faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()