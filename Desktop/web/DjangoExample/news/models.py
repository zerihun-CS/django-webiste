from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from tinymce import models as tinymce_models
class Category(models.Model):
   name = models.CharField(max_length=200)
   
   def __str__(self):
      return self.name
   
   def count_post(self):
      return Post.objects.filter(category__name = self.name).count()
   
class Tag(models.Model):
   name = models.CharField(max_length=30)
   

class Post(models.Model):
   title = models.CharField(max_length=200)
   description = tinymce_models.HTMLField()
   image  = models.ImageField()
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   category = models.ForeignKey("Category",  on_delete=models.SET_NULL, null=True)
   date = models.DateTimeField(auto_now=True,)

   def __str__(self):
      return self.title