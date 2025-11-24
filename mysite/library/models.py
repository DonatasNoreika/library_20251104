from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(to=User, verbose_name=_("User"), on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="profile_pics", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"

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
    name = models.CharField(verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(verbose_name=_("First Name"))
    last_name = models.CharField(verbose_name=_("Last Name"))
    description = HTMLField(verbose_name=_("Description"), default="")

    def display_books(self):
        return list(book.title for book in self.books.all())

    display_books.short_description = _("Books")

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(verbose_name=_("Title"))
    summary = models.TextField(verbose_name=_("Summary"))
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    author = models.ForeignKey(to="Author",
                               verbose_name=_("Author"),
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name=_("Genres"))
    cover = models.ImageField(verbose_name=_("Cover"), upload_to="covers", null=True, blank=True)

    def display_genre(self):
        genres = self.genre.all()
        result = ""
        for genre in genres:
            result += genre.name + ", "
        return result

    display_genre.short_description = _("Genres")


    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4)
    due_back = models.DateField(verbose_name=_("Due Back"), null=True, blank=True)
    book = models.ForeignKey(to="Book",
                             verbose_name=_("Book"),
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name="instances")

    LOAN_STATUS = (
        ('d', _('Administered')),
        ('t', _('Taken')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )
    status = models.CharField(verbose_name=_("Status"),
                              max_length=1,
                              choices=LOAN_STATUS,
                              default='a')

    reader = models.ForeignKey(to=User,
                               verbose_name=_("Reader"),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    class Meta:
        verbose_name = _("Book Instance")
        verbose_name_plural = _("Book Instances")

    def __str__(self):
        return str(self.uuid)


class BookReview(models.Model):
    book = models.ForeignKey(to="Book",
                             verbose_name=_("Book"),
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name="reviews")
    reviewer = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"))

    class Meta:
        verbose_name = _("Book Review")
        verbose_name_plural = _("Book Reviews")
        ordering = ['-pk']

