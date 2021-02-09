## CI api with GitHub

### Adds a commit status


    POST 'https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/statuses/{SHA}'

Adds a commit status for a given commit SHA. The user can set the parameters as follows: 

| Name 	        | In 	    | Description 	                        |
|---	        |---	    |---	                                |
| SHA 	        | path 	    | The commit SHA. 	|
| TOKEN         | header  	| Authorization token, will probably change value. |
| state         | body  	| The status, either: error, failure, pending, or success. |
| context       | body  	| A short header/id. This will be overrittwen if used several times for a commit. |
| description   | body  	| A short description of the status.    |
| target_url    | body  	| A link to the build output on our CI server. Note: only to be used if the web interface is implemented. |

#### Simple python code example

```python
import json
import requests

headers = {
    'Accept': 'application/vnd.github.v3+json'
    'Authorization': 'bearer {TOKEN}'
}
payload = {
    'context': '{context}',
    'state': '{state}',
    'description': '{description}',
    'target_url': '{target_url}'
}

r = requests.post(
    'https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/statuses/9359355448127e17eb8721f67e80adad4c8e96b9', 
    headers = headers, 
    data = json.dumps(payload)
)
print r.status_code
print r.text
```

#### Default response

```json
{
   "url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/statuses/9359355448127e17eb8721f67e80adad4c8e96b9",
   "avatar_url":"https://avatars.githubusercontent.com/u/48830999?v=4",
   "id":12114590580,
   "node_id":"MDEzOlN0YXR1c0NvbnRleHQxMjExNDU5MDU4MA==",
   "state":"error",
   "description":"There was a new error during the build",
   "target_url":"http://www.google.se",
   "context":"test_context",
   "created_at":"2021-02-09T09:59:55Z",
   "updated_at":"2021-02-09T09:59:55Z",
   "creator":{
      "login":"andnil5",
      "id":48830999,
      "node_id":"MDQ6VXNlcjQ4ODMwOTk5",
      "avatar_url":"https://avatars.githubusercontent.com/u/48830999?v=4",
      "gravatar_id":"",
      "url":"https://api.github.com/users/andnil5",
      "html_url":"https://github.com/andnil5",
      "followers_url":"https://api.github.com/users/andnil5/followers",
      "following_url":"https://api.github.com/users/andnil5/following{/other_user}",
      "gists_url":"https://api.github.com/users/andnil5/gists{/gist_id}",
      "starred_url":"https://api.github.com/users/andnil5/starred{/owner}{/repo}",
      "subscriptions_url":"https://api.github.com/users/andnil5/subscriptions",
      "organizations_url":"https://api.github.com/users/andnil5/orgs",
      "repos_url":"https://api.github.com/users/andnil5/repos",
      "events_url":"https://api.github.com/users/andnil5/events{/privacy}",
      "received_events_url":"https://api.github.com/users/andnil5/received_events",
      "type":"User",
      "site_admin":false
   }
}
```

