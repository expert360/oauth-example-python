What is this
====================

This is a repo forked from https://github.com/bullhorn/oauth-example-python to demonstrate API requests to Bullhorn as a prototype for the integration with Bullhorn

Docs: http://bullhorn.github.io/Getting-Started-with-REST/ for the flow of OAuth and Logging in with Bullhorn

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

## Creating a new event:

Events are unique, so you cannot create an event with the same name.
Note, if you delete events, this may not guarantee updates are returned for that event that was re-created.

http://bullhorn.github.io/rest-api-docs/index.html#put-event-subscription

```
curl -XPUT -v "https://rest60.bullhornstaffing.com/rest-services/64pqp0/event/subscription/event12345?type=entity&names=Candidate&eventTypes=INSERTED,UPDATED,DELETED" -H 'BhRestToken: 72e59adb-38d4-4d45-89db-2af8b141f34f'

curl -XPUT -v "https://rest60.bullhornstaffing.com/rest-services/64pqp0/event/subscription/candidate_event?type=entity&names=Candidate&eventTypes=INSERTED,UPDATED,DELETED" -H 'BhRestToken: 72e59adb-38d4-4d45-89db-2af8b141f34f'
```

Getting events

```
curl -v "https://rest60.bullhornstaffing.com/rest-services/64pqp0/event/subscription/event12345?maxEvents=10" -H 'BhRestToken: 72e59adb-38d4-4d45-89db-2af8b141f34f'
```

```
curl -v "https://rest60.bullhornstaffing.com/rest-services/64pqp0/event/subscription/event12345?maxEvents=10&requestId=2" -H 'BhRestToken: 72e59adb-38d4-4d45-89db-2af8b141f34f'
```

request:

```
curl -v "https://rest60.bullhornstaffing.com/rest-services/64pqp0/event/subscription/candidate_events?maxEvents=1&requestId=1" -H "BhRestToken: 4231a86f-1cdb-4665-bbce-8ac43be9f5e4"
```

response:
```
{"requestId":1,"events":[{"eventId":"ID:JBM-40000002","eventType":"ENTITY","eventTimestamp":1574142912400,"eventMetadata":{"CHANGE_HISTORY_ID":"11","TRANSACTION_ID":"1c7b7d44-eb12-4c95-9d59-66dca7a3bced","PERSON_ID":"3"},"entityName":"Candidate","entityId":6,"entityEventType":"UPDATED","updatedProperties":["email"]}]}
```

Events:
* Fetch most recent changes - dont pass in requestId (new request Id gets generated)
* Fetch from a particular request - pass in requestId

## Expired token

```
{"errorMessage":"Bad 'BhRestToken' or timed-out.","errorMessageKey":"errors.authentication.invalidRestToken","errorCode":401}
```

