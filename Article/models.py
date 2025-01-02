from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class ArticleModels(models.Model):
    # pub_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = RichTextField()
    author = models.CharField(max_length=50, default="Anonymous")
    Pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField()

    def __str__(self):
        return self.title