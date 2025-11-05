from django.db import models

class Genre(models.Model):
    name = models.CharField(verbose_name="Name")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name")
    last_name = models.CharField(verbose_name="Last Name")

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

    def __str__(self):
        return self.title