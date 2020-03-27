# trello-cli

Command line helper for Trello allowing listing of Active Boards, Lanes and Cards available to a given user
Using this tool requires the user to have a Trello Account.

# Trello API Authentication

This helper uses Trello API to access Trello Data and requires the user to get a token online
See https://trello.com/app-key/

Once you retrieve your API key and your token, they should be stored in your $HOME folder 
into a json file .trello.creds

`{`
`   "api_key": <api_key>,`
`   "token": <token>`
`}`

The tool will look for credentials by default in your home folder, however it is possible to overwrite this with the `-c` parameter and specify your own json file.
