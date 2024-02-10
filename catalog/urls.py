from django.urls import path
from django.views.generic import RedirectView

from . import views
# from views import LoanedBooksListView

urlpatterns = [
    # chama uma função 
    path("", views.index, name="index"),
    # Chama uma classe
    ]

# Você pode adicionar mais URLs aqui se necessário

# Por exemplo:
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='detalhe-livro'),
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('emprestados/', views.AllBorrowedBooksListView.as_view(), name='emprestados'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]