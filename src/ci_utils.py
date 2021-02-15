import subprocess
import os
import sys
from datetime import datetime
from status_response import Status_response, StatusType


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


def change_dir(dir):
    """Changes the current working directory of the OS.

    Parameters
    ----------
    dir : str
        The path (relative or absolute) to the new directory.

    Returns
    ----------
    None.
    """
    os.chdir(dir)


def create_env_file():
    """Creates an environment file with the path ``src/env.py`` defining the
       constant `TOKEN` as an empty string.

    Returns
    ----------
    None.
    """
    f = open('src/env.py', 'w')
    f.write('TOKEN = \'\'\n')
    f.close()


def setup_repo(branch):
    """Moves the OS to the directory ``./git_repo``, creates a dummy environment
       file in that directory and sets the git repo state to the remote head
       of a specific branch.

    Parameters
    ----------
    branch : str
        The name of the branch that the working tree should be switched to.

    Returns
    ----------
    None.
    """
    change_dir('./git_repo')
    create_env_file()
    cmd = [['git', 'fetch'], ['git', 'checkout', branch], ['git', 'pull']]
    for c in cmd:
        p = subprocess.Popen(c)
        if p.wait() != 0:
            print('Failed!!!')
            break


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
    with open("../" + file, 'a+') as log:
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
    sub_proc = subprocess.run(['python{}'.format(sys.version[:3]), '-m', 'flake8', '--ignore=E501', '../git_repo/'], capture_output=True)
    file = "logs_compile/{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    return Status_response(sub_proc.returncode, StatusType.compile, sha, file)


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
    sub_proc = subprocess.run(["python3", "-m", "pytest"], capture_output=True)
    file = "logs_tests/{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    return Status_response(sub_proc.returncode, StatusType.test, sha, file)
