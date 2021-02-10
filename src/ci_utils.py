import subprocess
import os
import sys
from datetime import datetime
from status_response import Status_response, StatusType


def parse(data):
    """ parse the json webhook input from github"""
    res = {}
    # branch name
    if 'ref' in data:
        res['branch'] = data['ref'].split("/")[-1]
    else:
        res['error'] = 'Missing branch'

    # last commit sha
    if 'head_commit' in data and 'id' in data['head_commit']:
        res['head_commit'] = data['head_commit']['id']
    else:
        res['error'] = 'Missing head commit'
    return res


def change_dir(dir):
    os.chdir(dir)


def setup_repo(branch):
    change_dir("./git_repo")
    cmd = [["git", "fetch"], ["git", "checkout", branch], ["git", "pull"]]
    for c in cmd:
        p = subprocess.Popen(c)
        if p.wait() != 0:
            print("Failed!!!")
            break


def log_to_file(file, branch, sha, p):
    with open("../" + file, 'a+') as log:
        # print meta data about test run to the log
        log.write("\n{date} :: {branch} -- {sha}:\n".format(date=datetime.now(), branch=branch, sha=sha))
        # print the test output to the log
        log.write(p.stdout.decode('utf-8'))


def run_test(branch, sha):
    sub_proc = subprocess.run(["python", "-m", "pytest"], capture_output=True)
    file = "logs_tests/{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    return Status_response(sub_proc.returncode, StatusType.test, sha, file)


def run_compile(branch, sha):
    sub_proc = subprocess.run(['python{}'.format(sys.version[:3]), '-m', 'flake8', '--ignore=E501', '../git_repo/'], capture_output=True)
    file = "logs_compile/{}_{}.txt".format(branch, sha)
    log_to_file(file, branch, sha, sub_proc)
    return Status_response(sub_proc.returncode, StatusType.compile, sha, file)
