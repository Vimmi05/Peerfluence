from django.db import models
from django.contrib.auth.hashers import make_password

class UserProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 15
    COLLEGE_MAX_LENGTH = 100

    STATUS_CHOICES = [
        ('Professor', 'Professor'),
        ('Student', 'Student'),
        ('Alumni', 'Alumni'),
    ]

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    phone_number = models.CharField(max_length=PHONE_MAX_LENGTH, blank=True)
    password = models.CharField(max_length=255)  # Store hashed password
    college = models.CharField(max_length=COLLEGE_MAX_LENGTH, blank=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    university_roll_no = models.CharField(max_length=50, blank=True, null=True)
    passout_year = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