A more detailed description of the response object is given [here](https://www.w3schools.com/python/ref_requests_response.asp).

## GitHub webhooks

### Notification for push requests

This notification is triggered whenever a user pushes to a branch within the repository. The purpose of this notification is to notify the CI server that a push has occurred.

#### Default request header:

```
Host: 3a7dccaf949a.ngrok.io
User-Agent: GitHub-Hookshot/3587fec
Content-Length: 7669
Content-Type: application/json
...
```

#### Default request body:

```json
{
    "ref":"refs/heads/test-hooks",
    "before":"0000000000000000000000000000000000000000",
    "after":"9359355448127e17eb8721f67e80adad4c8e96b9",
    "repository":{
       "id":336516630,
       "node_id":"MDEwOlJlcG9zaXRvcnkzMzY1MTY2MzA=",
       "name":"-dd2480-grp12-assignment2",
       "full_name":"andnil5/-dd2480-grp12-assignment2",
       "private":false,
       "owner":{
          "name":"andnil5",
          "email":"an.nilsson92@gmail.com",
          "login":"andnil5",
          "id":48830999,
          "node_id":"MDQ6VXNlcjQ4ODMwOTk5",
          "avatar_url":"https://avatars.githubusercontent.com/u/48830999?v=4",
          "gravatar_id":"",
          "url":"https://api.github.com/users/andnil5",
          "html_url":"https://github.com/andnil5",
          "followers_url":"https://api.github.com/users/andnil5/followers",
          "following_url":"https://api.github.com/users/andnil5/following{/other_user}",
          "gists_url":"https://api.github.com/users/andnil5/gists{/gist_id}",
          "starred_url":"https://api.github.com/users/andnil5/starred{/owner}{/repo}",
          "subscriptions_url":"https://api.github.com/users/andnil5/subscriptions",
          "organizations_url":"https://api.github.com/users/andnil5/orgs",
          "repos_url":"https://api.github.com/users/andnil5/repos",
          "events_url":"https://api.github.com/users/andnil5/events{/privacy}",
          "received_events_url":"https://api.github.com/users/andnil5/received_events",
          "type":"User",
          "site_admin":false
       },
       "html_url":"https://github.com/andnil5/-dd2480-grp12-assignment2",
       "description":null,
       "fork":false,
       "url":"https://github.com/andnil5/-dd2480-grp12-assignment2",
       "forks_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/forks",
       "keys_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/keys{/key_id}",
       "collaborators_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/collaborators{/collaborator}",
       "teams_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/teams",
       "hooks_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/hooks",
       "issue_events_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/issues/events{/number}",
       "events_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/events",
       "assignees_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/assignees{/user}",
       "branches_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/branches{/branch}",
       "tags_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/tags",
       "blobs_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/git/blobs{/sha}",
       "git_tags_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/git/tags{/sha}",
       "git_refs_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/git/refs{/sha}",
       "trees_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/git/trees{/sha}",
       "statuses_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/statuses/{sha}",
       "languages_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/languages",
       "stargazers_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/stargazers",
       "contributors_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/contributors",
       "subscribers_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/subscribers",
       "subscription_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/subscription",
       "commits_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/commits{/sha}",
       "git_commits_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/git/commits{/sha}",
       "comments_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/comments{/number}",
       "issue_comment_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/issues/comments{/number}",
       "contents_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/contents/{+path}",
       "compare_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/compare/{base}...{head}",
       "merges_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/merges",
       "archive_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/{archive_format}{/ref}",
       "downloads_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/downloads",
       "issues_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/issues{/number}",
       "pulls_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/pulls{/number}",
       "milestones_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/milestones{/number}",
       "notifications_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/notifications{?since,all,participating}",
       "labels_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/labels{/name}",
       "releases_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/releases{/id}",
       "deployments_url":"https://api.github.com/repos/andnil5/-dd2480-grp12-assignment2/deployments",
       "created_at":1612609165,
       "updated_at":"2021-02-08T15:06:28Z",
       "pushed_at":1612798708,
       "git_url":"git://github.com/andnil5/-dd2480-grp12-assignment2.git",
       "ssh_url":"git@github.com:andnil5/-dd2480-grp12-assignment2.git",
       "clone_url":"https://github.com/andnil5/-dd2480-grp12-assignment2.git",
       "svn_url":"https://github.com/andnil5/-dd2480-grp12-assignment2",
       "homepage":null,
       "size":1,
       "stargazers_count":0,
       "watchers_count":0,
       "language":null,
       "has_issues":true,
       "has_projects":true,
       "has_downloads":true,
       "has_wiki":true,
       "has_pages":false,
       "forks_count":0,
       "mirror_url":null,
       "archived":false,
       "disabled":false,
       "open_issues_count":2,
       "license":null,
       "forks":0,
       "open_issues":2,
       "watchers":0,
       "default_branch":"main",
       "stargazers":0,
       "master_branch":"main"
    },
    "pusher":{
       "name":"andnil5",
       "email":"an.nilsson92@gmail.com"
    },
    "sender":{
       "login":"andnil5",
       "id":48830999,
       "node_id":"MDQ6VXNlcjQ4ODMwOTk5",
       "avatar_url":"https://avatars.githubusercontent.com/u/48830999?v=4",
       "gravatar_id":"",
       "url":"https://api.github.com/users/andnil5",
       "html_url":"https://github.com/andnil5",
       "followers_url":"https://api.github.com/users/andnil5/followers",
       "following_url":"https://api.github.com/users/andnil5/following{/other_user}",
       "gists_url":"https://api.github.com/users/andnil5/gists{/gist_id}",
       "starred_url":"https://api.github.com/users/andnil5/starred{/owner}{/repo}",
       "subscriptions_url":"https://api.github.com/users/andnil5/subscriptions",
       "organizations_url":"https://api.github.com/users/andnil5/orgs",
       "repos_url":"https://api.github.com/users/andnil5/repos",
       "events_url":"https://api.github.com/users/andnil5/events{/privacy}",
       "received_events_url":"https://api.github.com/users/andnil5/received_events",
       "type":"User",
       "site_admin":false
    },
    "created":true,
    "deleted":false,
    "forced":false,
    "base_ref":null,
    "compare":"https://github.com/andnil5/-dd2480-grp12-assignment2/commit/935935544812",
    "commits":[
       {
          "id":"9359355448127e17eb8721f67e80adad4c8e96b9",
          "tree_id":"4dabcfd279fa796f0eae46b04bdabc022ec955cd",
          "distinct":true,
          "message":"test: test commit for webhooks",
          "timestamp":"2021-02-08T16:38:09+01:00",
          "url":"https://github.com/andnil5/-dd2480-grp12-assignment2/commit/9359355448127e17eb8721f67e80adad4c8e96b9",
          "author":{
             "name":"andnil5",
             "email":"andnil5@kth.se"
          },
          "committer":{
             "name":"andnil5",
             "email":"andnil5@kth.se"
          },
          "added":[
             "server.py"
          ],
          "removed":[
             
          ],
          "modified":[
             
          ]
       }
    ],
    "head_commit":{
       "id":"9359355448127e17eb8721f67e80adad4c8e96b9",
       "tree_id":"4dabcfd279fa796f0eae46b04bdabc022ec955cd",
       "distinct":true,
       "message":"test: test commit for webhooks",
       "timestamp":"2021-02-08T16:38:09+01:00",
       "url":"https://github.com/andnil5/-dd2480-grp12-assignment2/commit/9359355448127e17eb8721f67e80adad4c8e96b9",
       "author":{
          "name":"andnil5",
          "email":"andnil5@kth.se"
       },
       "committer":{
          "name":"andnil5",
          "email":"andnil5@kth.se"
       },
       "added":[
          "server.py"
       ],
       "removed":[
          
       ],
       "modified":[
          
       ]
    }
 }
 ```