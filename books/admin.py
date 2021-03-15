from django.contrib import admin

from .models import User, Track, Writer, Book, Comment

admin.site.register(User)
admin.site.register(Track)
admin.site.register(Writer)
admin.site.register(Book)
admin.site.register(Comment)

