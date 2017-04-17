# Wikid Authentication
This is the person authentication module for [Wikid Authentication](http://wikidsystems.com).

## Overview
The module has the following mandatory properties

|	Peoperty	|	Description			|	Example		|
|-----------------------|---------------------------------------|-----------------------|
|wikid_server_host	|IP address of WIKID server		|192.168.1.1		|
|wikid_server_port	|TCP port for WIKID serve		|[8388][default 8388]	|
|wikid_cert_path	|Path to the PKCS12 certificate file	|/etc/certs/wikid.p12	|
|wikid_cert_pass	|Passphrase for  PKCS12 file		|passphrase		|
|wikid_ca_store_path	|[CA][ca] for WAS server certificate	|/etc/certs/CACertStore.dat|
|wikid_ca_store_pass	|Passphrase to secure the CA store file	|passphrase		|
|wikid_server_code	|Server domain 12 digit code		|135711131719		|

## Installation
### Configure CE Chroot
The following libraries must be present in the `$TOMCAT_HOME/endorsed` folder.

- https://www.wikidsystems.com/webdemo/wClient-3.5.0.jar
- http://central.maven.org/maven2/org/jdom/jdom/1.1.3/jdom-1.1.3.jar
- http://central.maven.org/maven2/log4j/log4j/1.2.17/log4j-1.2.17.jar
- http://central.maven.org/maven2/com/thoughtworks/xstream/xstream/1.4.8/xstream-1.4.8.jar

For more informatiaon about the wClient Library, please see [this page](https://www.wikidsystems.com/downloads/network-clients)

### Token Client
Wikid Authentication requires [token client](https://www.wikidsystems.com/downloads/token-clients). Please install and configure it for 
first time use. The [demo](https://www.wikidsystems.com/demo) explains how to do that.

### Configure oxTrust
Follow the steps below to configure the Wikid module in the oxTrust Admin GUI.

1. Go to Manage Custom Scripts
![image](../img/2.4/config-script_menu.png)

2. Click on the add custom script button
![image](../img/2.4/config-script_add.png)

3. Fill up the form and add the [Wikid Authentication Script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/wikid/WikidExternalAuthenticator.py)

4. Enable the script by ticking the check box
![image](../img/2.4/config-script_enable.png)

5. Click Update
![image](../img/2.4/config-script_update.png)

6. Change the Default Authentication method to Wikid
![image](../img/2.4/admin_auth_wikid.png)
