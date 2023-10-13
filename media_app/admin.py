from django.contrib import admin
from .models import Profile,Comment,Like,Post,FriendRequest

# Register your models here.
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(FriendRequest)
