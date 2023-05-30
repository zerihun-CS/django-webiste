from django.urls import path, include
from .views import index,post_detail,category_post
urlpatterns = [
   
   path('', index, name='index_url'),
   path('category_post/<str:category_name>/', category_post, name='category_post_url'),
   path('post_detail/<str:post_title>/', post_detail, name='post_detail_url')
]
