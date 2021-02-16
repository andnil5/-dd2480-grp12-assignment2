from enum import Enum
import json
import requests
from env import TOKEN


BASE_URL = "http://b6e79c494870.ngrok.io/"


class Status(Enum):
    success = "success"
    pending = "pending"
    error = "error"
    failure = "failure"


class StatusType(Enum):
    compile = "compile"
    test = "test"


class Status_response:

    def __init__(self, return_code, context_type, sha, file):
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
        if return_code == 0:
            return Status.success, "All files passed successfully"
        elif return_code == 1:
            return Status.failure, "Code did not pass linter"
        elif return_code == 10:
            return Status.pending, ""
        else:
            return Status.error, "Something went wrong"

    def __generate_test_response(self, return_code):
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
            return Status.error, "Something went wrong"

    def send_status(self):
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
