# 👨‍🎓 Facial Recognition Attendance System

A Python-based attendance system that uses **Face Recognition** to automatically mark attendance by detecting and recognizing faces from a live webcam feed.

---

## 🚀 Features
- ✅ Real-time face detection and recognition using **OpenCV** and **dlib**
- ✅ Automatically logs recognized faces into an **Excel/CSV attendance file**
- ✅ Simple and lightweight Python-based solution
- ✅ Extendable for schools, colleges, and offices

---

## 🛠️ Tech Stack
- **Python 3.12**
- **OpenCV** – Camera input & image processing
- **dlib** – Face detection model
- **face_recognition** – High-level API for face encodings & matching
- **pandas / openpyxl** – Attendance logging
- **Excel/CSV** – Output files

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Facial_Recognition_Attendance_System.git
cd Facial_Recognition_Attendance_System
````

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the attendance system:

```bash
python Attendance.py
```

### Workflow:

1. The webcam will open and start detecting faces.
2. Known faces (from the dataset) will be recognized.
3. Attendance will be recorded automatically in an Excel/CSV file with:

   * Name
   * Date
   * Time

---

## 📂 Project Structure

```
Facial_Recognition_Attendance_System/
│── Attendance.py          # Main application file
│── Requirements.txt       # Project dependencies
│── README.md              # Documentation
│── Images                 # Folder containing known faces
│── Attendance.csv/        # File where attendance Excel/CSV files are saved
```

---

## 📊 Example Attendance Output

| Name       | Date       | Time     |
| ---------- | ---------- | -------- |
| Creative Purus   | 2025-08-18 | 09:32:14 |
| Jane Smith | 2025-08-18 | 09:35:02 |

---

## 🛡️ Requirements

* Windows/Linux/MacOS
* Python 3.12+
* C++ Build Tools (required for dlib)

---

## 🔮 Future Improvements

* Multi-camera support
* Cloud database integration (Firebase / Supabase)
* Web dashboard for attendance monitoring
* SMS/Email notifications

---

## 🙌 Contribution

Pull requests are welcome! If you’d like to contribute:

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify.

---

## 👨‍💻 Author

Developed by **Purushottam (creativepurus)** 🚀