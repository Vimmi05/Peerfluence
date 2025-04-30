from django.db import models
from website.models import UserProfile
class UserInformation(models.Model):
    
    img = models.ImageField(blank=True, null=True)
    profession = models.CharField(max_length=100) 
    birthday = models.DateField()  
    country = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  
    languages = models.TextField()  
    interests_music = models.TextField()  
    interests_movies = models.TextField()  
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profession

    class Meta:
        verbose_name = 'User Information'
        verbose_name_plural = 'User Information'

class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.percentage}%"