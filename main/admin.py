from django.contrib import admin
from main.models import Post, Image, Comment, Like, Rating

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
