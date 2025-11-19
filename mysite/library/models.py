from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="profile_pics", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)


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
    description = HTMLField(verbose_name="Aprašymas", default="")

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
    cover = models.ImageField(verbose_name="Viršelis", upload_to="covers", null=True, blank=True)

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
                             null=True, blank=True,
                             related_name="instances")

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

    reader = models.ForeignKey(to=User,
                               verbose_name="Skaitytojas",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    class Meta:
        verbose_name = "Egzempliorius"
        verbose_name_plural = "Egzemplioriai"

    def __str__(self):
        return str(self.uuid)


class BookReview(models.Model):
    book = models.ForeignKey(to="Book",
                             verbose_name="Knyga",
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name="reviews")
    reviewer = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Sukūrimo laikas", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas")

    class Meta:
        verbose_name = "Knygos atsiliepimas"
        verbose_name_plural = "Knygos atsiliepimai"
        ordering = ['-pk']

