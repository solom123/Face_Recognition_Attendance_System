# Attendance.py
# Author: Purushottam (creativepurus)
# Facial Recognition Attendance System

import face_recognition
import cv2
import os
import pandas as pd
from datetime import datetime

IMAGES_PATH = "Images"
ATTENDANCE_FILE = "Attendance.csv"

# Load known faces
known_face_encodings = []
known_face_names = []

print("📂 Loading known faces...")
for filename in os.listdir(IMAGES_PATH):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(IMAGES_PATH, filename)
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if len(face_encodings) > 0:
                label = os.path.splitext(filename)[0].replace('_', ' ').title()
                known_face_encodings.append(face_encodings)
                known_face_names.append(label)
                print(f"✅ Found face and encoding for {filename} as '{label}'")
            else:
                print(f"⚠️ No face found in {filename}")
        except Exception as e:
            print(f"❌ Error with {filename}: {e}")

if not known_face_encodings:
    print("❌ No valid faces found from the images. Exiting.")
    exit()
print(f"✅ {len(known_face_names)} known faces loaded: {known_face_names}")

# Load or create attendance.csv
if os.path.exists(ATTENDANCE_FILE):
    attendance_df = pd.read_csv(ATTENDANCE_FILE)
else:
    attendance_df = pd.DataFrame(columns=["Name", "Date", "Time"])

# Open webcam
print("🔎 Attempting to open webcam...")
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("❌ Cannot open webcam. Exiting.")
    exit()
print("✅ Webcam detected. Starting attendance system...")
print("Press 'q' to quit.")

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                already_recorded = (
                    (attendance_df["Name"] == name) &
                    (attendance_df["Date"] == date_str)
                ).any()
                if not already_recorded:
                    new_entry = {"Name": name, "Date": date_str, "Time": time_str}
                    attendance_df = pd.concat([attendance_df, pd.DataFrame([new_entry])], ignore_index=True)
                    attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                    print(f"📝 Attendance marked: {name} at {time_str} on {date_str}")

            top, right, bottom, left = [v * 4 for v in (top, right, bottom, left)]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🚪 Exiting...")
            break
except Exception as e:
    print(f"⚠️ Error occurred: {e}")

finally:
    video_capture.release()
    cv2.destroyAllWindows()
    print("✅ Webcam released. Goodbye!")