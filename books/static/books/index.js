window.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll(".like-toggle").forEach(el => {
      el.addEventListener('click', function( event ) {
        const id = event.target.dataset.id;
        like(id);          
      });
  });
});


// Like/unlike track
function like(trackId) {
  if (!document.querySelector('#profile-link')) {
    alert("Please log in to like posts.")
  } else {

    fetch(`/like/${trackId}`, {
      method: 'PUT' 
    })
    .then(response => {
      response.json();
    })
    .then(result => {
      const button= document.querySelector(`#like-btn-${trackId}`);
      const counter = document.querySelector(`#like-cnt-${trackId}`);
      const total = Number(counter.innerHTML);

      if (button.dataset.status == 'liked') {
        counter.innerHTML = total - 1;
        button.className ='like-toggle';
        button.dataset.status = 'not-liked';
      } else {
        counter.innerHTML = total + 1;
        button.className ='like-toggle like-active';
        button.dataset.status = 'liked';
      }
      location.reload();   
    });
  }
return false;  
}


// Add book to favorites
function favorite() {
  bookId = document.querySelector("#bookId").dataset.bookid;
  fetch('/favorite', {
    method: 'PUT',
    body: JSON.stringify({
      book_id: bookId
    })
  })
  .then(response => {
    response.json();    
  })
  .then(result => {
    console.log(result)
    document.querySelector("#favorites-btn").style.display = 'none';
    location.reload();   
  });  
  return false;  
}


// Add book to waitlist
function joinRequest(bookId) {
  fetch('/join', {
    method: 'PUT',
    body: JSON.stringify({
      book_id: bookId
    })
  })
  .then(response => {
    response.json();    
  })
  .then(result => {
    console.log(result)
    location.reload();   
  });  
  return false; 
}

