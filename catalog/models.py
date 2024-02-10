from datetime import date
from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances-7
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre.
        Modelo que representa um gênero de livro."""
    name = models.CharField(max_length=502, help_text='Crie aqui o  gênero do livro')

    def __str__(self):
        """String for representing the Model object.
            String para representar o objeto do modelo.
            Este que aparecerá no admin mostrando o gênero"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    """Modelo que representa um livro (mas não uma cópia específica de um livro)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    # Chave estrangeira usada porque um livro só pode ter um autor, mas autores podem ter vários livros
    # Autor como uma string ao invés de um objeto porque ainda não foi declarado no arquivo
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Descrição do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

     # ManyToManyField usada porque um gênero pode conter muitos livros. Livros podem cobrir muitos gêneros.
    # A classe Genre já foi definida, então podemos especificar o objeto acima.
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Selecione o genero do livro')

    def __str__(self):
        """String for representing the Model object.
        String para representar o objeto do modelo."""
        return self.title

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin.
        É preciso pra mostrar o gênero no admin
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book.
            Retorna a URL para acessar um registro de detalhes para este livro."""
        return reverse('detalhe-livro', args=[str(self.id)])
        
        # return reverse('book-detail', args=[str(self.id)])
    
class Author(models.Model):
    """Model representing an author.
        Modelo que representa um autor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object.
            Retorna a URL para acessar uma instância particular de autor."""
        return f'{self.last_name}, {self.first_name}'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library).
        Modelo que representa uma cópia específica de um livro (ou seja, que pode ser emprestada da biblioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    # borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


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
        help_text='Avaliação dos livros',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        if self.borrower:
            return f'{self.book.title} - Emprestado por: {self.borrower.first_name} {self.borrower.last_name}'
        else:
            return f'{self.book.title} - Emprestado por: Desconhecido'
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
         return True
        return False