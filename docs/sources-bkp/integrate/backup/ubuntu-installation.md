# Basic Web Server Installation

Before you can install mod_auth_openidc, you need to have an Apache
HTTPD server running with SSL enabled. 

## Apache Web Server

It is assumed that all the hostnames will be dns resolvable. If not, 
then add the entries in `/etc/hosts` file on both the web server
and Gluu Server. 

If you don't have the Apache HTTPD server installed, use apt-get
to install the Ubuntu standard distribution:

``` text
# apt-get install apache2
# service apache2 start
```

## SSL Configuration
The SSL Module is necessary for the Apache OpenID Connect Module. Please 
use the following commands to activate the `ssl module`.

``` text
# a2enmod ssl
```

The next step is to create a self-signed SSL Certificate.

* Create a directory to put the generate the ssl certificate

``` text
# mkdir /etc/apache2/ssl`
# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt
```

* Answer the questions that are asked. A template is given below

``` text
	Country Name (2 letter code) [AU]:US
	State or Province Name (full name) [Some-State]:TX
	Organization Name (eg, company) [Internet Widgits Pty Ltd]:Acme Inc.
	Organizational Unit Name (eg, section) []:
	Common Name (e.g. server FQDN or YOUR name) []:www.mydomain.com
	Email Address []:help@mydomain.com
```

### Configure Apache to use SSL
This section will guide you through the steps to configure apache to 
use the SSL module

1. Open the `default-ssl.conf` file

``` text
# vim /etc/apache2/sites-available/default-ssl.conf`

```

2. Update the certificate locations with the newly created certificates 
`/etc/apache2/ssl/apache.key` and `/etc/apache2/ssl/apache.crt`

3. Activate the SSL Virtual Host and CGI

``` text
# a2ensite default-ssl.conf
# a2enmod cgid
# service apache2 restart

```

At this point, its a good time to test to make sure SSL and CGI are 
working. Point your browser at 
https://www.mydomain.com/cgi-bin/printHeaders.cgi
You should see a list of current environment variables. 

## Configuration of mod_auth_openidc 

### Installation

`mod_auth_openidc` module depends on the Ubuntu package `libjansson4`: 

``` text
# apt-get install libjansson

```

You'll also need the mod_auth_openidc and libjose packages which can 
be downloaded from the [Releases Page](https://github.com/pingidentity/mod_auth_openidc/releases).

For example, at this time the current release is 2.1.3, so the command would be:

``` text
# wget https://github.com/pingidentity/mod_auth_openidc/releases/download/v2.1.3/libcjose_0.4.1-1ubuntu1.trusty.1_amd64.deb
# wget https://github.com/pingidentity/mod_auth_openidc/releases/download/v2.1.3/libapache2-mod-auth-openidc_2.1.3-1ubuntu1.trusty.1_amd64.deb
# dpkg -i libcjose_0.4.1-1ubuntu1.trusty.1_amd64.deb
# dpkg -i libapache2-mod-auth-openidc_2.1.3-1ubuntu1.trusty.1_amd64.deb

```

!!! Note
    Get the latest packages here: https://github.com/pingidentity/mod_auth_openidc/releases

Note, if you like to build from source, you can clone the project at [Github Page](https://github.com/pingidentity/mod_auth_openidc)

Now you can enable the module

``` text
# sudo a2enmod auth_openidc
# sudo service apache2 restart

```

## Client Registration

There are two methods for client registration:

1. Dynamic Client Registration
2. Manual Client Registration

For this example, let's create the client manually in the Gluu Server.
When you add the client, use the following parameters:

``` text
Name: mod_auth_openidc
Client Secret: something-sufficiently-unguessable
Application Type: Web
Pre-Authorization: Enabled
login uri: https://www.mydomain.com/callback
Subject Type: Public
Scopes: openid, profile, email
Response Types: code

```

Make a note of the `client_secret` (you won't get to see it again)! You'll
also need the `client_id` for the next step.

## Install CGI script

This cgi-script makes for a good test page! 

``` text
# vi /usr/lib/cgi-bin/printHeaders.cgi

```

Then paste in this code

``` python
#!/usr/bin/python

import os

d = os.environ
k = d.keys()
k.sort()

print "Content-type: text/html\n\n"

print "<HTML><Head><TITLE>Print Env Variables</TITLE></Head><BODY>"
print "<h1>Environment Variables</H1>"
for item in k:
    print "<p><B>%s</B>: %s </p>" % (item, d[item])
print "</BODY></HTML>"

```

Then you'll need to make the script executable by the Apache2

``` text
# chown www-data:www-data /usr/lib/cgi-bin/printHeaders.cgi
# chmod ug+x /usr/lib/cgi-bin/printHeaders.cgi

```

## Configuring the Apache VirtualHost 

You are almost done! You'll need to configure mod_auth_openidc to
protect your server.

``` text
# vi /etc/apache2/sites-available/default-ssl.conf

```

Add the following right under `<VirtualHost _default_:443>`

``` apacheconf
OIDCProviderMetadataURL https://idp.mydomain.com/.well-known/openid-configuration
OIDCClientID (client-id-you-got-back-when-you-added-the-client)
OIDCClientSecret (your-client-secret)
OIDCRedirectURI https://www.mydomain.com/callback
OIDCResponseType code
OIDCScope "openid profile email"
OIDCSSLValidateServer Off
OIDCCryptoPassphrase (a-random-seed-value)
OIDCPassClaimsAs environment
OIDCClaimPrefix USERINFO_
OIDCPassIDTokenAs payload
<Location "/">
    Require valid-user
    AuthType openid-connect
</Location>

```

Then restart Apache to effect the changes

``` text
# service apache2 restart

```

The most confusing part here is the `OIDCRedirectURI`--don't set this
to a path used by your server. The apache-filter uses the redirect_uri 
to process the response from the OpenID Provider (Gluu Server). 

Now you're ready to test. Open your web browser, and point it at 
`https://www.mydomain.com/cgi-bin/printHeaders.cgi` 

If you're not logged in already, you should be redirected to 
the authentication page. If you are logged in, you should just see
an html page with the `REMOTE_USER` variable populated. Also
check out the `OIDC_id_token_payload` and all the claims for 
`USERINFO_` 
