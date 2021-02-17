from flask import Flask, request, abort
import src.ci_utils as ci_utils
from src.status_response import Status_response, StatusType
import os
import git

app = Flask(__name__)


def read_file(name):
    """Get the content of a (non-binary) file.

    Parameters
    ----------
    name: A path to the file that should be read - A string.

    Returns
    ----------
    string: The content of the file.
    """

    with open(name) as f:
        file_content = f.read()
    return file_content


@app.route('/logs_compile/<name>')
def get_logfile_compile(name):
    """Show full flake8 output of a specific flake8 run.

    Parameters
    ----------
    name: The name of the log-file corresponding to the specific flake8 run
          on the format '<branch>_<sha>.txt' - A string.

    Returns
    ----------
    string: The full output.
    """
    return read_file("./logs_compile/{}".format(name))


@app.route('/logs_tests/<name>')
def get_logfile_test(name):
    """Show full pytest output of a specific run of the tests.

    Parameters
    ----------
    name: The name of the log-file corresponding to the specific test run
          on the format '<branch>_<sha>.txt' - A string.

    Returns
    ----------
    string: The full output.
    """
    return read_file("./logs_tests/{}".format(name))


@app.route('/hook', methods=['POST'])
def webhook():
    """Default route for GitHub webhook. Gets called at every push to any branch."""
    if request.headers['Content-Type'] == 'application/json':
        data = ci_utils.parse(request.json)
        if 'error' in data:
            abort(400)

        # Set commit compile status flag to pending
        Status_response(10, StatusType.compile, data['head_commit'], '').send_status()

        # Set commit test status flag to pending
        Status_response(10, StatusType.test, data['head_commit'], '').send_status()

        # Setup branch repo to git_repo which is gitignored
        ci_utils.clone_git_repo(data['branch'])

        # Run compile
        response = ci_utils.run_compile(data['branch'], data['head_commit'])
        response.send_status()

        # Run tests
        response = ci_utils.run_test(data['branch'], data['head_commit'])
        response.send_status()

        # Remove the branch repo after testing
        if os.path.isdir('./branch_repo'):
            git.rmtree('./branch_repo')

        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
