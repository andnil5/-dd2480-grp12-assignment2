from flask import Flask, request, abort
import ci_utils


app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook():
    """Default route for GitHub webhook. Gets called at every push to any branch."""
    if request.headers['Content-Type'] == 'application/json':
        data = ci_utils.parse(request.json)
        if 'error' in data:
            abort(400)
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
