from django.db import models

class Genre(models.Model):
    name = models.CharField(verbose_name="Name")

    def __str__(self):
        return self.name