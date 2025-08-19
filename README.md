# 👨🎓 Facial Recognition Attendance System (Windows 11 Ready)

A Python-based attendance system that uses Face Recognition to automatically mark attendance by detecting and recognizing faces from a live webcam feed.
- This README includes an installer-like setup specifically tuned for Windows 11 (64-bit), Conda environments, and common OpenCV/dlib pitfalls.

***

## 🚀 Features

- ✅ Real-time face detection and recognition using OpenCV and dlib
- ✅ Automatically logs recognized faces into an Excel/CSV attendance file
- ✅ One-entry-per-person-per-day de-duplication
- ✅ Robust Windows 11 setup with GUI and headless modes
- ✅ Simple and lightweight Python-based solution
- ✅ Well-suited for educational institutions and offices

***

## 🛠️ Tech Stack

- Python 3.8+ (Recommended: 3.8, for dlib/face_recognition compatibility)
- Conda – Preferred environment manager
- OpenCV – Camera input & image processing (Win32 HighGUI preferred on Windows)
- dlib – Face encoding model (via conda)
- face_recognition – High-level API for face encodings & matching (via pip)
- pandas – Attendance logging
- CSV (and optional per-day rotation) – Output files

***

## 📦 Installation (Windows 11 x64 - Recommended)

This flow avoids build headaches and GUI crashes on Windows:

1) Clone the repository

```bash
git clone https://github.com/creativepurus/Face_Recognition_Attendance_System.git
cd Face_Recognition_Attendance_System
```

2) Create & activate Conda environment

```bash
conda create -n face_attend python=3.8 -y
conda activate face_attend
```

3) Install core dependencies with conda (dlib, OpenCV, pandas, numpy)

```bash
conda install -c conda-forge dlib opencv pandas numpy -y
```

4) Install face_recognition with pip (after dlib via conda)

```bash
pip install face_recognition
```

Notes:
- Install dlib via conda first, then install face_recognition via pip to avoid ABI conflicts.
- If using a Qt-built OpenCV that crashes with “Could not find the Qt platform plugin 'windows'”, prefer an OpenCV build with Win32 HighGUI (typical with conda). Headless mode is also available (see below).

Optional: verify OpenCV build (Win32 HighGUI recommended on Windows)

```bash
python -c "import cv2; print(cv2.__version__); print(cv2.getBuildInformation().splitlines()[0])"
```

You should see a GUI section indicating Win32 UI (older builds) or a working Qt6 runtime. If Qt errors occur, see Troubleshooting.

***

## ▶️ Usage

Run the attendance system:

```bash
python Attendance.py
```

Environment variables (optional):

- CAMERA_INDEX: Select camera (default 0)
- FRAME_SCALE: Downscale for performance (default 0.25)
- DETECTION_MODEL: hog (default) or cnn
- DISTANCE_THRESHOLD: Recognition acceptance threshold (default 0.50)
- ATTENDANCE_FILE: CSV path (default Attendance.csv)
- DAILY_ROTATION: “1” to write per-day CSV (Attendance_YYYY-MM-DD.csv)
- VIDEO_BACKEND: “default”, “msmf” (Media Foundation), or “dshow” (DirectShow)
- NO_GUI: “1” to run headless (no window, useful for servers/kiosks)

Examples (PowerShell):

```powershell
$env:VIDEO_BACKEND="msmf"           # Use Media Foundation on Windows 11
$env:DISTANCE_THRESHOLD="0.55"      # Slightly more permissive
$env:DAILY_ROTATION="1"             # Per-day CSV files
python Attendance.py
```

Headless mode:

```powershell
$env:NO_GUI="1"
python Attendance.py
```

### Workflow

1. The webcam opens and starts detecting faces.
2. Known faces (from the Images folder) are recognized.
3. Attendance is recorded in CSV with:
   - Name
   - Date
   - Time
4. Only one entry per person per day is written (de-duplication).
5. Press q to quit if running with a window.

***

## 📂 Project Structure

