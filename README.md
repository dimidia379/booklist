# I read U

This is a website build using Django, HTML (with Bootstrap 4), CSS and some JavaScript.  The main functionality is listening audiobooks. Every registered user also can upload his own audiobook created by him. So users can read books to each other.

It contains the next features:
- registered user can upload audiofile and it appears in main tracklist after premoderation by admin
- if user is admin, he can see number of tracks awating premoderation on the main page
- for every published track user can like/unlike it,  leave comments, see other tracks for this book or see other books of this book's author, go to the profile of user created track
- search function allows search book by title or author's name
- if user wants to listen a book which wasn't added yet, he can write a request for this book
- other users can see this request and create a track for it or they can just join request if they want to listen this book too
- user's profile page provides information about tracks created by this user, his favorite and requested books

### Structure
I use standard Django folder structure. JS file (index.js) is in Static/Books folder. Also this folder contains style.css file and folder with background image.  
File models.py contains such models as: User, Writer, Book, Track and Comment.
File views.py contains the next views:
- login_view
- logout_view
- register
- index
- create
- tracks
- track
- comment
- like
- writer
- book
- favorite
- requested
- join_request
- search

Here are all the templates:
- **layout.html** This page contains navbar including search panel. Navbar is mobile responsive.
- **login.html** Page for login.
- **register.html** Page for registration.
- **index.html** The main page with links to all tracks, uploading own track, registration or login . Also it provide information about number of tracks on premoderation for the site admin.
- **create.html** Contains form for  uploading audiofile and image of the book.
- **profile.html** User's profile page provides Information about tracks created by this user, his favorite books and books he waiting.
- **claim.html** Page with form to make a request for book to listen. Also shows top three  most waiting boooks with link to full list.
- **requested.html** List of all waiting books. For each book there is "Join awaiting" button. If user is already joined, book marked as "In your waiting list".  And in this case If book already contains some tracks, it also marked as "You can listen it now!".
- **track.html** Page contains image, audioplayer, information about the book and reader and comments. Authorised users can add book to favorites, like/unlike track and also write a comment. It's possible to go to the writer page clicking on the book's author name or go to the book's page clicking on the title.
- **tracks.html** Full list of tracks which are available to listen. Clicking on track card leads to the track page. Each card contains information about reader, author and title of the book. It's possible to like/unlike track right here in the card. 
- **book.html** Here is information about particular book: author and list of tracks (if they exist). Clicking on track name leads to this track page, clicking on author name leads to the author page. Authorised users can add book to favorites. If book is already in favorites, it is mentioned.
- **writer.html** This is a list of the author's books. It's possible to go to the book page by clicking on the book name.
- **search.html** Page for result if searching. Provides a list of books. Like a writer page it's possible to go to the book page by clicking on the book name.

### Requirements to run the code
- Install python and pip.
- Execute: "python -m pip install Django"
- Go in the root folder of the project, execute: "python manage.py runserver"



