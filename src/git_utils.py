import subprocess
from subprocess import check_output
import os
from datetime import datetime


def parse(data):
    """ parse the json webhook input from github"""
    res = {}
    #branch name
    if 'ref' in data:
        res['branch'] = data['ref'].split("/")[-1]

    # last commit sha
    if 'head_commit' in data and 'id' in data['head_commit']:
        res['head_commit'] = data['head_commit']['id']
    return res

def change_dir(dir):
    os.chdir(dir)

def setup_repo(branch):
    change_dir("./git_repo")
    # ["git","reset", "--hard", "origin/{}".format(branch)]
    cmd = [["git", "fetch"],["git", "checkout", branch], ["git", "pull"]]
    return_code = 0
    for c in cmd:
        p = subprocess.Popen(c)
        if p.wait() != 0:
            print("Failed!!!")
            break

def run_test(branch, sha):
    p = subprocess.run(["python", "-m", "pytest"], capture_output=True)

    file= "logs_tests/{}_{}.txt".format(branch,sha)
    print("Timestamp\t\tBranch\t\tCommit")
    with open("../"+file, 'a+') as log:
        # print meta data about test run to the log
        log.write("\n{date} :: {branch} -- {sha}:\n".format(date=datetime.now(), branch=branch, sha=sha))
        # print the test output to the log
        log.write(p.stdout.decode('utf-8'))
    # print("STD ERRRRRRRRRRR {}".format(p.stderr))
    # print("STD OUTTTTTTTT {}".format(p.stdout))
    print("STD return code {}".format(p.returncode))
    if p.returncode ==0:
        return "success", "", file
    elif p.returncode ==1:
        return "failure", "test failed", file
    else:
        return "error", "something went wrong", file

def run_test2(branch, sha):
    # p = subprocess.run([ "python", "-m", "pytest"], capture_output=True)
    file= "../logs/{}_{}.txt".format(branch,sha)
    with subprocess.Popen(["python", "-m", "pytest"], stdout=PIPE) as proc:
        with open(file, 'a+') as log:
            # print meta data about test run to the log
            log.write("\n{date} :: {branch} -- {sha}:\n".format(date=datetime.now(), branch=branch, sha=sha))
            # print the test output to the log
            log.write(proc.stdout.decode('utf-8'))
            # log.write(proc.stdout.read())

            print(proc.wait())
