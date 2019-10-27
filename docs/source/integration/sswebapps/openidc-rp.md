# mod_auth_openidc RP Integration

## Basic Web Server Installation

Before you can install mod_auth_openidc, you need to have an Apache HTTPD server running with SSL enabled. 

### Apache Web Server

It is assumed that all the hostnames will be DNS resolvable. If not, then add the entries in `/etc/hosts` file on both the web server and Gluu Server. 

If you don't have the Apache HTTPD server installed, use apt-get to install the Ubuntu standard distribution, then [start](../../operation/services.md#start) the `apache2` service.

### SSL Configuration
The SSL Module is necessary for the Apache OpenID Connect Module. Please use the following commands to activate the `ssl module`.

```
a2enmod ssl
```

The next step is to create a self-signed SSL Certificate.

* Create a directory to put the generate the ssl certificate

``` text
mkdir /etc/apache2/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt
```

* Answer the questions that are asked. A template is given below

```
	Country Name (2 letter code) [AU]:US
	State or Province Name (full name) [Some-State]:TX
	Organization Name (eg, company) [Internet Widgits Pty Ltd]:Acme Inc.
	Organizational Unit Name (eg, section) []:
	Common Name (e.g. server FQDN or YOUR name) []:www.mydomain.com
	Email Address []:help@mydomain.com
```

#### Configure Apache to use SSL
This section will guide you through the steps to configure apache to use the SSL module

1. Open the `default-ssl.conf` file

    ```
    vim /etc/apache2/sites-available/default-ssl.conf
    ```

1. Update the certificate locations with the newly created certificates `/etc/apache2/ssl/apache.key` and `/etc/apache2/ssl/apache.crt`

1. Activate the SSL Virtual Host and CGI

    ```
    a2ensite default-ssl.conf
    a2enmod cgid
    ```

