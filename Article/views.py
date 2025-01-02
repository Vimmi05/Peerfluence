
from django.shortcuts import render,redirect
from Article.models import ArticleModels
from Article.forms import ArticleForm
from django.contrib import messages

def Add_Articles(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        
        if form.is_valid():
            s = form.save()
            messages.success(request, f"Article {s.title} is Added.")
            return redirect ('all_articles')
        else:
            print("Form Error : ",form.errors)
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'Article/add_article.html', context)

def All_Articles(request):
    data = ArticleModels.objects.all()
    context = {'data': data}
    return render(request, 'Article/all_article.html', context)

def View_Articel(request, id):
    data = ArticleModels.objects.get(id=id)
    randomArticles = ArticleModels.objects.exclude(id=id).order_by('-Pub_date')[:3]
    context = {'data': data, 'randomArticles': randomArticles}
    return render(request, 'Article/view_Articles.html', context)