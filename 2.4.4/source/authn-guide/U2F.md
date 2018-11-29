# FIDO U2F

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

This script enables multi-factor authentication with any FIDO U2F device. Learn more about the U2F standard [here](https://www.gluu.org/resources/documents/standards/fido-u2f/). For a list of U2F compliant devices for sale, [check Amazon](http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=U2F). 

Some well known U2F device manufacturers include:  
- [Yubico](https://www.yubico.com/)   
- [HyperFIDO](http://hyperfido.com/)   
- [Feitian Technologies](http://www.ftsafe.com/)    

## Overview
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|u2f_server_uri		|URL of the u2f server		|https://idp.gluu.info|
|u2f_server_metadata_uri|URL of the u2f server metadata|https://idp.gluu.info|

## Configure U2F

Follow the steps below to configure the U2F module in the oxTrust Admin GUI.

1. Navigate to `Configuration` > `Manage Custom Scripts`.    

2. Click on the `Person Authentication` tab
![person-auth](../img/admin-guide/multi-factor/person-auth.png)
3. Select the U2F script
![u2f-script](../img/admin-guide/multi-factor/u2f-script.png)
4. Enable the script by ticking the check box
![enable](../img/admin-guide/enable.png)
5. Click `Update`
6. Change the `Default Authentication Method` to `u2f`
![u2f](../img/admin-guide/multi-factor/u2f.png)