1. [Restart](../../operation/services.md#restart) the `apache2` service

At this point, its a good time to test to make sure SSL and CGI are working. Point your browser at https://www.mydomain.com/cgi-bin/printHeaders.cgi You should see a list of current environment variables. 

## Configuration of mod_auth_openidc 

### Installation

`mod_auth_openidc` module depends on the Ubuntu packages `libjansson`, `libhiredis`, and `libcurl`: 

For Ubuntu 16.04

```
apt-get install libjansson4 libhiredis0.13
```
```
apt-get install libcurl3
```

You'll also need the mod_auth_openidc and libjose packages which can be downloaded from the [Releases Page](https://github.com/zmartzone/mod_auth_openidc/releases).

For example, at this time the current release for mod_auth_openidc is 2.3.3 and for libjose is 2.3.0, so the command would be:

For Ubuntu 16.04

``` 
wget https://github.com/zmartzone/mod_auth_openidc/releases/download/v2.3.0/libcjose0_0.5.1-1.xenial.1_amd64.deb
```
```
wget https://github.com/zmartzone/mod_auth_openidc/releases/download/v2.3.8/libapache2-mod-auth-openidc_2.3.8-1.xenial+1_amd64.deb
```
```
dpkg -i libcjose0_0.5.1-1.xenial.1_amd64.deb
```
```
dpkg -i libapache2-mod-auth-openidc_2.3.8-1.xenial+1_amd64.deb
```


!!! Note
    Get the latest packages here: https://github.com/zmartzone/mod_auth_openidc/releases

Note, if you like to build from source, you can clone the project at [Github Page](https://github.com/zmartzone/mod_auth_openidc)

Now you can enable the module

``` text
sudo a2enmod auth_openidc
```

Then, [restart](../../operation/services.md#restart) the `apache2` service

### Client Registration

There are two methods for client registration:

1. Dynamic Client Registration
2. Manual Client Registration

For this example, let's create the client manually in the Gluu Server. When you add the client, use the following parameters:

``` text
Name: mod_auth_openidc
Client Secret: something-sufficiently-unguessable
Application Type: Web
Pre-Authorization: True
Redirect Login URIs: https://www.mydomain.com/callback
Subject Type: Public
Scopes: openid, profile, email
Response Types: code
Grant Types: authorization_code

```

Make a note of the `client_secret` (you won't get to see it again)! You'll also need the `client_id` for the next step.

### Install CGI script

This cgi-script makes for a good test page! 

``` text
vi /usr/lib/cgi-bin/printHeaders.cgi

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
chown www-data:www-data /usr/lib/cgi-bin/printHeaders.cgi
```
```text
chmod ug+x /usr/lib/cgi-bin/printHeaders.cgi

```

### Configuring the Apache VirtualHost 

You are almost done! You'll need to configure mod_auth_openidc to protect your server.

``` text
vi /etc/apache2/sites-available/default-ssl.conf

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

Then [restart](../../operation/services.md#restart) the `apache2` service

The most confusing part here is the `OIDCRedirectURI`--don't set this to a path used by your server. The apache-filter uses the redirect_uri to process the response from the OpenID Provider (Gluu Server). 

Now you're ready to test. Open your web browser, and point it at `https://www.mydomain.com/cgi-bin/printHeaders.cgi` 

If you're not logged in already, you should be redirected to the authentication page. If you are logged in, you should just see an HTML page with the `REMOTE_USER` variable populated. Also check out the `OIDC_id_token_payload` and all the claims for `USERINFO_` 

## Installation

We assume that all the hostnames will be dns resolvable. If not, then add the according entries in `/etc/hosts`, please.

### Add EPEL Repository

Run the following command to __Add EPEL Repo__.

* `rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm`

### Apache Web Server

To set up __Apache2 SSL__, run the following commands:

!!! Note
    If the hiredis package is not found by the `yum` command, please download it manually from [this page](https://centos.pkgs.org/6/puias-unsupported-x86_64/hiredis-0.12.1-1.sdl6.x86_64.rpm.html) and install it.

```
yum install httpd mod_ssl
```
```
yum install curl hiredis jansson
```

### Configure SSL Module
This section will guide you to create SSL certificates. Use the following commands to crete a  directory and generate the certificates.

```
mkdir /etc/httpd/ssl
```
```
openssl req -new -x509 -sha256 -days 365 -nodes -out /etc/httpd/ssl/httpd.pem -keyout /etc/httpd/ssl/httpd.key
```

You will be prompted to enter some values such as company name, country etc. Please enter them and your certificate will be ready. A template is given below

```text
	Country Name (2 letter code) [XX]:US
	State or Province Name (full name) []:TX
	Locality Name (eg, city) [Default City]:Austin
	Organization Name (eg, company) [Default Company Ltd]:Gluu
	Organizational Unit Name (eg, section) []:
	Common Name (eg, your name or your server's hostname) []:modauth-centos.info
	Email Address []:support@gluu.org
```

The next step is to configure Apache to use the certificates and use the following command to edit the `ssl.conf` file. 
```
vi /etc/httpd/conf.d/ssl.conf
```

The important part of the configuration is to enter the path to the created SSL certificates. The example is given below.  

!!! Note
    Please make sure to use the correct server name in the configuration file.

```
    SSLCertificateFile /etc/httpd/ssl/httpd.pem
    SSLCertificateKeyFile /etc/httpd/ssl/httpd.key
    ServerAdmin support@gluu.org
    ServerName gluu.org
```

[Restart](../../operation/services.md#restart) the `httpd` service.

### Authentication Module (mod_auth_openidc)

!!! Note
    The latest version of the apache OpenID Connect module is available from [this page](https://github.com/zmartzone/mod_auth_openidc/releases)

The latest package for the Apache module might have multiple dependencies which must be installed first.

Run the following command to install the `mod_auth_openidc` module:

```
rpm -ivhhttps://github.com/zmartzone/mod_auth_openidc/releases/download/v2.3.8/mod_auth_openidc-2.3.8-1.el6.x86_64.rpm
```

!!! Note
    If there are any difficulties installing `hiredis` and `jansson`,
try to update the package database of your system using the command below.

```
yum upgrade
```

#### Load Authentication Module 
Please make sure that the following shared-object file exists by running the following command:

```
ls -l /usr/lib64/httpd/modules/mod_auth_openidc.so
```
## Install CGI Script
The test page is made using the cgi-script. Please use the following command to create the script.

```
vi /var/www/cgi-bin/printHeaders.cgi
```

Please paste the following code to prepare the script

```python
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

The next step is to make the script executable by HTTPD

```text
chown apache:apache /var/www/cgi-bin/printHeaders.cgi
```
```
chmod ug+x /var/www/cgi-bin/printHeaders.cgi
```

### Client Registration

There are two methods for client registration:

1. Dynamic Client Registration
2. Manual Client Registration

You can use any of the methods to register the client. For this example, let's create the client manually in the Gluu Server. Please use the following parameters to create the client:

```text
Name: mod_auth_openidc
Client Secret: something-sufficiently-unguessable
Application Type: Web
Pre-Authorization: Enabled
login uri: https://www.mydomain.com/callback
Subject Type: Public
Scopes: openid, profile, email
Response Types: code
```

!!! Note
    The `client_secret` should be noted after creating the client in Gluu Server as it is used later.
    
### Configure the Apache Virtualhost
The Apache module is confgured in the defautl ssl configuration file. Please use the command below to open the file

```text
vi /etc/httpd/conf.d/ssl.conf 
```

Please add the following at the bottom of the file

```text
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

!!! Warning
    Please remember to populate the `OIDCRedirectURI` with a value that is not used by the server. The apache-filter uses the redirect_uri to process the response from the OpenID Provider (Gluu Server).

[Restart](../../operation/services.md#restart) the `httpd` service for the changes to take effect

Now you're ready to test. Open your web browser, and point it at https://www.mydomain.com/cgi-bin/printHeaders.cgi

