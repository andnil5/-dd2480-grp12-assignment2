from flask import Flask, request, json, abort
import ci_module
import git_utils
BASE_URL="http://b6e79c494870.ngrok.io/"
app = Flask(__name__)

@app.route('/logs_tests/<name>')
def get_logfile_test(name):
    with open("./logs_tests/{}".format(name)) as f:
        file_content = f.read()
    return file_content

@app.route('/logs_compile/<name>')
def get_logfile_compile(name):
    with open("./logs_compile/{}".format(name)) as f:
        file_content = f.read()
    return file_content

@app.route('/', methods=['POST'])
def webhook():
    if request.headers['Content-Type'] == 'application/json':
        #print(request.json)
        #call parse function from gitutils to parse webhook input
        data = git_utils.parse(request.json)
        #Set the state of the commit to pending
        response = ci_module.set_commit_status(
            sha= data['head_commit'],
            context='Compile: ',
            state='pending',
            description='',
            url=''
        )
        #Set the state of the commit to pending
        response = ci_module.set_commit_status(
            sha= data['head_commit'],
            context='Test: ',
            state='pending',
            description='',
            url=''
        )

        #setup branch repo to git_repo which is gitignored
        git_utils.setup_repo(data['branch'])
        state, description, file = git_utils.run_test(data['branch'], data['head_commit'])
        response = ci_module.set_commit_status(
            sha= data['head_commit'],
            context='Test: ',
            state=state,
            description=description,
            url=BASE_URL+file
        )
        git_utils.change_dir("../")
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
