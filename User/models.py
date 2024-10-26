from django.db import models

class UserInformation(models.Model):
    student_id = models.CharField(max_length=50, unique=True)  
    passout_year = models.CharField(max_length=4)  
    profession = models.CharField(max_length=100)  
    college = models.CharField(max_length=100)  
    birthday = models.DateField()  
    country = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  
    languages = models.TextField()  
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15)  
    interests_music = models.TextField()  
    interests_movies = models.TextField()  

    def __str__(self):
        return f"{self.student_id} - {self.profession}"

    class Meta:
        verbose_name = 'User Information'
        verbose_name_plural = 'User Information'
