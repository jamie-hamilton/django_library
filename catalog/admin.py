from django.contrib import admin


# Register your models here.
from .models import IndexContent, Author, Genre, Book, BookInstance, Language

# Register simple models in admin without customising:
admin.site.register(IndexContent)
admin.site.register(Genre)
admin.site.register(Language)

# More about how customisations are applied here:
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

# Define an admin class
class AuthorAdmin(admin.ModelAdmin):
    # display these fields in admin list view
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # display tuples on same line in admin object view
    fields = (('first_name', 'last_name'), ('date_of_birth', 'date_of_death'))

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Alternative method of registering Admin classes: 
# Book registered using the @admin.register decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # display these fields in admin list view
    list_display = ('title', 'author', 'display_genre')

# Book registered using the @admin.register decorator
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    # display these fields in admin list view
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    # admin list filtering in these fields
    list_filter = ('status', 'due_back')

    # split sections of admin page into field sets
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'borrower','due_back')
        }),
    )