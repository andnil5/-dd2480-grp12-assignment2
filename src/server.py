from flask import Flask, request, abort
import ci_utils
from status_response import Status_response, StatusType


app = Flask(__name__)


def get_logfile(path):
    """Gets the content of a (non-binary) file.

    Parameters
    ----------
    name : str
        A path to the file that should be read.

    Returns
    ----------
    str
        The content of the file. Returns a 404 response if file is not found.
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
    """A view function handling GET requests to the ``/logs_compile/<name>``
       endpoint. Shows full flake8 output of a specific flake8 run.

    Parameters
    ----------
    name : str
        The name of the log file corresponding to the specific flake8 run
        on the format ``<branch>_<sha>.txt``.

    Returns
    ----------
    200 - OK
        Response with payload of media type *text/html* including the plain text
        output of the specified flake8 run.
    500 -  Internal Server Error
        If `name` does not correspond to the log file of a specific flake8 run.
    """
    return get_logfile("./logs_compile/{}".format(name))


@app.route('/logs_tests/<name>')
def get_logfile_test(name):
    """A view function handling GET requests to the ``/logs_tests/<name>``
       endpoint. Shows full pytest output of a specific run of the tests.

    Parameters
    ----------
    name : str
        The name of the log-file corresponding to the specific test run
        on the format ``<branch>_<sha>.txt``.

    Returns
    ----------
    200 - OK
        Response with payload of media type *text/html* including the plain text
        output of the specified pytest run.
    500 - Internal Server Error
        If `name` does not correspond to the log file of a specific pytest run.
    """
    return get_logfile("./logs_tests/{}".format(name))


@app.route('/hook', methods=['POST'])
def webhook():
    """A view function handling POST requests to the ``/hook`` endpoint. If the
       request body is on the format of a GitHub push event (as defined by the
       GitHub REST API), the CI server will be triggered to check the push.

    Returns
    ----------
    200 - OK
        If the CI server runs successfully. The response will include a
        payload of media type *text/html* with the content "success".
    400 - Bad Request
        If the request body is not on the format of a GitHub push event.
    """
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
