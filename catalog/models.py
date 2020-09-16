from django.db import models
from django.contrib.auth.models import User

# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
# Required for BookInstance is_overdue @property
from datetime import date
# Required for unique book instances
import uuid

class IndexContent(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return self.title

# Create your models here.
class Genre(models.Model):
    """Represents genres of related book"""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """Genre object string."""
        return self.name


class Language(models.Model):
    """Represents language of related book"""
    name = models.CharField(max_length=200, help_text='Enter the language of the book')

    def __str__(self):
        """Language object string"""
        return self.name


class Book(models.Model):
    """Represents a published book (not a specific copy of a book)"""
    title = models.CharField(max_length=200)

    # Foreign Key (one-to-one) relationship
    # (Book can only have one author but author can have many books)
    # Note that Author is a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a brief description of the book'
    )
    isbn = models.CharField(
        'ISBN', 
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )

    # Many-to-many relationship
    # (Genre can contain many books and books can be multiple genres)
    # Genre class has been defined so can refer directly to object
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language=models.ForeignKey(
        Language, 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        permissions = (("can_edit_books", "Edit books"),)
    
    def __str__(self):
        """Book object string."""
        return self.title

    def get_absolute_url(self):
        """Return URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Represents specific copy of a book"""
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.SET_NULL, 
        null=True
    ) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(
        null=True, 
        blank=True,
        help_text='(YYYY-MM-DD)'
    )


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    borrower = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"), ("can_create_copy", "Create new copy of book"))

    def get_absolute_url(self):
        """Returns URL to access a particular author instance."""
        return reverse('book-instance-detail', args=[str(self.id)])

    def __str__(self):
        """Book instance object string."""
        return f'{self.id} ({self.book.title})'

    # property functions return a property attribute:
    # https://docs.python.org/3/library/functions.html#property
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        

class Author(models.Model):
    """Represents an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(
        'born', 
        null=True, 
        blank=True,
        help_text='(YYYY-MM-DD)'
    )
    date_of_death = models.DateField(
        'died', 
        null=True, 
        blank=True,
        help_text='(YYYY-MM-DD)'
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_edit_authors", "Edit authors"),)

    def get_absolute_url(self):
        """Returns URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Author object string."""
        return f'{self.last_name}, {self.first_name}'