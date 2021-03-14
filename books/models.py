from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):    
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.username


class Writer(models.Model):
    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey("Writer", on_delete=models.CASCADE, related_name="writers", default=None)
    title = models.CharField(max_length=100)
    favorites = models.ManyToManyField("User", related_name="lovers", default=None, blank=True)
    claimants = models.ManyToManyField("User", related_name="claimants", default=None, blank=True)

    def count_claimants(self):
        return self.claimants.count()

    def __str__(self):
        return f"{self.author} - {self.title}"


class Track(models.Model):
    chapter =  models.DecimalField(max_digits=5, decimal_places=0, default=1,)
    reader = models.ForeignKey("User", on_delete=models.CASCADE, related_name="readers", default=None)
    create_date = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="all_books", default=None)
    audio = models.FileField(upload_to='{book}/audio/')
    image = models.ImageField(upload_to='{book}/images/', default="images/noimage.jpg", blank=True)
    is_published = models.BooleanField(verbose_name="Published", default=False)
    likes = models.ManyToManyField("User", related_name="likers", default=None, blank=True)

    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.is_published} {self.book}: chapter {self.chapter} by {self.reader}"
       

class Comment(models.Model):
    track = models.ForeignKey("Track", on_delete=models.CASCADE, related_name="comment_tracks", default=None)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comment_authors", default=None)
    text = models.TextField(default=None, blank=False, verbose_name='Add your comment')
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} comment for {self.track}"