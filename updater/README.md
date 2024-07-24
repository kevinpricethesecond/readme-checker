# Dockerhub readme updater

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