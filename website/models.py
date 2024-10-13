# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='profile_pics', default='default.jpg')

#     def __str__(self):
#         return f'{self.user.username} Profile'

# class Post(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     image = models.ImageField(upload_to='post_images', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.author.username} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'