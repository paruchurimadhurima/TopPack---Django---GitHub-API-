from django.db import models
from github.models.packagenamemodel import PackageName

class PackageRepo(models.Model):
    package = models.ForeignKey(PackageName, on_delete=models.CASCADE, null=True)
    owner = models.CharField(max_length=150, null=False)
    repo = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.repo