from django.urls import path
from . import views

urlpatterns = [
     path('Article/', views.Add_Articles, name="add_articles"),
     path('AllArticles/', views.All_Articles, name="all_articles"),
     path('ViewArticle/<int:id>/', views.View_Articel, name="view_article")
]

             