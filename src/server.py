from flask import Flask, request, abort
import ci_utils
from status_response import Status_response, StatusType


app = Flask(__name__)


def get_logfile(path):
    """Gets the content of a (non-binary) file.

    Parameters
    ----------
    path: A path to the file that should be read - A string.

    Returns
    ----------
    string: The content of the file. Returns a 404 response if file is not found.
    """
    try:
        f = open(path)
        file_content = f.read()
        f.close()
        return file_content
    except FileNotFoundError:
        abort(404)


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
    return get_logfile("./logs_compile/{}".format(name))


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
    return get_logfile("./logs_tests/{}".format(name))


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
        ci_utils.setup_repo(data['branch'])

        # Run compile
        response = ci_utils.run_compile(data['branch'], data['head_commit'])
        response.send_status()

        # Run tests
        response = ci_utils.run_test(data['branch'], data['head_commit'])
        response.send_status()

        ci_utils.change_dir("../")
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
