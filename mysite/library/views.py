from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.count()
    my_context = {
        "num_books": num_books,
        "num_instances": num_instances,
        'num_instances_available': num_instances_available,
        "num_authors": num_authors,
    }
    return render(request, template_name="index.html", context=my_context)


def authors(request):
    context = {
        "authors": Author.objects.all()
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