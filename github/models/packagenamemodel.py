from django.db import models

class PackageName(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.name