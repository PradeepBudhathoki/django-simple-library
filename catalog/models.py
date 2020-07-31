from django.db import models
from django.urls import reverse #used to generate urls by reversing the url patterns
import uuid #required for unique identifiers
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    """model representing a book genre."""
    """help text is required for easiness during django form"""
    name=models.CharField(max_length=20,help_text='Enter the book genre (e.g. Science fiction)')
    
    def __str__(self): #this is instantiation which returns genre of particular book
        return self.name

class Language(models.Model):
    """model representing a language;English, French, Japanese"""
    name=models.CharField(max_length=200,help_text="Enter the book's natural language")

    def __str__(self):
        return self.name

class Book(models.Model):
    """model representing a book but not any particular instance(not any particular copy"""
    title=models.CharField(max_length=25)
    """foreign key used here because author here is a separate model so we need to link book to author.One to 
    many relationships."""
    author=models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)#author as a string beacause beacuse it hasn't been declared yet
    summary=models.TextField(max_length=1000,help_text='Enter brief description of the book')
    isbn=models.CharField('ISBN',max_length=13,help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    """many genres of each books, many books of each genre so manytomany field"""
    genre=models.ManyToManyField(Genre,help_text='Select a genre for this book')#here Genre is object not string
    language=models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)
    

    def __str__(self):
        return self.title #return title string of Book model

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
         """Create a string for the Genre. This is required to display genre in Admin."""
         return ','.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description='Genre'

    def display_language(self):
        return self.language

    

class BookInstance(models.Model):
    """model representing a specific copy of a book (i.e. that cab be borrowed from the library)"""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique id for this particular book across whole library')
    book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    borrower=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),

    )
    status=models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book_availability'
    )


    class Meta:
        ordering=['due_back']
        permissions=(("can_mark_returned","Set book as returned"),)#custom permission
    

    def __str__(self):
        return f'{self.id},{self.book.title}'

    

class Author(models.Model):
    """model representing an author"""
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField('Died',null=True,blank=True)


    def get_absolute_url(self):
        """returns the url to access particular author instance"""
        return reverse('author-detail',args=[str(self.id)])

    def __str__(self):
        """string for representing the model object/printing two fields"""
        return f'{self.last_name},{self.first_name}'

    class Meta:
        ordering=['last_name']


