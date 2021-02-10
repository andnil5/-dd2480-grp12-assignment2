import json
import requests


TOKEN = ''
def set_commit_status(sha, context, state, description, url):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'bearer ' + TOKEN
    }
    payload = {
        'context': context,
        'state': state,
        'description': description,
        'target_url': url # TO BE CONFIGURED
    }
    return requests.post(
        'https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/statuses/'+sha,
        headers = headers,
        data = json.dumps(payload)
    )
