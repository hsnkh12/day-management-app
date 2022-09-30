from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from .managers import NotesManager

class Note(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="notes",
        )

    title = models.CharField(
        max_length=25
        )

    text = models.TextField(
        max_length=5000
        )

    date = models.DateField(
        null=True,
        blank=True
        )

    objects = NotesManager()

    def __str__(self):
        return f"Title : {self.title}  -  Date : {str(self.date)}"

    def get_absolute_url(self):
        return reverse("",kwargs={"pk":self.pk})