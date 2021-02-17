from enum import Enum
import json
import requests
from src.env import TOKEN, BASE_URL


class Status(Enum):
    """An enumeration representing the possible commit states defined by
       the GitHub REST API.
    """
    success = "success"
    pending = "pending"
    error = "error"
    failure = "failure"


class StatusType(Enum):
    """An enumeration representing the different commit contexts used by the
       CI server.
    """
    compile = "compile"
    test = "test"


class Status_response:
    """A class that generates POST requests for commit status updates via the
       GitHub REST API from partial results of different steps of the CI server
       workflow.
    """

    def __init__(self, return_code, context_type, sha, file):
        """Generates the POST request data, without sending the request.

        Parameters
        ----------
        return_code : int
            The return code of the subprocess that was run as part of the
            CI server workflow step that should cause the commit update. A
            `return_code` of value 10 indicates that the step is started without
            being finished (this will set the commit state to pending).
        context_type : StatusType member
            A enum member of the `StatusType` enumeration representing which
            context the status update concerns.
        sha : str
            The sha of the commit that should have its status updated.
        file : str
            The path to the log file corresponding to the output of the
            subprocess. If no such file exist, set this value to the empty string.

        Returns
        ----------
        None.
        """
        if context_type == StatusType.test:
            self.context = 'Test: '
            self.state, self.description = self.__generate_test_response(return_code)
        else:
            assert context_type == StatusType.compile
            self.context = 'Compile: '
            self.state, self.description = self.__generate_compile_response(return_code)
        self.url = BASE_URL + file if len(file) > 0 else ''
        self.sha = sha

    def __generate_compile_response(self, return_code):
        """Convert return codes from flake8 to fitting commit states and
           descriptions. If `return_code` has value 10, the state will be set
           to pending.

        Returns
        ----------
        linting status : Status
            success - All files passed linter successfully.
            failure - One or more files did not pass linter.
            pending - Lint analysis started.
            error - Server error.
        """
        if return_code == 0:
            return Status.success, "All files passed successfully"
        elif return_code == 1:
            return Status.failure, "Code did not pass linter"
        elif return_code == 10:
            return Status.pending, ""
        else:
            return Status.error, "Server error"

    def __generate_test_response(self, return_code):
        """Convert return codes from pytest to fitting commit states and
           descriptions. If `return_code` has value 10, the state will be set
           to pending.

        Returns
        ----------
        test status : Status
            success - All tests were collected and passed successfully.
            failure - One or more test failed.
            pending - Test analysis started.
            error - Internal server error.
        """
        if return_code == 0:
            return Status.success, "All tests were collected and passed successfully"
        elif return_code == 1:
            return Status.failure, "Tests were collected and run but some of the tests failed"
        elif return_code == 2:
            return Status.error, "Test execution was interrupted by the user"
        elif return_code == 3:
            return Status.error, "Internal error happened while executing tests"
        elif return_code == 4:
            return Status.error, "pytest command line usage error"
        elif return_code == 5:
            return Status.error, "No tests were collected"
        elif return_code == 10:
            return Status.pending, ""
        else:
            return Status.error, "Server error"

    def send_status(self):
        """Sends the generated POST request to the GitHub REST API.

        Returns
        ----------
        requests.Response
            A `requests.Response` instance representing the response from the
            GitHub REST API.
        """
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'bearer ' + TOKEN
        }
        payload = {
            'context': self.context,
            'state': self.state.value,
            'description': self.description,
            'target_url': self.url
        }
        return requests.post(
            'https://api.github.com/repos/andnil5/dd2480-grp12-assignment2/statuses/{}'.format(self.sha),
            headers=headers,
            data=json.dumps(payload)
        )
