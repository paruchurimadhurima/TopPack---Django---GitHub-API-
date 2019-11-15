from django.urls import path
from .views import top_packages, search_repo, import_repo

urlpatterns = [
    path('', top_packages.top_packages_list, name='top_packages_list'),
    path('search_repositories', search_repo.search_repo, name='search_repo'),
    path(r'import_repo/<str:owner>/<str:repo>', import_repo.import_repo, name='import_repo'),
]
