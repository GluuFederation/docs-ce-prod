### Setup Prompt

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

The `setup.py` script will bring up a prompt to provide information for certificate as well as the IP Address and the hostname for the Gluu Server. The prompt is given below.

```
Enter IP Address [192.168.122.60] :
Enter hostname [localhost] : centos.gluu.info
Enter your city or locality : Austin
Enter your state or province two letter code : TX
Enter two letter Country Code : US
Enter Organization Name : Gluu
Enter email address for support at your organization : support@gluu.org
Enter maximum RAM for tomcat in MB [3072] :
Optional: enter password for oxTrust and LDAP superuser [hlE3vzf0hMdD] :
Install oxAuth OAuth2 Authorization Server? [Yes] :
Install oxTrust Admin UI? [Yes] :
Install LDAP Server? [Yes] :
Install Apache HTTPD Server [Yes] :
Install Shibboleth SAML IDP? [Yes] :
Install Asimba SAML Proxy? [Yes] :
Install CAS? [Yes] :
Install oxAuth RP? [Yes] :
Install Passport? [Yes]
```
!!! Login
    Please log in using the username `admin` and the password from the setup script promtpt e.g `hlE3vzf0hMdD` or the password entered

If a resolvable DNS host is not used, then it must be added to the hostname of the Operating System  hosts file on the server running the browser.

!!! warning
    Please remove or encrypt the setup.properties.last file as it contains the clear text passwords for *LDAP, admin user, keystores, and 3DES salt*.

The errors can be found the the `setup_errors.log` file and a detailed step by step installation is found in the `setup.log` file under the `/install/community-edition-setup` folder.

!!! warning
    Use a FQDN (fully qualified domain name) as hostname and refrain from using 127.0.0.1 as IP address or usage of private IP is not supported and not recommended.

### Script Command Line Options
The `setup.py` script can be used to configure your Gluu Server and to add initial data
for oxAuth and oxTrust to start. If `setup.properties` is found
in this folder, these properties will automatically be used instead of
the interactive setup.

The administrator can use the following command line options to include additional components:

* __-a__ install Asimba
* __-c__ install CAS
* __-d__ specify the directory where community-edition-setup is located. Defaults to '.'
* __-f__ specify `setup.properties` file
* __-h__ invoke this help
* __-l__ install LDAP
* __-n__ no interactive prompt before install starts. Run with `-f`
* __-N__ no Apache httpd server
* __-s__ install the Shibboleth IDP
* __-u__ update hosts file with IP address/hostname
* __-w__ get the development head war files

Example Command: `# ./setup.py -cas` This command will install Gluu Server with CAS, Asimba and Shibboleth IDP.
