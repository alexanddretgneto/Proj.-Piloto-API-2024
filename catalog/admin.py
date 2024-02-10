from django.contrib import admin

# Register your models here.
from .models import Book, BookInstance, Genre, Author

class BooksInline(admin.TabularInline):
    model = Book
    fields = ['title', 'display_genre']
    readonly_fields = ['title', 'display_genre']
    extra = 0

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # Define o número de formulários em linha extras para 0


# Esta classe mostrará no admin tudo o 
# que for adicionado
# na class AuthorAdmin
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = [('first_name', 'last_name'), 'date_of_birth', 'date_of_death']
    inlines = [BooksInline]
    search_fields = ['first_name', 'last_name', 'book__title']
    
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    search_fields = ['title', 'author__first_name', 'author__last_name']
    inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
    

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
