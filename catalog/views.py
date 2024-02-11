from msilib.schema import ListView
from django.shortcuts import render

# Create your views here. 
# Esta é a visão mais simples possível no Django.
# Para chamar a view, precisamos mapeá-la para uma URL - e para isso precisamos de um URLconf.

# Para criar um URLconf no diretório polls, 
# crie um arquivo chamado urls.py.
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.db.models import Prefetch

from django.views.generic import DetailView
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Esta função é a mais fácil pois apresenta apenas páginas estáticas
import datetime
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Author

# @login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('emprestados'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# @login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_livros_pesquisados = Book.objects.filter(title__icontains='mago').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genero = Genre.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # No contexto que vai ser rodadado no HTML o que se pode modificar
    # é o primeiro elemento, é o mesmo que será modificado no HTML
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genero':num_genero,
        'num_livros_esquisados': num_livros_pesquisados,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class AuthorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Author
    template_name = 'catalog/detalhe_author.html'
    
    
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 20
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'  # Nome do seu template HTML para o detalhe do livro
    
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'

    def get_queryset(self):
        # Retorna todos os livros emprestados no sistema com informações sobre quem emprestou
        return BookInstance.objects.filter(status__exact='o').order_by('due_back').prefetch_related('borrower')


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'



class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author')
    permission_required = 'catalog.delete_author'