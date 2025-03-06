# readme-checker
Gets a list of repos in dockerhub without a description. The repos must be public to be found by the script and a username and password must be passed as params. If no `--namespace` param is provided, it is assumed to be the username.

## Quickstart:
### checking readmes
Use the below command to get a list of repos without a descriptiuon (overview)
`$ python3 readme-checker.py --username <<dockerhub username>> --password <<dockerhub password>> --namespace <<dockerhub namespace>> --file <</path/to/file>>`
response format:
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

### updating readmes
Use the below command to update a readme.
`python3 readme-updater.py`

You *must* have an .env file containing a dockerhub username/password with access to the repos you're trying to update. Example of this is in ./updater/.env-example
You *must* have a map.json file with the following params:
```
"dockerhub_target" --> the repo in Dockerhub that you want to update, in the format docker.io/<namepsace>/<repo name>
"readme_location" --> the url to the README.md file you want as the overview of the Dockerhub repo. This script will pull it down and put it in Docklerhub (using python requests.get).
"short_desc" --> a short description of the repo. Usually optional.
```
an example of this is at ./updater/map.json
