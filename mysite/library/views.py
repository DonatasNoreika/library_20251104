from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session['num_visits'] = num_visits + 1
    my_context = {
        "num_books": num_books,
        "num_instances": num_instances,
        'num_instances_available': num_instances_available,
        "num_authors": num_authors,
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=my_context)


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        "authors": paged_authors,
    }
    return render(request, template_name="authors.html", context=context)


def author(request, author_id):
    context = {
        "author": Author.objects.get(pk=author_id)
    }
    return render(request, template_name="author.html", context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"


def search(request):
    query = request.GET.get('query')
    books = Book.objects.filter(Q(title__icontains=query) |
                                Q(summary__icontains=query) |
                                Q(author__first_name__icontains=query) |
                                Q(author__last_name__icontains=query))

    authors = Author.objects.filter(Q(first_name__icontains=query) |
                                    Q(last_name__icontains=query))

    context = {
        "query": query,
        "books": books,
        "authors": authors,
    }
    return render(request, template_name="search.html", context=context)


class MyBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "my_books.html"
    context_object_name = "instances"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

