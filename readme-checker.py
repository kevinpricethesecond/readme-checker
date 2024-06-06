import sys
import os
import requests
import argparse
import json

docker_url = 'https://hub.docker.com/v2/'

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
    try:
        resp = json.loads(json.dumps(requests.get(f'{docker_url}/namespaces/{namespace}/repositories').json()))
    except AssertionError as e:
        pass
    except Exception as e:
        print(f'Uncaught exception getting repos:: {e}')

    next_page = resp['next']
    while next_page:
        resp = json.loads(json.dumps(requests.get(next_page).json()))
        for repo in resp['results']:
            repos.append(repo)
        next_page = resp['next']
    print(json.dumps(repos))



if __name__ == '__main__':
    username = None
    password = None
    namespace = None
    p = argparse.ArgumentParser()
    p.add_argument('--username', dest='username')
    p.add_argument('--password', dest='password')
    p.add_argument('--namespace', dest='namespace')
    args = p.parse_args()
    username = args.username
    password = args.password
    namespace = args.namespace if args.namespace else username
    print(f'checking for repos in {namespace}')
    main(username, password, namespace)
