from django.forms import ModelForm
from Article.models import *

class ArticleForm(ModelForm):
    class Meta:
        model = ArticleModels
        fields = "__all__"