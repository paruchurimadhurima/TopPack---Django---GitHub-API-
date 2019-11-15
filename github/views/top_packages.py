from django.shortcuts import render
from django.db.models import Q, Count
from github.models.packagenamemodel import PackageName
from github.models.packagerepomodel import PackageRepo

def top_packages_list(request):
    results = PackageRepo.objects.exclude(package__isnull=True).values('package').annotate(count = Count('repo')).order_by('-count')[:10]
    for result in results:
        result["package"] = PackageName.objects.get(pk=result["package"])
    context = {
        'result': results,
    }
    return render(request, 'github/top_packages.html', {'context': context})
