from flask import Flask, request, abort
import ci_utils
from status_response import Status_response, StatusType


app = Flask(__name__)


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
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
