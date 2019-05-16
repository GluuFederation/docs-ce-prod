# Installation

We assume that all the hostnames will be dns resolvable. If not, then
add the according entries in `/etc/hosts`, please.

### Add EPEL Repository

Run the following command to __Add EPEL Repo__.

* `# rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm`

## Apache Web Server
To setup __Apache2 SSL__, run the following commands:

!!! Note
    If the hiredis package is not found by the `yum` command, please download it manually from [this page](https://centos.pkgs.org/6/puias-unsupported-x86_64/hiredis-0.12.1-1.sdl6.x86_64.rpm.html) and install it.

```
# yum install httpd mod_ssl
# yum install curl hiredis jansson
```

## Configure SSL Module
This section will guide you to create SSL certificates.
Use the following commands to crete a  directory and generate the certificates.

```
# mkdir /etc/httpd/ssl
# openssl req -new -x509 -sha256 -days 365 -nodes -out /etc/httpd/ssl/httpd.pem -keyout /etc/httpd/ssl/httpd.key
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
# vi /etc/httpd/conf.d/ssl.conf
```

The important part of the configuration is to enter the path to the created SSL certificates. The example is given below.<br/>
**Note:** Please make sure to use the correct server name in the configuration file.

```
    SSLCertificateFile /etc/httpd/ssl/httpd.pem
    SSLCertificateKeyFile /etc/httpd/ssl/httpd.key
    ServerAdmin support@gluu.org
    ServerName gluu.org
```

Restart Apache Server and you are done configuring the SSL Module. Use the command below to restart the Apache Server.

```
# service httpd restart
```

## Authentication Module (mod_auth_openidc)
!!! Note
    The latest version of the apache OpenID Connect module is available from [this page](https://github.com/pingidentity/mod_auth_openidc/releases)

The latest package for the apache module might have multiple dependencies which must be installed first.


Run the following command to install the `mod_auth_openidc` module:

```
rpm -ivh https://github.com/pingidentity/mod_auth_openidc/releases/download/v1.8.2/mod_auth_openidc-1.8.2-1.el6.x86_64.rpm
```

!!! Note
    If there are any difficulties installing `hiredis` and `jansson`,
try to update the package database of your system using the command below.

```
# yum upgrade
```
### Load Authentication Module 
Please make sure that the following shared-object file exists by running the following command:

```
ls -l /usr/lib64/httpd/modules/mod_auth_openidc.so
```
## Install CGI Script
The test page is made using the cgi-script. Please use the following command to create the script.

```
# vi /var/www/cgi-bin/printHeaders.cgi
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
# chown apache:apache /var/www/cgi-bin/printHeaders.cgi
# chmod ug+x /var/www/cgi-bin/printHeaders.cgi
```

## Client Registration

There are two methods for client registration:

1. Dynamic Client Registration
2. Manual Client Registration

You can use any of the methods to register the client.
For this example, let's create the client manually in the Gluu Server.
Please use the following parameters to create the client:

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
## Configure the Apache Virtualhost
The apache module is confgured in the defautl ssl configuration file. Please use the command below to open the file

```text
# vi /etc/httpd/conf.d/ssl.conf 
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

Please restart the HTTPD server for the changes to take effect

```text
# service httpd restart
```

Now you're ready to test. Open your web browser, and point it at
https://www.mydomain.com/cgi-bin/printHeaders.cgi`