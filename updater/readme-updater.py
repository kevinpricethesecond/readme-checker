import os
import sys
import json
import requests
import docker
import argparse
from dotenv import dotenv_values

## global vars
debug=False

class env:
    DOCKER_USER=None
    DOCKER_PASS=None
    PUSHRM_PROVIDER='dockerhub'
    PUSHRM_FILE='/myvol/README.md'
    PUSHRM_SHORT=None
    PUSHRM_TARGET=None
    PUSHRM_DEBUG=1

    def __init__(self, path):
        self.get_common_env(path)


    def get_common_env(self, path):
        env_dict = {}
        try:
            environment = dotenv_values(dotenv_path=path)
        except Exception as e:
            print(f'Unhandled exception loading env at {path}:: \n\t{e}')
        self.override_env(environment)
        if debug:
            print('Got common env values: ')
            self.debug_env()
        return environment

    def override_env(self, environment):
        for key in environment:
            setattr(self, key, environment[key])

    def debug_env(self):
        hidden_pass = ''
        if self.DOCKER_PASS and self.DOCKER_PASS != '':
            for char in self.DOCKER_PASS:
                hidden_pass += '*'

        print(f'''
            DOCKER_USER={self.DOCKER_USER}
            DOCKER_PASS={hidden_pass}
            PUSHRM_PROVIDER={self.PUSHRM_PROVIDER}
            PUSHRM_FILE={self.PUSHRM_FILE}
            PUSHRM_SHORT={self.PUSHRM_SHORT}
            PUSHRM_TARGET={self.PUSHRM_TARGET}
            PUSHRM_DEBUG={self.PUSHRM_DEBUG}
            ''')
        
    def to_dict(self):
        return {
            "DOCKER_USER": f"{self.DOCKER_USER}",
            "DOCKER_PASS": f"{self.DOCKER_PASS}",
            "PUSHRM_PROVIDER": f"{self.PUSHRM_PROVIDER}",
            "PUSHRM_FILE": f"{self.PUSHRM_FILE}",
            "PUSHRM_SHORT": f"{self.PUSHRM_SHORT}",
            "PUSHRM_TARGET": f"{self.PUSHRM_TARGET}",
            "PUSHRM_DEBUG": f"{self.PUSHRM_DEBUG}"
        }
            
    
def get_map_from_file(path):
    with open(path, 'r') as file:
        data = file.read()
    return json.loads(data)

def get_readme_from_url(url):
    resp = requests.get(url)
    # print(resp)
    # print(resp.text)
    return resp.text

def update_readme(tmpfile_path, env):
    if debug:
        print(f'Updating Dockerhub repo: {env.PUSHRM_TARGET}')
    client = docker.from_env()
    try:
        container = client.containers.run("chko/docker-pushrm", detach=True, environment=env.to_dict(), volumes=[f'{tmpfile_path}:{env.PUSHRM_FILE}'])
    except Exception as e:
        print(f'Error trying to update readme: {e}')
    if debug:
        print(f'have container: {container.name}')
    for line in container.logs(stream=True): 
        print(line.strip())

def main(env):
    mapping = get_map_from_file('map.json')
    tmpfile_path = os.path.expanduser('~/tmp/dockerhubtmpfile.txt')
    if debug:
        print(f'Attempting to write readme contents to {tmpfile_path}')
    for repo in mapping:
        # override the target repo in the env
        dockerhub_target = mapping[repo].get('dockerhub_target')
        readme_location = mapping[repo].get('readme_location')
        short_desc = mapping[repo].get('short_desc')
        overrides = {
            "PUSHRM_TARGET": dockerhub_target,
            "PUSHRM_SHORT": short_desc
        }
        env.override_env(overrides)

        # save readme into tmp file for mounting in update_readme
        readme = get_readme_from_url(readme_location)
        with open(tmpfile_path, 'w+') as f:
            f.write(readme)
        
        # do update
        update_readme(tmpfile_path, env)

        # cleanup
        os.remove(tmpfile_path)

if __name__ == '__main__':
    env_fpath = None
    p = argparse.ArgumentParser()
    p.add_argument('--env_file', '-f', dest='env_fpath', default='../../.env')
    p.add_argument('--verbose', '-v', dest='verbose', action='store_true')
    p.add_argument('--user', '-u', dest='DOCKER_USER')
    p.add_argument('--password', '-p', dest='DOCKER_PASS')
    p.add_argument('--provider', dest='PUSHRM_PROVIDER')
    p.add_argument('--overview', '-o', dest='PUSHRM_FILE')
    p.add_argument('--description', dest='PUSHRM_SHORT')
    p.add_argument('--repo', '-r', dest='PUSHRM_TARGET')
    args = p.parse_args()
    globals()['debug'] = bool(args.verbose)

    if args.env_fpath:
        if debug:
            print(f'have env file path: {args.env_fpath}')
        env_fpath = os.path.expanduser(args.env_fpath)

    environment = env(env_fpath)
    overrides = {}
    # dynamically assign args
    # but skip verbose and env path
    vars(args).pop('verbose')
    vars(args).pop('env_fpath')
    for arg in vars(args):
        tmp = getattr(args, arg)
        if tmp is not None:
            overrides[arg] = tmp

    # load override env with provided arg vals
    if overrides is not {}:
        if debug:
            print(f'Overriding env vars with: {overrides}' if overrides != {} else 'No env overrides given')
        environment.override_env(overrides)

    main(environment)
