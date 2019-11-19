import urllib, urllib2, urlparse, json

# This sample shows how to obtain a Bullhorn OAuth access token
# without the user/browser flow.  This style of OAuth authentication
# can be used when building scheduled jobs or other code that needs
# to log in without user intervention.

# Change the values for the following global variables to test out
# this code.  Code can then be run directly, e.g.:
# [user@host]: python oauth_example.py
#
# See: http://bullhorn.github.io/Getting-Started-with-REST/

# Bullhorn OAuth client ID
client_id = "..."
# Bullhorn OAuth secret
client_secret = '...'
# Bullhorn OAuth service endpoint.  Don't forget to change
# host to auth9 if using a sandbox environment
base_url = 'https://auth.bullhornstaffing.com/oauth'
# put login credentials here
username = "..."
password = "..."


class AuthCodeRedirectHandler(urllib2.HTTPRedirectHandler):
    """
    A bare bones redirect handler that pulls the auth code sent back
    by OAuth off the query string of the redirect URI given in the
    Location header.  Does no checking for other errors or bad/missing
    information.
    """
    def http_error_302(self, req, fp, code, msg, headers):
        """handler for 302 responses that assumes a properly constructed
        OAuth 302 response and pulls the auth code out of the header"""
        qs = urlparse.urlparse(headers["Location"]).query
        print(qs)
        auth_code = urlparse.parse_qs(qs)['code'][0]
        return auth_code

class CustomRequest(urllib2.Request):
    '''class to handling putting with urllib2'''

    def __init__(self, *args, **kwargs):
        # return urllib2.Request.__init__(self, *args, **kwargs)
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib2.Request.get_method(self, *args, **kwargs)

def build_auth_code_request(username, password):
    auth_data = urllib.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "username": username,
        "password": password,
        "action": "Login"
    })
  
    req = urllib2.Request(url=base_url + "/authorize", data=auth_data)
    return req


def get_access_token(code):
    """
    Gets an OAuth access token given an OAuth authorization code
    """
    access_token_params = urllib.urlencode({
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    })
    
    req = urllib2.Request(base_url + '/token', access_token_params)
    print(req.get_full_url())
    print("params: " + access_token_params)
    f = urllib2.urlopen(req)
    return f.read()

if __name__ == "__main__":
    req = build_auth_code_request(username, password)
    print("\nStep 1. POST: Get authenticated via OUATH (using credentials, username and password): ")
    print(req.get_full_url())
    print("request payload: " + req.get_data())
    opener = urllib2.build_opener(AuthCodeRedirectHandler)

    # get code returned in redirect location header when make a request to /authorize
    print("\nStep 2. Look at headers in the response for the 'code' which is the authorization code")
    auth_code = opener.open(req) 
    print('auth code in headers: ' + auth_code)

    print("\nStep 3. POST: Get the access_token using the authorization 'code' returned")
    access_token = get_access_token(auth_code)
    print("response: " + access_token)

    access_token_json = json.loads(access_token)
    print('access_token: ' + access_token_json['access_token'])

    # login request to get the BhRestToken and restUrl
    login_data = urllib.urlencode({
        "version": "2.0",
        "access_token": access_token_json['access_token']
    })

    req = urllib2.Request(url=api_url + "/login", data=login_data)
    print("\nStep 4. GET: Login using the access_token to get BhRestToken and restUrl for subsequent requests:")
    print(req.get_full_url())
    f = urllib2.urlopen(req)
    resp = f.read()
    print("resonse: " + resp)

    # get BhRestToken and restUrl
    login_resp_json = json.loads(resp)
    bhRestToken = login_resp_json['BhRestToken']
    restUrl = login_resp_json['restUrl']

    print("\nStep 5. GET: Make a request - fetch candidate 5 details")
    # get a candidate
    # https://rest.bullhornstaffing.com/rest-services/{corpToken}/entity/Candidate/{id}?BhRestToken={session_key}&fields=firstName,lastName,address
    candidate_data = urllib.urlencode({
        "BhRestToken": bhRestToken,
        "fields": "firstName,lastName"
    })
    candidate_id = "5"
    # print(candidate_data) #url encoded params
    req = urllib2.Request(restUrl + "entity/Candidate/" + candidate_id + "?" + candidate_data)
    print(req.get_full_url())
    f = urllib2.urlopen(req)
    resp = f.read()
    print("Response:" + resp)

    # This is generally not needed, but deleting old events for testing and demonstration only
    # print("\nStep 6. DELETE: Delete a Subscription to an event")
    # req = CustomRequest(url=restUrl + "event/subscription/candidate_events?BhRestToken=" + bhRestToken, method='DELETE')
    # req.get_method = lambda: 'DELETE'
    # print("URL: " + req.get_full_url())
    # print("Method:" + req.get_method())
    # f = urllib2.urlopen(req)
    # resp = f.read()
    # print("Response:" + resp)

    # subscribe to events - note: once an event exists you cannot create it again
    # e.g. https://rest.bullhorn.com/e999/event/subscription/Abcde?type=entity&names=Candidate&eventTypes=INSERTED,UPDATED,DELETED
    # print("\nStep 7. PUT: Subscribe to Candidate Events")
    # req = CustomRequest(url=restUrl + "event/subscription/candidate_events?BhRestToken=" + bhRestToken + "&type=entity&names=Candidate&eventTypes=INSERTED,UPDATED,DELETED", method='PUT')
    # print("URL: " + req.get_full_url())
    # print("Method:" + req.get_method())
    # f = urllib2.urlopen(req)
    # resp = f.read()
    # print("Response:" + resp)

    # get the last request id - to use when fetching from the last event request
    # subscribe_event_resp = json.loads(resp)
    # last_request_id = subscribe_event_resp['lastRequestId']
    # print("lastRequestId: " + str(last_request_id))

    # Get event subscription
    last_request_id = 1 #Note: request id = 0 does not return results
    print("\nStep 8. GET: Candidate Events")
    headers = {'BhRestToken': bhRestToken}
    req = urllib2.Request(restUrl + "event/subscription/candidate_events?BhRestToken=" + bhRestToken + "&maxEvents=100&requestId=" + str(last_request_id))
    print("URL: " + req.get_full_url())
    f = urllib2.urlopen(req)
    print("response status: " + str(f.getcode()))
    resp = f.read()
    print("Response:" + resp)

    # TODO: refresh token flow - ideally store the token in cache until expiry time and then refetch using the refresh token


