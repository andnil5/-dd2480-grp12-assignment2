# Assignment 2 - Continuous Integration :earth_americas:

Implementation of a small continuous integration CI server containing core features of continuous integration. 

## Features of CI

The core CI features of continous integration are the following: 

1. **Compilation:**
The branch that has been changed is compiled by the CI server. The compilation is triggered as webhook. Furthermore, a static syntax check is performed.

2. **Testing:**
The CI server executes automated tests on the branch that has been changed. The testing is triggerd as webhook. 

3. **Notification:**
The CI server uses the notification mechanism of setting a [commit status](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-status-checks) on the repository, using [REST API](https://docs.github.com/en/rest/reference/repos#statuses).

4. **Storing history:**
The CI server stores the history of builds, even when the server restarts. A single URL exists that lists all builds, whilst each and every build also has its own URL containing build information (commit identifier, build date and build logs).

## Motivation :man_student: :woman_student:

This is a group assignment, in the course *Software Engineering Fundamentals* at KTH, with the purpose of teaching continuous integration. The assignment is conducted in spring 2021.  

## Architecture :bricks:

The architecture of this project follows the pattern in the following figure.

[![](architecture.PNG)](#Architecture)

### GitHub

**GitHub** is used for the repository. In this project it is used for applying [feature 2](#Features-of-CI), the notification feature, of continuous integration.

### ngrok

[**ngrok**](https://ngrok.com/docs) is used to make the local web server visible externally, on the internet. Furthermore, it is used in order to catch all HTTP traffic going via the tunnel. 

### Flask

Flask is used as Python web framework.

### Build and test

Whenever something is pushed to a particular branch [feature 1 and feature 2](#Features-of-CI), compilation and testing, are conducted. Compilation uses the linter [flake8](https://flake8.pycqa.org/en/latest/), and the tests are constructed using mockups. 

### Logging

Whenever something is pushed to a particular branch [feature 3](#Features-of-CI), storing history, is conducted. The approach for storing history is logging to a file each time a compilation occurs and storing the file. 

## Installation :computer:

Run the following command in order to install all **dependencies** needed to run this project
- `pip install -r /path/to/requirements.txt`

## Usage :books:

### Set PYTHONPATH

Run the following command in order to set the Python path
- `export PYTHONPATH=src`

### Run flake8

**flake8** is automated to run when a push is conducted, but it can also be run directly in the project folder using one of the following commands 
- Linting a specific file `flake8 path/to/file.py`
- Linting the whole project `flake8 path/to/project_folder/`

### Run pytest

**pytest** is automated to run when a push is conducted, but it can also be run directly in the project folder using the following command
- `python -m pytest`

### Run ngrok

**ngrok** is started using the following command
- `ngrok http local_machine_port_number`

This command generates an ngrok "URL" that should be added to `BASE_URL` variable inside the `status_response` file.

### Push to GitHub

To see the status of your push follow the following steps
1. Run ngrok
2. Make a change to a file in the repository
3. `git add .`
4. `git commit -m "some_message"`
5. `git push`
6. Check the repository on GitHub and view the flag to see the status of the push

## Statement of Contributions :thought_balloon:

The members of Group 12 claim to have achieved a P+ result. We feel that we have established something remarkable that we are proud of as a result of for instance our structurized teamwork including usage of for example GitHub Projects. We developed as a team since assignment 1 by evaluating what went good and by identifying our development areas. This meant that we did not have to spend as much time on for example clean-up since we had decided concrete standards before starting the project. 

Moreover, we have set up clear guidelines for consistency in language, variable naming, logic, comments and structure. We aimed to create a descriptive documentation using both a README.md, an api.md, clear docstings and HTML for further clarity. We used relevant and current frameworks for implementation. In addition, we used consistent, reliable and descriptive issue and commit naming and labels. Thus, our technique for creating issues and commits that ultimately provides a good review of our process has been improved and we claim to have achieved P8. Likewise, we claim  to have achieved P7 since we have achieved something remarkable, as a team, that we are very proud of. Last but not least we have achieved P8 since the CI server keeps the history of the past builds. 

Work was distrubuted intelligently between then the 5 team members; the tasks were essentially handled as follows: 

**Maja Tennander**: structure repository, set up `requirements.txt`, make CI server run pytest, write docstrings, clean-up, create tests, code review<br/>
**Carl Johan Freme**: implement flake8 linting for CI server, bug fix, add pytest functionality, code review<br/>
**Anders Nilsson**: create basic CI server, CI interface for GitHub integration, connection to endpoints, api documentation, handle import errors, code review<br/>
**Omid Hazara**: structure repository, create basic CI server, add functionality for cloning and checkout, create tests, code review<br/>
**Jennifer Lindberg**: implement flake8 linting for CI server, add functionality for cloning and checkout, documentation, code review, clean-up 

## Further Documentation :open_file_folder:

Further documentation can be found in the `api.md` file in the `docs` folder. Moreover, further code documentation can be found [here](https://majate.github.io/testing/src/index.html).  