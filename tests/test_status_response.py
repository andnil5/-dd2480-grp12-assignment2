import pytest
import requests_mock
from src.status_response import Status_response, StatusType, Status
from src.env import BASE_URL


@pytest.fixture
def dummy_Status_response():
    """Get a dummy instance of `Status_response`.

    Returns
    ----------
    Status_response
        An instance of the `Status_response` class with the instance
        variables set to undefined values.
    """
    return Status_response(0, StatusType.compile, '', '')


def test_generate_compile_response(dummy_Status_response):
    """Test that `__generate_compile_response` returns the expected states for
       some valid flake8 return codes.

    Parameters
    ----------
    dummy_Status_response : Status_response
        An instance of the `Status_response` class. The values of the instance
        variables are unimportant.
    """
    test_cases = [
        (0, Status.success),
        (1, Status.failure),
        (10, Status.pending)
    ]
    for code, expected_state in test_cases:
        state, _ = dummy_Status_response._Status_response__generate_compile_response(code)
        assert state == expected_state


def test_generate_compile_response_invalid(dummy_Status_response):
    """Test that `__generate_compile_response` returns an error
       state when an invalid return code is given.

    Parameters
    ----------
    dummy_Status_response : Status_response
        An instance of the `Status_response` class. The values of the instance
        variables are unimportant.
    """
    invalid_codes = [99, 3, 'hello']
    for code in invalid_codes:
        state, _ = dummy_Status_response._Status_response__generate_compile_response(code)
        assert state == Status.error


def test_generate_test_response(dummy_Status_response):
    """Test that `__generate_test_response` returns the expected states for
       some valid pytest return codes.

    Parameters
    ----------
    dummy_Status_response : Status_response
        An instance of the `Status_response` class. The values of the instance
        variables are unimportant.
    """
    test_cases = [
        (0, Status.success),
        (1, Status.failure),
        (4, Status.error),
        (10, Status.pending)
    ]
    for code, expected_state in test_cases:
        state, _ = dummy_Status_response._Status_response__generate_test_response(code)
        assert state == expected_state


def test_generate_test_response_invalid(dummy_Status_response):
    """Test that `__generate_test_response` returns an error
       state when an invalid return code is given.

    Parameters
    ----------
    dummy_Status_response : Status_response
        An instance of the `Status_response` class. The values of the instance
        variables are unimportant.
    """
    invalid_codes = [99, 6, 'hello']
    for code in invalid_codes:
        state, _ = dummy_Status_response._Status_response__generate_test_response(code)
        assert state == Status.error


def test_status_response_init_file():
    """Test that initialization of a `Status_response` instance sets the
       instance variables to the expected values when the file name is a
       non-empty string.
    """
    sha = 'hohohoji'
    code = 10
    file = 'file.txt'
    s = Status_response(code, StatusType.compile, sha, file)
    assert s.context == 'Compile: '
    assert s.state == Status.pending
    assert s.sha == sha
    assert s.url == BASE_URL + file


def test_status_response_init_empty_file():
    """Test that initialization of a `Status_response` instance sets the
       instance variables to the expected values when the file name is an
       empty string.
    """
    sha = 'hohohoji'
    code = 0
    file = ''
    s = Status_response(code, StatusType.test, sha, file)
    assert s.context == 'Test: '
    assert s.state == Status.success
    assert s.sha == sha
    assert s.url == ''


def test_send_status():
    """Test that `Status_response.send_status` sends a POST request to the
       correct URL for a given commit.
    """
    with requests_mock.Mocker() as m:
        sha = '12345'
        code = 0
        file = 'file.txt'
        # Mock the GitHub REST API for a specific commit status request
        m.post('https://api.github.com/repos/andnil5/dd2480-grp12-assignment2/statuses/12345', status_code=201)
        response = Status_response(code, StatusType.test, sha, file).send_status()
        assert response.status_code == 201
