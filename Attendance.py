# Attendance.py
# Author: Purushottam (creativepurus)
# Facial Recognition Attendance System

# Attendance.py
import cv2
import face_recognition
import os
import pandas as pd
from datetime import datetime

# -------------------------------
# CONFIGURATION
# -------------------------------
IMAGES_PATH = "Images"             # Folder containing known faces
ATTENDANCE_FILE = "Attendance.csv"  # CSV file to store attendance

# -------------------------------
# LOAD KNOWN FACES
# -------------------------------

known_face_encodings = []
known_face_names = []

print("📂 Loading known faces...")

for filename in os.listdir(IMAGES_PATH):
    if filename.endswith(('.jpg', '.png')):
        image_path = os.path.join(IMAGES_PATH, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename))
        else:
            print(f"⚠️ No face found in {filename}")

print(f"✅ {len(known_face_names)} known faces loaded: {known_face_names}")

# -------------------------------
# INITIALIZE ATTENDANCE CSV
# -------------------------------

if os.path.exists(ATTENDANCE_FILE):
    attendance_df = pd.read_csv(ATTENDANCE_FILE)
    for col in ["Name", "Date", "Time"]:
        if col not in attendance_df.columns:
            attendance_df[col] = ""
else:
    attendance_df = pd.DataFrame(columns=["Name", "Date", "Time"])
    attendance_df.to_csv(ATTENDANCE_FILE, index=False)

# -------------------------------
# START WEBCAM
# -------------------------------

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("❌ Cannot open webcam")
    exit()

print("✅ Webcam detected. Starting attendance system...")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB

    # Detect faces and get encodings in one step
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Record attendance if not already for today
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            if not ((attendance_df['Name'] == name) & (attendance_df['Date'] == date_str)).any():
                attendance_df = pd.concat(
                    [attendance_df, pd.DataFrame([[name, date_str, time_str]], columns=["Name", "Date", "Time"])],
                    ignore_index=True
                )
                attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                print(f"📝 Attendance marked: {name} at {time_str} on {date_str}")

        # Scale locations back up for original frame
        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.imshow('Attendance System', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🚪 Exiting...")
        break

# Release webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
