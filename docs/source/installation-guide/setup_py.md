### Setup Prompt
The `setup.py` script will bring up a prompt to provide information for 
certificate as well as the IP Address and the hostname for the Gluu Server. 
The prompt with example values is provided below.

```
Do you acknowledge that use of the Gluu Server is under the MIT license? [N|y] : y
Enter IP Address [192.168.122.60] :
Enter hostname [localhost] : e.g. idp.mydomain.info
Enter your city or locality : 
Enter your state or province two letter code : 
Enter two letter Country Code : 
Enter Organization Name : MyOrg
Enter email address for support at your organization : e.g. support@mydomain.com
Enter maximum RAM for applications in MB [3072] :
Optional: enter password for oxTrust and LDAP superuser [hlE3vzf0hMdD] :
Install oxAuth OAuth2 Authorization Server? [Yes] : 
Install oxTrust Admin UI? [Yes] : 
Install Backend DB Server? [Yes] : 
Install Apache HTTPD Server [Yes] : 
Install Shibboleth SAML IDP? [No] : 
Install oxAuth RP? [No] : 
Install Passport? [No] : 
Install Gluu Radius? [No] : 
```
!!! Login
    Please log in using the username `admin` and the password from the setup script prompt e.g `hlE3vzf0hMdD` or the password entered

If a resolvable DNS host is not used, then it must be added to the hostname of the Operating System hosts file on the server running the browser.

!!! warning
    Please remove or encrypt the setup.properties.last file as it contains the clear text passwords for *LDAP, admin user, keystores, and 3DES salt*.

The errors can be found the the `setup_errors.log` file and a detailed step by step installation is found in the `setup.log` file under the `/install/community-edition-setup` folder.

!!! Warning
    Use a FQDN (fully qualified domain name) as hostname and refrain from using 127.0.0.1 as IP address or usage of private IP is not supported and not recommended.

### Script Command Line Options
The `setup.py` script can be used to configure your Gluu Server and to add initial data
for oxAuth and oxTrust to start. If `setup.properties` is found
in this folder, these properties will automatically be used instead of
the interactive setup.

The administrator can use the following command line options to include additional components:

* __-r__ Install oxAuth RP
* __-p__ Install Passport
* __-d__ specify the directory where community-edition-setup is located. Defaults to '.'
* __-f__ specify `setup.properties` file
* __-h__ invoke this help
* __-n__ no interactive prompt before install starts. Run with `-f`
* __-N__ no Apache httpd server
* __-s__ install the Shibboleth IDP
* __-u__ update hosts file with IP address/hostname
* __-w__ get the development head war files
* __-t__ Load test data
* __-x__ Load test data and exit
* __--import-ldif=custom-ldif-dir__ Render ldif templates from custom-ldif-dir and import them in LDAP
* __--listen_all_interfaces__ Allow the LDAP server to listen on all server interfaces. This is required for clustered installations to replicate between LDAP servers. If not enabled, the LDAP server listens only to localhost
* __---allow-pre-released-features__ Enable options to install experimental features, not yet officially supported.
* __--remote-ldap__ Enables using remote LDAP server. For further information see https://github.com/GluuFederation/support-docs/blob/master/howto/4.0/setup_remote_LDAP.md
* __--remote-couchbase__ Enables using remote couchbase server. For further information see https://github.com/GluuFederation/support-docs/blob/master/howto/4.0/CE_with_remote_CB.md

Example Command: `# ./setup.py -ps` This command will install Gluu Server with Passport and Shibboleth IDP.

<!-- 
#### Couchbase Server Setup (Experimental)
Starting in CE 4.0, Gluu Server supports Couchbase Server as a database backend. To install with Couchbase, you need to download the OS-specific Couchbase package from https://www.couchbase.com/downloads (Enterprise version only), and save to `/opt/dist/couchbase`. For example, for Ubuntu 18,

```
# ls /opt/dist/couchbase
couchbase-server-enterprise_6.0.1-ubuntu18.04_amd64.deb
```

If both Couchbase and LDAP (either locally or remote) are available, you will be asked if you want to use hybrid backends:

```
Install (1) Gluu OpenDj (2) Couchbase (3) Hybrid [1|2|3] [1] : 3
  Please note that you have to update your firewall configuration to
  allow connections to the following ports:
  4369, 28091 to 28094, 9100 to 9105, 9998, 9999, 11207, 11209 to 11211,
  11214, 11215, 18091 to 18093, and from 21100 to 21299.
By using this software you agree to the End User License Agreement.
See /opt/couchbase/LICENSE.txt.
Use Gluu OpenDj to store (1) default (2) user (3) cache (4) statistic (5) site : 14
```

In this example, both OpenDJ and Couchbase will be used for storing data. Default storage (system configurations, attributes, clients, etc.) will be OpenDJ and also metric data (statistic) will be stored in OpenDJ. Other data will be stored in Couchbase server.

-->
