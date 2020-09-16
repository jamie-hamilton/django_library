from django.shortcuts import render, redirect, get_object_or_404
import datetime
# templates for class based view
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# see AuthorDelete class for example use
from django.urls import reverse_lazy

# class based view restriction using mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# required for function based pagination:
from django.core.paginator import Paginator
# function based view restriction using decorators
from django.contrib.auth.decorators import login_required, permission_required

# Import models to view;
from catalog.models import Book, Author, BookInstance, Genre, IndexContent
from catalog.forms import RenewBookForm, ReturnBookForm, SearchForm


def index(request):
    """Home page view function"""

    # Pull in introduction content from IndexContent model
    intro = IndexContent.objects.first()

    # Generate counts of main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (books with status of 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default, so this works:
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Pass variables to view
    context = {
        'intro': intro,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render index.html template with declared context
    return render(request, 'index.html', context)


# class based view example
class BookListView(generic.ListView):
    # ListView will automatically look for template at:
    # locallibrary/catalog/templates/catalog/book_list.html
    model = Book
    # pagination is included in generic.ListView
    # can be applied as so:
    paginate_by = 20

    # ordering queryset ensures that pagination doesn't throw an error
    # https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/#making-friendly-template-contexts
    def get_queryset(self):
        queryset = Book.objects.order_by('title')
        return queryset

    # additional data can be added to context of class view
    # this overrides get_context_data() function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = SearchForm()
        return context


class BookSearchView(generic.ListView):
    model = Book
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET['q']
        queryset = Book.objects.filter(title__contains=q).order_by('title')
        return queryset
    
    # additional data can be added to context of class view
    # this overrides get_context_data() function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookSearchView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = SearchForm()
        return context


class BookDetailView(generic.DetailView):
    model = Book


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_edit_books'
    fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_edit_books'
    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_edit_books'
    # lazily executed version of reverse()
    # required here because URL is being provided to a class-based view
    success_url = reverse_lazy('books')


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    permission_required = 'catalog.can_create_copy'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.book_id})

class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    permission_required = 'catalog.can_create_copy'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.book_id})

class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    permission_required = 'catalog.can_create_copy'
    # get_success_url function tweaked to redirect to related book after delete
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.book_id})


def author_list(request):
    # function based view pagination:
    author_list = Author.objects.all()
    paginator = Paginator(author_list, 20)
    page_number = request.GET.get('page')
    # required for is_paginated layout ifs:
    is_paginated = True if paginator.num_pages > 1 else False
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'is_paginated': is_paginated}
    return render(request, "catalog/author_list.html", context)


def author_detail(request, pk):
    author = Author.objects.get(pk=pk)

    context = {'author': author}
    return render(request, 'catalog/author_detail.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_edit_authors'
    fields = '__all__'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_edit_authors'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_edit_authors'
    # lazily executed version of reverse()
    # required here because URL is being provided to a class-based view
    success_url = reverse_lazy('authors')


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 20
    
    # re-implement get_queryset() to restrict query to solely request.user
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksLibrarianListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan for libarian."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 20
    
    # re-implement get_queryset() to restrict query to solely request.user
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# raise_exception = True raises PermissionDenied, prompting 403 view instead of redirecting to login page
# See: https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-permission-required-decorator
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
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
            return redirect('all-borrowed')

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def return_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ReturnBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # remove relationship with user and save form
            book_instance.borrower = None
            book_instance.due_back = None
            # initial value of 'a' set in modelform
            book_instance.status = form.cleaned_data['status']
            book_instance.save()
            # redirect to a new URL:
            return redirect('all-borrowed')

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReturnBookForm()

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_return_librarian.html', context)