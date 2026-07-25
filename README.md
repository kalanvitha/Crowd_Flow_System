# 🚦 CrowdFlow Prediction System

## 📌 Overview

CrowdFlow Prediction System is an AI-based smart crowd and traffic monitoring application that uses Computer Vision techniques to analyze congestion during public events.

The system processes video feeds, detects movement, estimates crowd density, monitors traffic flow, and displays the analysis through an interactive dashboard.

The main aim of this project is to assist authorities and event organizers in monitoring crowd situations and improving traffic management.

---

## 🎯 Problem Statement

Large public events often create heavy crowd movement and traffic congestion, which can lead to safety issues and delays.

Manual monitoring requires continuous human effort and may not provide accurate real-time analysis.

This project provides an automated solution using Computer Vision to analyze video streams and identify congestion levels efficiently.

---

## ✨ Features

- 🎥 Upload and analyze video files
- 👥 Crowd and object movement detection
- 🚦 Traffic congestion monitoring
- 📊 Crowd density analysis
- 📈 Interactive dashboard visualization
- ⚠️ Congestion alert generation
- 📍 Real-time monitoring support
- 🗂️ Data-based analysis and reporting

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js
- Leaflet.js

### Backend
- Python
- Flask

### Computer Vision & Data Processing
- OpenCV
- NumPy
- Pandas
- SciPy

### Database
- SQLite / MySQL

### Tools
- VS Code
- Git
- GitHub

---

## 🏗️ System Architecture

```
              Video / CCTV Input
                     |
                     ↓
          Video Processing Module
                     |
                     ↓
        Computer Vision Detection
                     |
                     ↓
        Crowd & Traffic Analysis
                     |
                     ↓
             Flask Backend API
                     |
                     ↓
          Interactive Web Dashboard
```

---

## 📂 Project Structure

```
Crowd_Flow_System/

│
├── app.py                 # Flask main application
├── test_mysql.py          # Database testing file
├── .env.example           # Environment variables example
├── requirements.txt       # Project dependencies
│
├── templates/
│   └── HTML pages
│
├── static/
│   ├── CSS files
│   ├── JavaScript files
│   └── Images
│
├── uploads/
│   └── Input videos
│
└── models/
    └── Detection models
```

---

## ⚙️ Installation & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/kalanvitha/Crowd_Flow_System.git
```

### Step 2: Navigate to Project Folder

```bash
cd Crowd_Flow_System
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

---

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5: Run Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

## 📊 Dashboard

The dashboard provides:

- Video upload interface
- Crowd monitoring information
- Detection output visualization
- Traffic flow statistics
- Congestion analysis

---

## 🚀 Future Enhancements

- Real-time CCTV camera integration
- YOLOv8 deep learning model integration
- AI-based crowd prediction
- Cloud deployment
- Mobile application support
- Emergency notification system

---

## 👩‍💻 Author

**Kalanvitha Gundrathi**

Data Science Student

GitHub:
https://github.com/kalanvitha

---

## 📜 License

This project is developed for educational and research purposes.