from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Track, Writer, Book, Comment


def index(request):
    tracks = []
    user = request.user
    row_tracks = Track.objects.filter(is_published=True).order_by("-create_date")
    for track in row_tracks: 
        liked = False
        if user is not None and user in track.likes.all():
            liked = True
        tracks.append({
            'id': track.id,
            'reader': track.reader,
            'image': track.image.url,
            'author': track.book.author,
            'title': track.book.title,
            'chapter': track.chapter,
            'timestamp': track.create_date,
            'likes_counter': track.likes.count(),
            'liked': liked
        })

    all_books = Book.objects.all()
    claims = []
    for book in all_books:
        counter = book.count_claimants()
        if counter > 0:
            claims.append(book)

    return render(request, "books/index.html", {
        'tracks': tracks,
        'claims': claims[:3]
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "books/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "books/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "books/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "books/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "books/register.html")


class TrackForm(forms.ModelForm):
    book_author = forms.CharField(required=True)
    book_title = forms.CharField(required=True)

    class Meta:
        model = Track
        fields = ('book_author', 'book_title', 'chapter', 'audio', 'image')

@login_required
def create(request):
    if request.method == "POST":
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            b_author = form.cleaned_data['book_author']
            b_title = form.cleaned_data['book_title']          

            writer, created = Writer.objects.get_or_create(name=b_author)
            writer.save()
            book, created = Book.objects.get_or_create(author=writer, title=b_title)
            book.save()

            track = form.save(commit=False)
            track.reader = request.user
            track.book = book
            track.create_date = timezone.now()
            track.is_published = False
            track.save()            

            return HttpResponseRedirect(reverse("index"))
    else:
        form = TrackForm()
        return render(request, 'books/create.html', {
            'form': form
        })


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

def track(request, track_id):
    track = Track.objects.get(pk=track_id)   
    book_id = track.book.id
    writer_id = track.book.author.id    
    user_id = track.reader.id
    comments = Comment.objects.filter(track=track)
    form = CommentForm
    likes_counter = track.likes.count()

    user = request.user
    
    liked = False    
    if user is not None and user in track.likes.all():
        liked = True

    book_in_favs = False
    book =  Book.objects.get(pk=book_id)
    book_favs =book.favorites.all()
    if user is not None and user in book_favs:
        book_in_favs = True
    
    return render(request, "books/track.html", {
        "track": track,
        "book_id": book_id,
        "writer_id": writer_id,
        "user_id": user_id,
        "comments": comments,
        "liked": liked,
        "book_in_favs": book_in_favs,
        'likes_counter': likes_counter,
        "form": form
    })



@login_required
def comment(request, track_id):
    user = request.user
    track = Track.objects.get(pk=track_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.track = track
            comment.create_date = timezone.now()
            comment.save()
            return HttpResponseRedirect(reverse('track', args=(track.id,)) )
        else:
            return HttpResponseRedirect(reverse('track', args=(track.id,)) )
    return HttpResponseRedirect(reverse('track', args=(track.id,)))



class ClaimForm(forms.ModelForm):
    book_author = forms.CharField(required=True)
    book_title = forms.CharField(required=True)   

    class Meta:
        model = Book
        fields = ('book_author', 'book_title')

def claim(request):
    user = request.user
    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():

            b_author = form.cleaned_data['book_author']
            b_title = form.cleaned_data['book_title']          

            writer, created = Writer.objects.get_or_create(name=b_author)
            writer.save()
            book = form.save(commit=False)
            book.author = writer
            book.title = b_title
            
            book.save()
            book.claimants.add(user)
            book.save()          

            return HttpResponseRedirect(reverse("requested"))
    else:
        form = ClaimForm()
        return render(request, 'books/claim.html', {
            'form': form
        })


def book(request, book_id):
    book = Book.objects.get(pk=book_id)
    tracks = Track.objects.filter(book=book).order_by("-chapter")
    return render(request, "books/book.html", {
        "book": book,
        "tracks": tracks
    })

def writer(request, writer_id):
    writer = Writer.objects.get(pk=writer_id)
    author = writer.id
    books = Book.objects.filter(author=author)
    return render(request, "books/writer.html", {
        "writer": writer,
        "books": books
    })


@csrf_exempt
@login_required
def like(request, track_id):
    track = Track.objects.get(pk=track_id)

    if request.method == "PUT":
        liker = request.user
        likers = track.likes.all()     
        if not liker in likers:
            track.likes.add(liker)
        else:
            track.likes.remove(liker)
        
        track.save()
        return JsonResponse({"message": "Successfully liked."}, status=201)

    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@login_required
def profile(request, user_id):
    profile = User.objects.get(pk=user_id)
    tracks = Track.objects.filter(reader=profile)

    all_books = Book.objects.all()
    books = []
    claims = []
    for book in all_books:
        if profile in book.favorites.all():
            books.append(book)
        if profile in book.claimants.all():
            claims.append(book)
      
    return render(request, "books/profile.html", {
        "profile": profile,
        "tracks": tracks,
        "books": books,
        "claims": claims
    })


@csrf_exempt
@login_required
def favorite(request):
    user = request.user
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("book_id") is not None:
            book_id = data["book_id"]
            book = Book.objects.get(pk=book_id)
            book.favorites.add(user)
            book.save()
            return JsonResponse({"message": "Successfully added to favorites."}, status=201)

    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


def requested(request):
    claims = []
    for book in Book.objects.all():
        counter = book.count_claimants()
        if counter > 0:
            claims.append(book)
     
    read = []
    for track in Track.objects.all():
        read.append(track.book)
    
    return render(request, "books/requested.html", {
        "claims": claims,
        "read": read
    })


@csrf_exempt
@login_required
def join_request(request):
    user = request.user
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("book_id") is not None:
            book_id = data["book_id"]
            print(book_id)
            book = Book.objects.get(pk=book_id)
            book.claimants.add(user)
            book.save()
            return JsonResponse({"message": "Successfully added to requested."}, status=201)

    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
