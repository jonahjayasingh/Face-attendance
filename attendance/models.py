from django.db import models
from datetime import datetime
from django.utils import timezone

class Staff(models.Model):
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='staff_training_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.department})"

    @property
    def get_student_count(self):
        return self.students.count()

class StaffAttendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.staff.name} - {self.date} - {self.status}"

class StudentData(models.Model):
    registration_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    dept = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='training_images/') # Training image
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True) # Profile photo
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now) # Sign-in time
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    @property
    def name(self):
        return self.student.name

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class SystemSettings(models.Model):
    start_time = models.TimeField(default="09:00:00")
    end_time = models.TimeField(default="17:00:00")
    absent_threshold_minutes = models.IntegerField(default=30) # Mark absent if not present by start_time + threshold

    class Meta:
        verbose_name_plural = "System Settings"
