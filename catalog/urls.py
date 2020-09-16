from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path("search/", views.BookSearchView.as_view(), name="search"),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.LoanedBooksLibrarianListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/return/', views.return_book_librarian, name='return-book-librarian'),
    path('book_instance/create/', views.BookInstanceCreate.as_view(), name='book_instance_create'),
    path('book_instance/<uuid:pk>/update/', views.BookInstanceUpdate.as_view(), name='book_instance_update'),
    path('book_instance/<uuid:pk>/delete/', views.BookInstanceDelete.as_view(), name='book_instance_delete'),
    path('authors/', views.author_list, name='authors'),
    path('author/<int:pk>', views.author_detail, name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]