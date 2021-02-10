

BASE_URL="http://b6e79c494870.ngrok.io/"

class Status_response:
    def __init__(self, return_code, context_type, sha, file):
        if context_type == 'test':
            self.context = 'Test: '
            self.state, self.description = self.__generate_test_response(return_code)
        else:
            assert context_type == 'compile'
            self.context = 'Compile: '
            self.state, self.description = self.__generate_compile_response()  
        self.file = BASE_URL+file

    def __generate_compile_response(self):
        return "succes", ""

    def __generate_test_response(self, return_code):
        if return_code == 0:
            return "success", "All tests were collected and passed successfully"
        elif return_code == 1:
            return "failure", "Tests were collected and run but some of the tests failed"
        elif return_code == 2:
            return "error", "Test execution was interrupted by the user"
        elif return_code == 3:
            return "error", "Internal error happened while executing tests"
        elif return_code == 4:
            return "error", "pytest command line usage error"
        elif return_code == 5:
            return "error", "No tests were collected"
        else:
            return "error", "something went wrong"