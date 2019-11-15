from django.db import models
from jsonfield import JSONField

class SearchResults(models.Model):
    keyword = models.CharField(max_length=150, null=False)
    result = JSONField(default=None)

    def __str__(self):
        return self.keyword