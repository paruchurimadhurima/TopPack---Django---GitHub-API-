from django.contrib import admin
from .models.packagenamemodel import PackageName
from .models.packagerepomodel import PackageRepo
from .models.searchresultmodel import SearchResults

admin.site.register(PackageName)
admin.site.register(PackageRepo)
admin.site.register(SearchResults)
