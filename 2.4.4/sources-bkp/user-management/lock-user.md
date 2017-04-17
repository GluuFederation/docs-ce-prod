# Lock User in Gluu Server
This section deals with the locking of user after 4 failed login attempts. This feature requires using the interception script to achieve the goal. The login attempts are stored in a custom attribute which needs to be created first.

## Create Custom Attribute
The custom attribute `oxCountInvalidLogin` will track the unsuccessful login attempts by any user. Please create that attribute from the oxTrust Admin GUI.

* Click on the add user button under **Configuration**
![image](../img/2.4/admin_config_attribute_add.png)

* Please fill up the form as shown in the screenshot below
![image](../img/2.4/custom_attribute.png)

* Click the **Update** button and the custom attribute is added in the Gluu Server

## Script Installation

* Go to Manage Custom Scripts
![image](../img/2.4/config-script_menu.png)

* Click on the Person Authenticaiton tab
![image](../img/2.4/config-script_person.png)

* Click on the Add custon script configuration button
![image](../img/2.4/config-script_add.png)

* Fill up the form with the following information:
![image](../img/2.4/config_script_update1.png)

    1. Name: LockAccount

    2. Description: Basic Lock Account

    3. Programming Language: Python

    4. Level: 1

    5. Location Type: Ldap

    6. Usage Type: Both methods

    7. Custom property(key/value)

      1. invalid_login_count_attribute: oxCountInvalidLogin

      2. maximum_invalid_login_attemps: 4

    8. Script: [Lock User Account Script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/basic.lock.account/BasicLockAccountExternalAuthenticator.py)

    9. Enable the script by ticking the check box 
![image](../img/2.4/config-script_enable.png)

    10. Click Update 
![image](../img/2.4/config-script_update.png)

    11. Change Default Authentication Method to LockAccount
![image](../img/2.4/lock_user_method.png)


