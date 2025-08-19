# 👨🎓 Facial Recognition Attendance System

A Python-based attendance system that uses **Face Recognition** to automatically mark attendance by detecting and recognizing faces from a live webcam feed.

***

## 🚀 Features

- ✅ Real-time face detection and recognition using **OpenCV** and **dlib**
- ✅ Automatically logs recognized faces into an **Excel/CSV attendance file**
- ✅ Simple and lightweight Python-based solution
- ✅ Well-suited for educational institutions and offices

***

## 🛠️ Tech Stack

- **Python 3.8+** (Recommended: 3.8, due to dlib/face_recognition compatibility)
- **Conda** – Preferred environment manager
- **OpenCV** – Camera input & image processing
- **dlib** – Face detection model (automatically installed via conda)
- **face_recognition** – High-level API for face encodings & matching
- **pandas** – Attendance logging
- **Excel/CSV** – Output files

***

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/creativepurus/Face_Recognition_Attendance_System.git
cd Face_Recognition_Attendance_System
```

### 2. Create & activate a Conda environment

```bash
conda create -n face_attend python=3.8 -y
conda activate face_attend
```

### 3. Install dependencies (Conda + pip hybrid, robust for Windows!)

```bash
# Install system-level libraries using conda
conda install -c conda-forge dlib opencv pandas numpy -y

# Install face_recognition via pip for the latest version (after conda dlib!)
pip install face_recognition
```

> ⚠️ **Note:**  
> - Installing `face_recognition` with pip after dlib via conda is crucial to avoid version conflicts.
> - If you see errors about missing DLLs (`cudnn*.dll`), ensure you installed with conda as above.

***

## ▶️ Usage

Run the attendance system:

```bash
python Attendance.py
```

### Workflow:

1. The webcam will open and start detecting faces.
2. Known faces (from the `Images` folder) will be recognized.
3. Attendance will be recorded automatically in a CSV file with:
    - Name
    - Date
    - Time

***

## 📂 Project Structure

```
Facial_Recognition_Attendance_System/
│── Attendance.py            # Main application file
│── test_face.py             # Script to test face encoding/detection
│── test_installation.py     # Script to test setup and installation
│── environment.yml          # Conda environment/dependencies file
│── Attendance.csv           # File where attendance is saved
│── README.md                # Documentation
│── LICENSE                  # Project license
│── .gitignore               # Git ignore file
│── Images/                  # Folder containing known faces
```

***

## 📊 Example Attendance Output

| Name           | Date       | Time     |
| -------------- | ---------- | -------- |
|    obama       | 2025-08-18 | 09:32:14 |
|    sample_1    | 2025-08-18 | 09:35:02 |

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

## ⚙️ Troubleshooting

- If you get `compute_face_descriptor()` or DLL errors, ensure you used **conda install dlib** and only then **pip install face_recognition**.
- Only use clear, front-facing, unfiltered images in your `Images/` folder.
- For optimal results, install and run in a dedicated conda environment as shown above.

***

## 🔮 Future Improvements

- Multi-camera support
- Cloud database integration (Firebase / Supabase)
- Web dashboard for attendance monitoring
- SMS/Email notifications

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

Developed by **[Purushottam (creativepurus)](https://github.com/creativepurus)** 🚀

[LinkedIn](https://linkedin.com/in/creativepurus)
