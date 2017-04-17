# setup.py Command Line Options

Use `setup.py` to configure Gluu Server and to add initial data
required for oxAuth and oxTrust to start. If `setup.properties` is found
in this folder, these properties will automatically be used instead of
the interactive setup.

The following options are available:

|Option | Function |
|:------:|---------|
| __-a__ | install Asimba |
| __-c__ | install CAS |
| __-d__ |specify the directory where community-edition-setup is located. Defaults to '.'|
| __-f__ | specify `setup.properties` file|
| __-h__  | invoke this help|
| __-l__ | install LDAP |
| __-n__ | no interactive prompt before install starts. Run with `-f`|
| __-N__ | no Apache httpd server|
| __-s__ | install the Shibboleth IDP|
| __-u__ | update hosts file with IP address/hostname|
| __-w__ | get the development head war files|

