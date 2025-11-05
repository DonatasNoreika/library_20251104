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

