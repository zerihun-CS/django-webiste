from django.shortcuts import render
from .models import Post, Category
# Create your views here.


def index(request):
   post = Post.objects.all()
   
   return render(request, 'index.html',{'post':post})


def post_detail(request,post_title:str):
   single_post = Post.objects.filter(title = post_title).first()
   category = Category.objects.all()
   return render(request, 'post_detail.html',{'single_post':single_post,'category':category})


def category_post(request, category_name:str):

   post = Post.objects.filter(category__name = category_name)   
      
   return render(request, 'index.html',{'post':post})
