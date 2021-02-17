from datetime import datetime
from src.status_response import Status_response, StatusType
import git
import os
import subprocess
import sys


def parse(data):
    """Parses the json request data from the GitHub webhook and extracts the
       branch name and head commit sha of the push event that triggered the
       webhook.

    Parameters
    ----------
    data : dict
        The dict representing the request data from the GitHub webhook.

    Returns
    ----------
    res : dict
        If the request data includes a branch name and a head commit sha in
        the same format as specified in the GitHub REST API, `res['branch']`
        will be set to the name of the branch (str) and `res['head_commit']`
        will be set to the sha of the head commit (str). If important data is
        missing in `data`, `res['error']` will be set to an error message (str).
    """
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
    """Creates an environment file with the path ``src/env.py`` defining the
       constants BASE_URL and `TOKEN` as empty strings.

    Returns
    ----------
    None.
    """
    file_path = './src/env.py'
    with open(file_path, 'w+') as f:
        f.write('TOKEN = \'\'\n')
        f.write('BASE_URL = \'\'\n')
        f.close()


def clone_git_repo(branch):
    """Clones the repo into ``./branch_repo`` directory and sets the git repo state to the remote head
       of a specific branch. Adds a dummy environment file ``src/env.py`` in the repo.

    Parameters
    ----------
    branch : str
        The name of the branch that the working tree should be switched to.

    Returns
    ----------
    None.
    """
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
    file : str
        The path (in relation to the root directory) of the log file.
    branch : str
        The name of the branch in which the commit is made.
    sha : str
        The commit sha of the repo state which the process was run in.
    p : subprocess.CompletedProcess
        The completed subprocess whose stdout should be logged.

    Returns
    ----------
    None.
    """
    with open(file, 'w+') as log:
        # print meta data about test run to the log
        log.write("\n{date} :: {branch} -- {sha}:\n".format(date=datetime.now(), branch=branch, sha=sha))
        # print the test output to the log
        log.write(p.stdout.decode('utf-8'))


def run_compile(branch, sha):
    """From the ``git_repo`` directory, run the linter tool flake8 on all the
       files in the directory, ignoring E501 (too long lines). The flake8
       output is logged to a file with the path ``logs_compile/<branch>_<sha>.txt``,
       where ``<branch>`` and ``<sha>`` are substituted to the `branch` and `sha`
       arguments.

    Parameters
    ----------
    branch : str
        The name of the branch in which the commit is made.
    sha : str
        The commit sha of the repo state that should be analysed.

    Returns
    ----------
    status_response.Status_response
        A `src.status_response.Status_response` instance representing the
        result of the analysis.
    """
    os.chdir('./branch_repo')
    sub_proc = subprocess.run([sys.executable, '-m', 'flake8', '--ignore=E501', '../branch_repo/'], capture_output=True)
    os.chdir('../logs_compile')
    file = "{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    os.chdir('..')
    return Status_response(sub_proc.returncode, StatusType.compile, sha, '/logs_compile/' + file)


def run_test(branch, sha):
    """Runs all the tests within the current directory with pytest. The tests
       must be written in files with names on the form ``test*.py`` or ``*test.py``.
       The pytest output is logged to a file with the path
       ``logs_tests/<branch>_<sha>.txt``, where ``<branch>`` and ``<sha>`` are
       substituted to the `branch` and `sha` arguments.

    Parameters
    ----------
    branch : str
        The name of the branch in which the commit is made.
    sha : str
        The commit sha of the repo state that should be tested.

    Returns
    ----------
    status_response.Status_response
        A `src.status_response.Status_response` instance representing the
        result of the test.
    """
    os.chdir('./branch_repo')
    sub_proc = subprocess.run([sys.executable, "-m", "pytest", "tests"], capture_output=True)
    os.chdir('../logs_tests')
    file = "{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    os.chdir('..')
    return Status_response(sub_proc.returncode, StatusType.test, sha, '/logs_tests/' + file)
