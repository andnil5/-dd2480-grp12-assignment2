from datetime import datetime
from status_response import Status_response, StatusType
import git
import os
import subprocess
import sys


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


def create_env_file():
    """Creates an environment file with a TOKEN constant."""
    file_path = './src/env.py'
    with open(file_path, 'w+') as f:
        f.write('TOKEN = \'\'\n')
        f.write('BASE_URL = \'\'\n')
        f.close()


def clone_git_repo(branch):
    """clone the branch repo"""
    if os.path.isdir('./branch_repo'):
        git.rmtree('./branch_repo')
    os.mkdir('./branch_repo')
    repo = git.Repo.clone_from('https://github.com/andnil5/dd2480-grp12-assignment2.git', './branch_repo', progress=None)
    gt = repo.git
    gt.checkout(branch)
    os.chdir('./branch_repo')
    create_env_file()
    os.chdir('..')


def log_to_file(file, branch, sha, p):
    """Logs the content of the stdout of a subprocess to a specific log file
       as well as a timestamp for the logging, and the branch and sha
       corresponding to the subprocess.

    Parameters
    ----------
    file: The path (in relation to the root directory) of the logfile - A string.
    branch: The name of the branch in which the commit is made - A string.
    sha: The commit sha of the repo state which the process was run in - A string.
    p: The completed subprocess which stdout should be logged - A CompletedProcess object.

    Returns
    ----------
    None
    """
    with open(file, 'w+') as log:
        # print meta data about test run to the log
        log.write("\n{date} :: {branch} -- {sha}:\n".format(date=datetime.now(), branch=branch, sha=sha))
        # print the test output to the log
        log.write(p.stdout.decode('utf-8'))


def run_compile(branch, sha):
    """From the `git_repo` directory, run the linter tool flake8 on all the
       files in the directory, ignoring E501 (too long lines). The flake8
       output is logged to a file with the path 'logs_compile/<branch>_<sha>.txt',
       where <branch> and <sha> are substituted to the `branch` and `sha`
       arguments.

    Parameters
    ----------
    branch: The name of the branch in which the commit is made - A string.
    sha: The commit sha of the repo state that should be analysed - A string.

    Returns
    ----------
    Status_response: A Status_response instance representing the result of
                     the analysis.
    """
    os.chdir('./branch_repo')
    sub_proc = subprocess.run([sys.executable, '-m', 'flake8', '--ignore=E501', '../branch_repo/'], capture_output=True)
    os.chdir('../logs_compile')
    file = "{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    os.chdir('..')
    return Status_response(sub_proc.returncode, StatusType.compile, sha, '/logs_compile/' + file)


def run_test(branch, sha):
    """Run all the tests within the current directory with pytest. The tests
       must be written in files with names on the form 'test*.py' or '*test.py'.
       The pytest output is logged to a file with the path
       'logs_tests/<branch>_<sha>.txt', where <branch> and <sha> are
       substituted to the `branch` and `sha` arguments.

    Parameters
    ----------
    branch: The name of the branch in which the commit is made - A string.
    sha: The commit sha of the repo state that should be tested - A string.

    Returns
    ----------
    Status_response: A Status_response instance representing the result of
                     the test.
    """
    os.chdir('./branch_repo')
    sub_proc = subprocess.run([sys.executable, "-m", "pytest"], capture_output=True)
    os.chdir('../logs_tests')
    file = "{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    os.chdir('..')
    return Status_response(sub_proc.returncode, StatusType.test, sha, '/logs_tests/' + file)
