from django.db import models
import uuid

class Genre(models.Model):
    name = models.CharField(verbose_name="Name")

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name")
    last_name = models.CharField(verbose_name="Last Name")

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(verbose_name="Title")
    summary = models.TextField(verbose_name="Summary")
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    author = models.ForeignKey(to="Author",
                               verbose_name="Author",
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    genre = models.ManyToManyField(to="Genre", verbose_name="Genre")

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4)
    due_back = models.DateField(verbose_name="Available", null=True, blank=True)
    book = models.ForeignKey(to="Book",
                             verbose_name="Book",
                             on_delete=models.SET_NULL,
                             null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Administered'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(verbose_name="Status",
                              max_length=1,
                              choices=LOAN_STATUS,
                              default='a')

    class Meta:
        verbose_name = "Egzempliorius"
        verbose_name_plural = "Egzemplioriai"

    def __str__(self):
        return str(self.uuid)