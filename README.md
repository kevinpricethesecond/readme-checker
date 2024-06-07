# readme-checker
Gets a list of repos in dockerhub without a description. The repos must be public to be found by the script and a username and password must be passed as params. If no `--namespace` param is provided, it is assumed to be the username.

Quickstart:
`$ python3 readme-checker.py --username <<dockerhub username>> --password <<dockerhub password>> --namespace <<dockerhub namespace>> --file <</path/to/file>>`
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

Options
--username Dockerhub username *required
--password Docker hub password *required
--namespace The dockerhub namespace to search. Defaults to the username *optional
--file Path to the output file. Defaults to None. If this is not provided, output will just print to console. *optional
