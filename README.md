# readme-checker
Gets a list of repos in dockerhub without a description. The repos must be public to be found by the script and a username and password must be passed as params. If no `--namespace` param is provided, it is assumed to be the username.

Usage:
`$ python3 readme-checker.py --username <<dockerhub username>> --password <<dockerhub password>> --namespace <<dockerhub namespace>>`
```
{
    "count": count,
    "names": [
        "repo name": "dockerhub url"
    ],
    "repos": [{
        "name": "repo name", 
        "namespace": "repo namespace", 
        "repository_type": "image", 
        "status": 1, 
        "status_description": "active", 
        "description": "", 
        "is_private": false, 
        "star_count": count, 
        "pull_count": count, 
        "last_updated": "timestamp", 
        "date_registered": "timestamp", 
        "affiliation": "", 
        "media_types": ["application/vnd.docker.container.image.v1+json"], 
        "content_types": ["image"], 
        "categories": []
    }]
}

```
