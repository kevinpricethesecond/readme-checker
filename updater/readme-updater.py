import os
import sys
import json
import requests
import docker

class env:
    DOCKER_USER=''
    DOCKER_PASS=''
    PUSHRM_PROVIDER=dockerhub 
    PUSHRM_FILE=/myvol/README.md 
    PUSHRM_SHORT=''
    PUSHRM_TARGET=''
    PUSHRM_DEBUG=1 
    def __init__(path):
        with open(path, 'r') as f:
            lines = f.read()
            ## TODO: assign vars from file

def get_map_from_file(path):
    with open(path, 'r') as file:
        data = file.read()
    return json.loads(data)

def get_readme_from_url(url):
    resp = requests.get(url)
    print(resp)
    print(resp.text)
    return resp.text

def get_common_env(path):

    

def update_readme(repo, readme):
    client = docker.from_env()
    container = client.containers.run("chko/docker-pushrm", "/bin/sh", "-c", "/docker-pushrm", detach=True, environment=env)
    print(f'have container {container}')
    for line in container.logs(stream=True):
        print(line.strip())

def main():
    mapping = get_map_from_file('map.json')
    for repo in mapping:
        readme = get_readme_from_url(mapping[repo])
        update_readme(repo, readme)



if __name__ == '__main__':
    main()
