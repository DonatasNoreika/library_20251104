from django.db import models
import uuid

class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas")

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas")
    last_name = models.CharField(verbose_name="Pavardė")

    def display_books(self):
        return list(book.title for book in self.books.all())

    display_books.short_description = "Knygos"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas")
    summary = models.TextField(verbose_name="Aprašymas")
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    author = models.ForeignKey(to="Author",
                               verbose_name="Autorius",
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name="Žanras (-ai)")

    def display_genre(self):
        genres = self.genre.all()
        result = ""
        for genre in genres:
            result += genre.name + ", "
        return result

    display_genre.short_description = "Žanrai"


    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4)
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)
    book = models.ForeignKey(to="Book",
                             verbose_name="Knyga",
                             on_delete=models.SET_NULL,
                             null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Administered'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(verbose_name="Būsena",
                              max_length=1,
                              choices=LOAN_STATUS,
                              default='a')

    class Meta:
        verbose_name = "Egzempliorius"
        verbose_name_plural = "Egzemplioriai"

    def __str__(self):
        return str(self.uuid)