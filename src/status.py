from enum import Enum

class Status(Enum):
    success = 'success'
    pending = 'pending'
    error = 'error'
    failure = 'failure'