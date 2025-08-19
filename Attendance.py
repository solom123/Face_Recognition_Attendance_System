# Attendance.py
# Author: Purushottam (@creativepurus)
# Facial Recognition Attendance System (Stable Windows version)

import os
import sys
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import face_recognition
import time

# -----------------------
# Configurable parameters (override via environment variables)
# -----------------------
IMAGES_PATH = os.environ.get("IMAGES_PATH", "Images")                   # Folder with known faces
OUTPUT_CSV = os.environ.get("ATTENDANCE_FILE", "Attendance.csv")        # Base CSV filename
USE_DAILY_ROTATION = os.environ.get("DAILY_ROTATION", "0") == "1"       # "1" to write per-day CSV
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", "0"))                 # Webcam index
FRAME_SCALE = float(os.environ.get("FRAME_SCALE", "0.25"))              # 0.25 for speed
DETECTION_MODEL = os.environ.get("DETECTION_MODEL", "hog")              # "hog" or "cnn"
DISTANCE_THRESHOLD = float(os.environ.get("DISTANCE_THRESHOLD", "0.50"))# Stricter than default 0.6
NO_GUI = os.environ.get("NO_GUI", "0") == "1"                           # Headless mode if "1"
# Choose explicit Windows capture backend: "default", "msmf", "dshow"
VIDEO_BACKEND = os.environ.get("VIDEO_BACKEND", "default").lower()

REQUIRED_COLUMNS = ["Name", "Date", "Time"]

# -----------------------
# Helpers
# -----------------------
def ensure_images_path(path: str) -> None:
    if not os.path.isdir(path):
        print(f"❌ Images directory not found: {path}")
        sys.exit(1)

def load_or_init_csv(csv_path: str) -> pd.DataFrame:

    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)

            if not all(col in df.columns for col in REQUIRED_COLUMNS):
                print("⚠️ CSV schema mismatch. Reinitializing with required columns.")
                df = pd.DataFrame(columns=REQUIRED_COLUMNS)

        except Exception as e:
            print(f"⚠️ Failed to read CSV ({csv_path}): {e}. Reinitializing.")
            df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    else:
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)

    return df

def get_output_csv_for_today(default_csv: str) -> str:
    if not USE_DAILY_ROTATION:
        return default_csv
    date_str = datetime.now().strftime("%Y-%m-%d")
    base, ext = os.path.splitext(default_csv)
    if ext == "":
        ext = ".csv"
    return f"{base}_{date_str}{ext}"

def save_attendance(df: pd.DataFrame, csv_path: str) -> None:
    try:
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"❌ Failed to write attendance CSV: {e}")

def print_config():
    print("= Configuration =")
    print(f"Images path:         {IMAGES_PATH}")
    print(f"Attendance CSV:      {OUTPUT_CSV} (daily rotation: {USE_DAILY_ROTATION})")
    print(f"Camera index:        {CAMERA_INDEX}")
    print(f"Frame scale:         {FRAME_SCALE}")
    print(f"Detection model:     {DETECTION_MODEL}")
    print(f"Distance threshold:  {DISTANCE_THRESHOLD}")
    print(f"Video backend:       {VIDEO_BACKEND}")
    print(f"NO_GUI (headless):   {NO_GUI}")
    print("====")

def safe_label_from_filename(filename) -> str:
    if not isinstance(filename, str):
        print(f"⚠️ Non-string filename encountered: type={type(filename)} value={filename}")
        filename = str(filename)
    base, _ = os.path.splitext(filename)
    label = base.replace('_', ' ').strip()
    label = label.title()
    return label

