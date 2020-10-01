# :books: library_

A local library application that allows 'librarians' to create, edit, update and renew books/authors, and borrowers can monitor their loans and view book availabilities.

__tl;dr:__
- ORMs! Django admin! Unit Testing! Security! Production consideration!

- favourite code snippet:
```Python
  # generic views were a revelation:
  class BookDetailView(generic.DetailView):
    model = Book
```
- what it looks like:

![library screenshot](https://s3.eu-west-2.amazonaws.com/media.jh-portfolio/media/project_images/library-1.png)

I used [MDN's server side development tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side) as a guide for the project. The module focused on server-side web programming, and provided me with an opportunity to to explore several key features of Django further.
