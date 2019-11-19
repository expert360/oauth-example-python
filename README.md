What is this
====================

This is a repo forked from https://github.com/bullhorn/oauth-example-python to demonstrate API requests to Bullhorn as a prototype for the integration with Bullhorn

## What's in the repo

(1) Original implementation of making OAUTH requests: `oauth_example.py`

  Notes
  - OAuth request is made with the username and password included in the request.
  - The redirect_uri is empty, so the response will be a 302
  - The Location header of the redirect response, will contain "code" - this is where the authorization code is retrieved from.

The authorization code will be used to fetch an access_token to be used in subsequent requests

(2) Example API requests in `rest-requests.py`

This contains API calls to

- OAuth request from step 1.
- Login to get the access_token
- Fetch candidate details
- Delete and add event subscription
- Fetch updates from an event subscription

See `notes.txt` for an example of the output of the `rest-requests.py` script

## How to run the script

To run just OAuth requests:

```
python oauth_example.py
```

To run OAuth + REST API requests
```
python rest-requests.py
```
