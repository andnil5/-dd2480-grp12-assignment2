from src.ci_utils import parse, change_dir, create_env_file, clone_git_repo
import os
import subprocess
import git
from src.status_response import Status_response, StatusType
import requests
from env import TOKEN, BASE_URL


def test_parse_correct_keys():
    """Test that parse sets both ref and head_commit correctly."""
    data = {
        'ref': 'refs/heads/ci_server',
        'head_commit': {
            'id': '3f28d0dd76b9b1bdd5db5224a1012e5738d2b7b5',
        }
    }
    res = parse(data)
    assert res['branch'] == 'ci_server'
    assert res['head_commit'] == '3f28d0dd76b9b1bdd5db5224a1012e5738d2b7b5'


def test_parse_missing_keys():
    """Test that parse sets error if key does not exist."""
    data = {}
    res = parse(data)

    assert 'ref' not in res
    assert 'head_commit' not in res
    assert res['error'] == 'Missing key'


def test_setup_repo():
    """Test that the setup_repo(branch) makes the branch clone, we test this by cloning another branch repo
    with the assumption that parse and change_dir function as intended"""
    data = {
        'ref': 'refs/heads/test',
        'head_commit': {
            'id': '3f28d0dd76b9b1bdd5db5224a1012e5738d2b7b5',
        }
    }
    res = parse(data)
    # print(res['branch'])
    assert res['branch'] == 'test'
    clone_git_repo(res['branch'])
    change_dir('./branch_repo')
    new_branch = 'webhook_fetch_build'
    cmd = ['git','checkout', new_branch]
    p = subprocess.Popen(cmd)
    p.wait()

    repo = git.Repo('./')
    branch = repo.active_branch
    assert branch.name == new_branch

def test_setup_repo_false():
    """Test that the setup_repo(branch) makes the branch clone, we test this by cloning another branch repo
    with the assumption that parse and change_dir function as intended"""
    data = {
        'ref': 'refs/heads/test',
        'head_commit': {
            'id': '3f28d0dd76b9b1bdd5db5224a1012e5738d2b7b5',
        }
    }
    res = parse(data)
    # print(res['branch'])
    assert res['branch'] == 'test'
    clone_git_repo(res['branch'])
    change_dir('./branch_repo')
    new_branch = 'webhook_fetch_build'
    cmd = ['git','checkout', new_branch]
    p = subprocess.Popen(cmd)
    p.wait()

    repo = git.Repo('./')
    branch = repo.active_branch
    assert branch.name != new_branch
    # url = 'https://github.com/andnil5/dd2480-grp12-assignment2.git'
    # headers = {
    #     'Accept': 'application/vnd.github.v3+json',
    #     'Authorization': 'bearer ' + TOKEN
    # }
    # r = requests.get(url, headers=headers).json()
    # assert r['ref'] == new_branch

def test_change_dir():
    """Test that the change dir can actually change to the directory"""
    dir = './git_repo'
    change_dir(dir)
    cwd = os.getcwd().split('/')[-2:]
    cwd_stringified = str(cwd[0]) + '/' + str(cwd[1])
    #remove the first dash/hyphon in the repo, since we have updated it
    assert cwd_stringified == 'branch_repo/git_repo'
    os.chdir('./')