```
Face_Recognition_Attendance_System/
│── Attendance.py             # Main application file (robust Windows handling)
│── test_face.py              # Script to test face encoding/detection
│── test_installation.py      # Script to test setup and installation
│── environment.yml           # Conda environment/dependencies file (optional)
│── Attendance.csv            # File where attendance is saved (default)
│── README.md                 # Documentation
│── LICENSE                   # Project license
│── .gitignore                # Git ignore file
│── Images/                   # Folder containing known faces
```

Enrollment guidance:
- Put 1–3 clear, frontal images per person into Images/.
- Each image must contain exactly one face. Multi-face or no-face images are skipped.
- Filenames become labels (e.g., “Anand_Photo_1.jpg” → “Anand Photo 1”).

***

## 📊 Example Attendance Output

| Name          | Date       | Time     |
| ------------- | ---------- | -------- |
| Obama         | 2025-08-18 | 09:32:14 |
| Sample 1      | 2025-08-18 | 09:35:02 |

With DAILY_ROTATION=1, files are written as Attendance_YYYY-MM-DD.csv.

***

## 🛡️ Requirements

- **Python 3.8 (recommended for face_recognition/dlib)**
  - [Python 3.8 for Windows, Mac, and Linux (official archive)](https://www.python.org/downloads/release/python-380/)

- **C++ Build Tools (required for manual dlib/face_recognition builds on Windows)**
  - [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    - During install, select “C++ build tools” workload, including the recommended defaults.

- **Conda (Anaconda or Miniconda)**
  - [Anaconda Download](https://www.anaconda.com/download)  
    *(Full distribution)*
  - [Miniconda Download](https://docs.conda.io/en/latest/miniconda.html)  
    *(Minimal installer for conda)*

### These are the official and most reliable sources for each requirement.

***

## ⚙️ Windows 11 Tips and Backend Notes

- Prefer conda-forge OpenCV (installed via conda) so HighGUI works out-of-the-box.

- If the camera is flaky to open, set a specific backend:
  - VIDEO_BACKEND=msmf (Media Foundation, recommended on Windows 10/11)
  - VIDEO_BACKEND=dshow (DirectShow, alternative)

- The app includes:
  - Camera warm-up frames (reduces initial black frames)
  - Robust RGB conversion (cv2.cvtColor)
  - Defensive handling of transient invalid frames (skips gracefully)

- Headless mode (NO_GUI=1) avoids GUI entirely and is reliable on servers/kiosks.

***

## 🧪 Quick Self-Tests

- OpenCV HighGUI test:

```powershell
python -c "import cv2, numpy as np; img=np.zeros((200,300,3),dtype=np.uint8); cv2.namedWindow('t'); cv2.imshow('t',img); cv2.waitKey(800); cv2.destroyAllWindows()"
```

- Camera backend switch:

```powershell
$env:VIDEO_BACKEND="msmf"
python Attendance.py
```

- Adjust threshold if genuine matches show as Unknown:

```powershell
$env:DISTANCE_THRESHOLD="0.55"
python Attendance.py
```

***

## 🧹 Troubleshooting

- Qt platform plugin “windows” error (cv2.imshow crash):
  - Use an OpenCV build with Win32 HighGUI (typical with conda).
  - Or run headless: NO_GUI=1.
  - Avoid mixing pip OpenCV with conda OpenCV in the same env.

- compute_face_descriptor() or DLL errors:
  - Ensure dlib was installed via conda first, then install face_recognition via pip.

- No face detected in enrollment images:
  - Use clear, front-facing, unfiltered images with one face only.

- Duplicate daily entries:
  - The app prevents duplicates by Name+Date. If running multiple instances, consider centralizing CSV or using a database.

***

## 🔮 Future Improvements

- Multi-camera support
- Cloud database integration (Firebase / Supabase)
- Web dashboard for attendance monitoring
- SMS/Email notifications
- GUI enrollment tool and encoding cache for faster startup

***

## 🙌 Contribution

Pull requests are welcome! To contribute:
1. Fork the repo
2. Create a new branch
3. Commit changes
4. Open a Pull Request

***

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify.

***

## 👨💻 Author

Developed by **[creativepurus](https://github.com/creativepurus)** 🔥

## 👉🏻 [LinkedIn](https://linkedin.com/in/creativepurus) | [GitHub](https://github.com/creativepurus)
