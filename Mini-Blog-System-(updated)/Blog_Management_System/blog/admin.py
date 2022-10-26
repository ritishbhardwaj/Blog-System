from django.contrib import admin
from .models import Post,Comments_Post
# Register your models here.

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc','user']

@admin.register(Comments_Post)
class CommentModelAdmin(admin.ModelAdmin):
    pass