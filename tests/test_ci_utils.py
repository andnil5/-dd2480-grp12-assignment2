from src.ci_utils import parse, create_env_file, clone_git_repo
import os, subprocess, git


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


def test_clone_git_repo():
    """Test that the setup_repo(branch) makes the branch clone, we test this by cloning another branch repo"""
    branch = 'test'
    clone_git_repo(branch)
    repo = git.Repo('./branch_repo')
    assert repo.active_branch.name == branch


# def test_change_dir():
#     """Test that the change dir can actually change to the directory"""
#     dir = './branch_repo'
#     change_dir(dir)
# #     cwd = os.getcwd().split('/')[-2:]
#     path = os.path.normpath(os.getcwd())
#     cwd = path.split(os.sep)[-2:]
#     cwd_stringified = str(cwd[0]) + '/' + str(cwd[1])
#     #remove the first dash/hyphon in the repo, since we have updated it
#     assert cwd_stringified == 'dd2480-grp12-assignment2/branch_repo'
#     os.chdir('./')
