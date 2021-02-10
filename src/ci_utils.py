import subprocess
from subprocess import check_output
import os


def parse(data):
    """Parse the json webhook input from github."""
    res = {}
    # branch name
    if 'ref' in data:
        res['branch'] = data['ref'].split('/')[-1]
    else:
        res['error'] = 'Missing key'

    # last commit sha
    if 'head_commit' in data and 'id' in data['head_commit']:
        res['head_commit'] = data['head_commit']['id']
    else:
        res['error'] = 'Missing key'
    return res


def change_dir(dir):
    """helper function to change dir"""
    os.chdir(dir)


def setup_repo(branch):
    """clone the branch repo"""
    change_dir("./git_repo")
    cmd = [["git", "fetch"], ["git", "checkout", branch], ["git", "pull"]]
    for c in cmd:
        p = subprocess.Popen(c)
        if p.wait() != 0:
            print("Failed!!!")
            break
