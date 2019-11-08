# Session and Custom parameters and claims in `password` grant flow 

## Overview

This tutorial offers a step-by-step guide for setting up a basic proof-of-concept environment showcasing an creation SSO cookie in `password` grant flow. Refer to general documentation describing each component for more details.

## Testing

1. Install CE 4.0.1
2. Log into oxTrust admin GUI
3. Enable `resource_owner_password_credentials_custom_params_example` Resource Owner Password Credentials script
4. Enable `introspection_custom_params` 	Introspection script
5. Register OpenId client for RO flow with next parameters:
   - Grant Types = `password`
   - Authentication method for the Token Endpoint = `client_secret_post` 
6. Prepare and run demo  RP
   - Put into CE `/usr/lib/cgi-bin` folder file `rp.py` with next content:

```
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
import ssl
import httplib, urllib, urllib2
import json
import sys
import io
import codecs

# Enable detail logging
cgitb.enable()

# Configuration
op_server_uri = "https://<server>"
op_client_id = "<client_id>"
op_client_secret = "<client_secret>"

user_name = "<user_name>"
pwd = "<user_pwd>"

session_id_cookie_domain = ".<domain>"

# Outut should be utf-8
#def enc_print(string='', encoding='utf8'):
#    sys.stdout.buffer.write(string.encode(encoding) + b'\n')

# Prepare SSL trust all context
context = ssl._create_unverified_context()

# Get access_token
token_post_params_json = { 'client_id': op_client_id, 'client_secret': op_client_secret,
    'username': user_name, 'password': pwd, 'grant_type': 'password',
    'custom1': 'custom_value_1', 'custom2': 'custom_value_2' }
post_token_params_url_encoded = urllib.urlencode(token_post_params_json)
token_headers_json = { 'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json' }
token_endpoint_uri = '%s/oxauth/restv1/token' % op_server_uri

token_req = urllib2.Request(token_endpoint_uri, post_token_params_url_encoded, token_headers_json)
try:
    token_resp = urllib2.urlopen(token_req, context=context)
except Exception as e:
    print("Content-Type: text/html\n")

    print("<title>RP script output</title>")
    print("Failed to get access_token!")
    exit()

token_resp_data = token_resp.read()
token_resp_json = json.loads(token_resp_data)

access_token = token_resp_json['access_token']

# Request introspection
introspection_post_params_json = { 'token': access_token }
post_introspection_params_url_encoded = urllib.urlencode(introspection_post_params_json)
introspection_headers_json = { 'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'Authorization': 'Bearer %s' % access_token }
introspection_endpoint_uri = '%s/oxauth/restv1/introspection' % op_server_uri

introspection_req = urllib2.Request(introspection_endpoint_uri, post_introspection_params_url_encoded, introspection_headers_json)
try:
    introspection_resp = urllib2.urlopen(introspection_req, context=context)
except Exception as e:
    print("Content-Type: text/html\n")

    print("<title>RP script output</title>")
    print("Failed to get introspection data!")
    exit()

introspection_resp_data = introspection_resp.read()
introspection_resp_json = json.loads(introspection_resp_data)

session_id = introspection_resp_json['session_id']

print("Content-Type: text/html")
#print("Set-Cookie: session_id=%s; Path=/; Secure; HttpOnly; Expires=Fri, 08 Nov 2030 18:52:39 +0000; HttpOnly" % session_id)
print("Set-Cookie: session_id=%s; domain=%s; Path=/; Secure; HttpOnly; Expires=Fri, 08 Nov 2030 18:52:39 +0000; HttpOnly" % (session_id, session_id_cookie_domain))
print("\n")

print("<title>RP script output</title>")
print("<h1>RP 'password' grant sample application</h1>")

print("<p>Token Response Data:</p>")
print("<pre>" + token_resp_data + "</pre>")

print("<p>Introspection Response Data:</p>")
print("<pre>" + introspection_resp_data + "</pre>")
```

   - Update next parameters in file above:
     `op_server_uri`, `op_client_id`, `op_client_secret` 
     `user_name`, `pwd`
     `session_id_cookie_domain`
   - Set executable permission to this file
   - Open in browser `https://<server>/cgi-bin/rp.py`
   - As result this demo pge should produce page with `token` and `introspection responses`. Also it should set `session_id` cookie      

   8. Open in browser `https://<server>` to log into oxTrust. oxAuth should accept cookie which `rp.py` set and allow log into application without entering credentials.
   
## Note
   1. In order to full support this flow we need to resolve issue: https://github.com/GluuFederation/oxAuth/issues/1196
      Without this issue resolution after logout from oxTrust user not able to logging until he restart browser.
      
   
   