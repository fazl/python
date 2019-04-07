from django.db import models

# Create your models here. Migrated DB after adding:
# # py manage.py makemigrations
# D:\python\django_test\bibliothek>py manage.py makemigrations
# Migrations for 'catalog':
#   catalog\migrations\0001_initial.py
#     - Create model Author
#     - Create model Book
#     - Create model Genre
#     - Create model BookInstance
#     - Add field genre to book
#
# D:\python\django_test\bibliothek>py manage.py migrate
# Operations to perform:
#   Apply all migrations: admin, auth, catalog, contenttypes, sessions
# Running migrations:
#   Applying catalog.0001_initial... OK

# Seems a bit of overkill - could just use a genre string attribute on books
# But this way the framework support will add value
#
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(
        max_length=200,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

# Used to generate URLs by reversing the URL patterns
# In English: read as 'viewNameToUrl'
from django.urls import reverse


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key (book has one author, author can have multiple books)
    # 'Author' (str) not Author (class) as class not yet declared in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book'
    )
    #label specified to avoid default 'Isbn'
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='13 char <a href="http://bit.ly/2uRdbcD">ISBN number</a>'
    )

    # ManyToManyField because..
    # A genre can apply to many books.
    # Many genres can apply to a given book.
    # Genre class has already been defined so we can reference it directly
    #
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


import uuid # Required for unique book instances
class BookInstance(models.Model):
    """Model representing an instance or copy of a book (that can be borrowed
    from the library)."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text="What's an imprint?")
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['-due_back'] # Earliest due back first seems more useful

    def __str__(self):
        """String for representing the Model object."""
        # short for "{0} ({1})"%(self.id, self.book.title)
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('D.O.B.', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
