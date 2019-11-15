from django.shortcuts import render
from django.conf import settings
from github.models.packagerepomodel import PackageRepo
from github.models.searchresultmodel import SearchResults
from django.template import loader, RequestContext
from django.http import HttpResponse

import requests

def search_repo(request):
    keyword = ""
    result = {}
    if request.method == 'GET':
        keyword = request.GET.get('q')
        # keyword = keyword.encode()

        if keyword:
            dbresult = SearchResults.objects.filter(keyword=keyword).first()
            if(dbresult):
                result = dbresult.result
                for package in result['items']:
                    package["imported"] = bool(PackageRepo.objects.filter(repo=package['name'], owner=package['owner']['login']))
                SearchResults.objects.update(keyword=keyword, result=result)
            else:
                endpoint = 'https://api.github.com/search/repositories?q=%s&sort=stars&order=desc&per_page=100' % keyword
                headers = {'access_token': settings.GITHUB_APP_KEY}
                response = requests.get(endpoint, headers=headers)
                if response.status_code == 200:  # SUCCESS
                    result = response.json()
                    result['success'] = True
                    for package in result['items']:
                        package["imported"] = bool(PackageRepo.objects.filter(repo=package['name'], owner=package['owner']['login']))
                    SearchResults.objects.create(keyword=keyword, result=result)
                else:
                    result['success'] = False
                    if response.status_code == 404:  # NOT FOUND
                        result['message'] = 'No data found for "%s"' % keyword
                        SearchResults.objects.create(keyword=keyword, result=result)
                    else:
                        result['message'] = 'The Github API is not available at the moment. Please try again later.'


    context = {
        'keyword': keyword,
        'result': result,
    }
    return render(request, 'github/search_repo.html', {'context': context})



