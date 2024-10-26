from django.db import models
from website.models import UserProfile
class UserInformation(models.Model):
    student_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_student')
    employee_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_employee')
    passout_year = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_year')  
    profession = models.CharField(max_length=100)  
    college = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_college')    
    birthday = models.DateField()  
    country = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  
    languages = models.TextField()  
    email = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_email')    
    phone = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_information_phone')   
    interests_music = models.TextField()  
    interests_movies = models.TextField()  

    def __str__(self):
        return f"{self.student_id} - {self.profession}"

    class Meta:
        verbose_name = 'User Information'
        verbose_name_plural = 'User Information'
