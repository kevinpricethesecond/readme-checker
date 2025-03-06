import sys
import os
import requests
import argparse
import json

docker_url = 'https://hub.docker.com/v2'
repo_base_url = 'https://hub.docker.com/repository/docker'
namespace = None
filename = None
response = {
    "count": 0,
    "names": [],
    "repos": []
}

def get_repo_tags(repo):
    pass

def auth(username, password):
    token = None
    data = {
        "username": username,
        "password": password 
    }
    try:
        resp = requests.post(
            f'{docker_url}/users/login',
            data=data)
        assert resp.status_code == 200
        token = resp.json()['token']
    except AssertionError as e:
        print(f'got {resp.status_code} while authenticating to Docker')
    except Exception as e:
        print(f'Unknown error authenticating to Docker -- {e}')
    return token

def main(username, password, namespace):
    token = auth(username, password)
    next_page = None
    repos = []
    count = 0
    names = []
    try:
        resp = json.loads(json.dumps(requests.get(f'{docker_url}/namespaces/{namespace}/repositories').json()))
    except AssertionError as e:
        pass
    except Exception as e:
        print(f'Uncaught exception getting repos:: {e}')
    check_for_desc(resp['results'])
    next_page = resp['next']
    while next_page:
        resp = json.loads(json.dumps(requests.get(next_page).json()))
        check_for_desc(resp['results'])
        next_page = resp['next']
    print(json.dumps(response))
    print(filename)
    if filename:
        f = open(filename, 'w')
        f.write(json.dumps(response))

def check_for_desc(results):
    for repo in results:
            if repo['description'] == '':
                repo_name = repo['name']
                repo_url = f'{repo_base_url}/{namespace}/{repo_name}'
                response['count'] = response['count'] + 1
                response['names'].append(f'"{repo_name}": "{repo_url}"')
                response['repos'].append(repo)

if __name__ == '__main__':
    username = None
    password = None
    # namespace is global
    p = argparse.ArgumentParser()
    p.add_argument('--username', dest='username')
    p.add_argument('--password', dest='password')
    p.add_argument('--namespace', dest='namespace')
    p.add_argument('--file', dest='filename')
    args = p.parse_args()
    username = args.username
    password = args.password
    namespace = args.namespace if args.namespace else username
    filename = args.filename if args.filename else None
    print(f'checking for repos in {namespace}')
    main(username, password, namespace)
