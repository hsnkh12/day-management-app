from django.db import models


class NotesManager(models.Manager):

    def get_relatd_notes(self,user):
        return self.select_related("user").filter(user=user)