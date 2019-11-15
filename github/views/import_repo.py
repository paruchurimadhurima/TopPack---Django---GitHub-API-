from django.shortcuts import render
from django.conf import settings

from github.models.packagenamemodel import PackageName
from github.models.packagerepomodel import PackageRepo

import requests
import base64
import json

def maintain_db_records(result, owner, repo):
    if 'decoded_content' not in result:
        packagerepo, created = PackageRepo.objects.get_or_create(
            package=None,
            owner=owner,
            repo=repo,
        )
    else:
        if 'dependencies' in result['decoded_content']:
            for dependency in result['decoded_content']['dependencies']:
                packagename, created = PackageName.objects.get_or_create(
                    name=dependency
                )
                packagerepo = PackageRepo.objects.create(
                    package=packagename,
                    owner=owner,
                    repo=repo
                )
        if 'devDependencies' in result['decoded_content']:
            for dependency in result['decoded_content']['devDependencies']:
                packagename, created = PackageName.objects.get_or_create(
                    name=dependency
                )
                packagerepo = PackageRepo.objects.create(
                    package=packagename,
                    owner=owner,
                    repo=repo
                )


def import_repo(request, owner, repo):
    result = {}
    filename = "package.json"
    if request.method == 'GET':
        endpoint = 'https://api.github.com/repos/'+owner+'/'+repo+'/contents/'+filename
        headers = {'access_token': settings.GITHUB_APP_KEY}
        response = requests.get(endpoint, headers=headers)
        repoendpoint = 'https://api.github.com/repos/' + owner + '/' + repo
        reporesponse = requests.get(repoendpoint, headers=headers)

        if response.status_code == 200:  # SUCCESS
            result = response.json()
            result['success'] = True
            result['decoded_content'] = base64.b64decode(result["content"])
            result['decoded_content'] = json.loads(result['decoded_content'].decode("utf-8"))
            maintain_db_records(result, owner, repo)
        else:
            result['success'] = False
            if response.status_code == 404:  # NOT FOUND
                result['message'] = 'This project does not contain a "%s" file' % filename
                maintain_db_records(result, owner, repo)
            else:
                result['message'] = 'The Github API is not available at the moment. Please try again later.'
    context = {
        'owner': owner,
        'repo': repo,
        'result': result,
    }
    return render(request, 'github/import_repo.html', {'context': context})