# -----------------------
# Load known faces
# -----------------------
def load_known_faces(images_path: str):
    print("📂 Loading known faces...")
    known_encodings = []
    known_names = []

    try:
        files = os.listdir(images_path)
    except Exception as e:
        print(f"❌ Cannot list images in {images_path}: {e}")
        sys.exit(1)

    image_files = [f for f in files if isinstance(f, str) and f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not image_files:
        print("❌ No images found in Images/ folder.")
        sys.exit(1)

    for filename in image_files:
        image_path = os.path.join(images_path, filename)
        try:
            image = face_recognition.load_image_file(image_path)
            # Detect faces using selected model
            face_locations = face_recognition.face_locations(image, model=DETECTION_MODEL)
            face_encs = face_recognition.face_encodings(image, face_locations)

            if len(face_encs) == 0:
                print(f"⚠️ No face found in {filename} — skipping.")
                continue
            if len(face_encs) > 1:
                print(f"⚠️ Multiple faces found in {filename} — skipping for unambiguous enrollment.")
                continue

            encoding = face_encs[0]
            label = safe_label_from_filename(filename)

            known_encodings.append(encoding)
            known_names.append(label)
            print(f"✅ Encoding loaded for '{filename}' as '{label}'")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    if not known_encodings:
        print("❌ No valid faces loaded from Images/. Exiting.")
        sys.exit(1)

    print(f"✅ {len(known_names)} known faces loaded: {known_names}")
    return known_encodings, known_names

# -----------------------
# Recognition utilities
# -----------------------
def best_match_name(known_encodings, known_names, face_encoding, threshold=DISTANCE_THRESHOLD):
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    if len(distances) == 0:
        return "Unknown", None
    best_idx = int(np.argmin(distances))
    best_distance = float(distances[best_idx])
    if best_distance < threshold:
        return known_names[best_idx], best_distance
    return "Unknown", best_distance

def open_video_capture(index: int, backend: str):
    if backend == "msmf":
        cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
    elif backend == "dshow":
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(index)
    return cap

# -----------------------
# Main
# -----------------------
def main():
    print_config()
    ensure_images_path(IMAGES_PATH)

    known_face_encodings, known_face_names = load_known_faces(IMAGES_PATH)

    current_csv_path = get_output_csv_for_today(OUTPUT_CSV)
    attendance_df = load_or_init_csv(current_csv_path)

    print("🔎 Attempting to open webcam...")
    video_capture = open_video_capture(CAMERA_INDEX, VIDEO_BACKEND)
    if not video_capture.isOpened():
        print("❌ Cannot open webcam. Exiting.")
        sys.exit(1)

    # Optional: Warm-up frames to avoid zeroed first frames
    for _ in range(5):
        ret, _ = video_capture.read()
        if not ret:
            break

    print("✅ Webcam detected. Starting attendance system...")
    print("Press 'q' to quit.")

    if not NO_GUI:
        # Create the window explicitly (helps on Win32 HighGUI)
        try:
            cv2.namedWindow("Attendance System", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        except Exception as e:
            print(f"⚠️ Could not create window (running headless instead): {e}")
            # Force headless for this run
            no_gui_runtime = True
        else:
            no_gui_runtime = False
    else:
        no_gui_runtime = True

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("❌ Failed to grab frame.")
                break

            # Resize frame for speed
            small_frame = cv2.resize(frame, (0, 0), fx=FRAME_SCALE, fy=FRAME_SCALE)
            if small_frame.size == 0:
                # Defensive: skip empty frames
                if not no_gui_runtime:
                    cv2.imshow("Attendance System", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("🚪 Exiting...")
                        break
                continue

            # Convert to RGB explicitly (robust on older OpenCV)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the small RGB frame
            face_locations = face_recognition.face_locations(rgb_small_frame, model=DETECTION_MODEL)

            if not face_locations:
                # No faces this frame: show/update window or just loop
                if not no_gui_runtime:
                    cv2.imshow("Attendance System", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("🚪 Exiting...")
                        break
                continue

            # Compute encodings with guard against transient failures
            try:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            except Exception as e:
                print(f"⚠️ face_encodings failed this frame: {e}")
                if not no_gui_runtime:
                    cv2.imshow("Attendance System", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("🚪 Exiting...")
                        break
                continue

            # Iterate detected faces
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name, dist = best_match_name(known_face_encodings, known_face_names, face_encoding, DISTANCE_THRESHOLD)

                if name != "Unknown":
                    now = datetime.now()
                    date_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H:%M:%S")

                    # Handle daily rotation across midnight
                    new_csv_path = get_output_csv_for_today(OUTPUT_CSV)
                    if new_csv_path != current_csv_path:
                        current_csv_path = new_csv_path
                        attendance_df = load_or_init_csv(current_csv_path)

                    # Ensure dedup by Name+Date
                    already = False
                    if not attendance_df.empty:
                        already = ((attendance_df["Name"] == name) & (attendance_df["Date"] == date_str)).any()

                    if not already:
                        new_entry = {"Name": name, "Date": date_str, "Time": time_str}
                        attendance_df = pd.concat([attendance_df, pd.DataFrame([new_entry])], ignore_index=True)
                        save_attendance(attendance_df, current_csv_path)
                        if dist is not None:
                            print(f"📝 Attendance marked: {name} at {time_str} on {date_str} (dist={dist:.3f})")
                        else:
                            print(f"📝 Attendance marked: {name} at {time_str} on {date_str}")

                # Draw rectangle and label on original-size frame
                inv_scale = int(round(1.0 / FRAME_SCALE))
                top, right, bottom, left = [int(v * inv_scale) for v in (top, right, bottom, left)]
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            # Show window (unless headless)
            if not no_gui_runtime:
                cv2.imshow("Attendance System", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("🚪 Exiting...")
                    break

            else:
                # Headless: avoid busy-looping CPU at 100%
                time.sleep(0.005)

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")
    finally:
        video_capture.release()
        if not no_gui_runtime:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass
        print("✅ Webcam released. Goodbye!")

if __name__ == "__main__":
    main()
