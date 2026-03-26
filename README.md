# 👤 Face Attendance System

A modern, automated attendance tracking system leveraging artificial intelligence and computer vision to streamline student attendance management.

## 🚀 Overview
The Face Attendance System uses state-of-the-art face recognition technology to automatically mark attendance. It supports student enrollment with face capture, real-time recognition, and comprehensive attendance reports.

## ✨ Features
- **Real-time Recognition**: Automated attendance logging via live camera feed.
- **Smart Enrollment**: Quick student registration with live face capture.
- **Attendance Insights**: View daily, weekly, and monthly attendance reports.
- **Admin Dashboard**: Secure management of student data and system stats.
- **Robust Database**: Uses SQLite with foreign key relationships for data integrity.
- **Responsive Web Interface**: Modern UI for both admin and student views.

## 🛠️ Tech Stack
- **Frameworks**: Flask (Primary App), Django (Backend Services)
- **Computer Vision**: OpenCV, face-recognition (dlib)
- **Database**: SQLite, SQLAlchemy, Django ORM
- **UI/UX**: HTML5, CSS3, JavaScript

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd face_attendance
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy django opencv-python numpy face-recognition werkzeug
   ```

4. **Initialize Databases**
   ```bash
   # For Flask
   python model.py
   python migrate_db.py  # Optional: For data migration
   
   # For Django
   python manage.py migrate
   ```

## 🔑 Admin Setup
To create an administrator account for the Flask application:
```bash
python create_admin.py
```
Follow the interactive prompts to create/manage admin accounts.

## 🏃 Running the Application

### Flask App (Recommended)
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5001`.

### Django App
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000`.

## 📁 Project Structure
- `app.py`: Main Flask application.
- `model.py`: SQLAlchemy database models.
- `attendance/`: Django app for attendance management.
- `core/`: Django project configuration.
- `static/`: CSS, JS, and Training images.
- `templates/`: HTML templates for the web interface.

---
Produced with ❤️ for the Face Attendance Project.
