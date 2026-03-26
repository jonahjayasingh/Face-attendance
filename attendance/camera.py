import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime, timedelta
from uuid import uuid4
from .models import StudentData, Attendance, Staff

TRAINING_PATH = "static/Training images"

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.encodeListKnown = []
        self.known_students = []
        self.load_known_faces()

    def __del__(self):
        self.video.release()

    def load_known_faces(self):
        self.encodeListKnown = []
        self.known_entities = [] # Can be StudentData or Staff
        
        try:
            # Fetch all students from database
            students = StudentData.objects.all()
            for student in students:
                if student.image and student.image.name:
                    self._add_entity_to_known(student, student.image.path)
            
            # Fetch all staff from database
            staff_members = Staff.objects.all()
            for staff in staff_members:
                if staff.image and staff.image.name:
                    self._add_entity_to_known(staff, staff.image.path)
                    
        except Exception as e:
            print(f"Database error in load_known_faces: {e}")

    def _add_entity_to_known(self, entity, img_path):
        try:
            if os.path.exists(img_path):
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    encs = face_recognition.face_encodings(img)
                    if encs:
                        self.encodeListKnown.append(encs[0])
                        self.known_entities.append(entity)
        except Exception as e:
            print(f"Error loading face for {entity.name}: {e}")

    def get_frame(self, mode='none'):
        success, image = self.video.read()
        if not success:
            return None

        if mode == 'recognize' and self.encodeListKnown:
            imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                if len(faceDis) > 0:
                    matchIndex = np.argmin(faceDis)
                    if faceDis[matchIndex] < 0.50:
                        entity = self.known_entities[matchIndex]
                        name = entity.name
                        # Mark attendance based on entity type
                        if isinstance(entity, StudentData):
                            self.mark_attendance_internal(entity)
                    else:
                        name = 'UNKNOWN'
                else:
                    name = 'UNKNOWN'

                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                color = (0, 255, 0) if name != 'UNKNOWN' else (0, 0, 255)
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                # Display name, time, status, and info on overlay
                display_text = name
                prefix = "Faculty: " if name != 'UNKNOWN' and isinstance(entity, Staff) else ""
                info_text = ""
                
                if name != 'UNKNOWN':
                    now = datetime.now()
                    today = now.date()
                    
                    if isinstance(entity, StudentData):
                        att = Attendance.objects.filter(student=entity, date=today).first()
                        status_str = f" ({att.status})" if att else ""
                        display_text = f"{name}{status_str} {now.strftime('%I:%M %p')}"
                        if entity.staff:
                            info_text = f"Faculty: {entity.staff.name} | {entity.staff.department}"
                    else: # Staff
                        student_count = entity.students.count()
                        display_text = f"{prefix}{name} {now.strftime('%I:%M %p')}"
                        info_text = f"Dept: {entity.department} | Handled: {student_count} Students"

                cv2.putText(image, display_text, (x1 + 6, y2 - 22), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 255, 255), 2)
                if info_text:
                    cv2.putText(image, info_text, (x1 + 6, y2 - 4), cv2.FONT_HERSHEY_COMPLEX, 0.45, (180, 220, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def mark_attendance_internal(self, student):
        try:
            now = datetime.now()
            today = now.date()
            if not student: return
            
            attendance = Attendance.objects.filter(student=student, date=today).first()
            if not attendance:
                from .models import SystemSettings
                conf = SystemSettings.objects.first() or SystemSettings.objects.create()
                start_time = datetime.combine(today, conf.start_time)
                threshold_time = start_time + timedelta(minutes=conf.absent_threshold_minutes)
                status = 'Present' if now <= threshold_time else 'Absent'
                Attendance.objects.create(student=student, date=today, time=now.time(), status=status)
                print(f"✓ Student Attendance MARKED ({status}) for {student.name}")
        except Exception as e:
            print(f"Error in student mark: {e}")

global_camera = None

def get_camera():
    global global_camera
    if global_camera is None:
        global_camera = VideoCamera()
    return global_camera
