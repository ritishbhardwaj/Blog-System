from django.db import models
from django.contrib.auth.models import User
from sqlalchemy import null
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,
                        
                        null = True, 
                        on_delete = models.SET_NULL)
    title= models.CharField(max_length=250)
    desc=models.TextField()


class Comments_Post(models.Model):
    commentUser=models.ForeignKey(Post, null= True, on_delete=models.SET_NULL)
    comment=models.TextField()