# Writing a Custom Authentication Script

In this document we walk through the steps of writing a script to implement OTP authentication using [Twilio](http://twilio.com) to send an SMS code for a two-step out-of-band authentication mechanism.

At the end of this tutorial you should have a better understanding of how to write your own custom scripts. For reference, you can review the completed Twilio custom authentication script [here](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/twilio_sms/twilio2FA.py). 

Fields in Custom Script:

|Field     |Description           |
|----------|:---------------------|
|Name    |Name of the Script|
|Description  |[optional] Description about the script|
|Programming Language |Currently Python is supported, In future jscript and Java script might be added|
|Level    | Authentication Level for the authentication, which determines the security level|
|Location Type    |Determines the script location. Can be stored in a "File" or could be stored in "LDAP"|
|Usage Type       |Determines the type of the usage. Web, Native or Both|
|Custome Property |Determines the key and value of the custom property, which can added to the authentication to pass the values|
|Script Box |Script Box will displayed if Location Type is selected as "File", to enter the path of the script|
|Script     |Script Box will be displayed when Location Type is selected as "LDAP"|

## Custom Script Location

Custom scripts can either be inserted directly into the Gluu Server interface or you can specify a path to the script. Specifying a path will make script development easier. There is also an option to revert back to a working script if the script is faulty or needs further enhancements. The administrator can select `File` from the Script Location Type in oxTrust and the file input box will be displayed:

![image](../img/auth_article/script_upload_box.png)

The 'LDAP' option in the Script Location Type can be used to store the script in the LDAP tree once the development is complete. Remember that selecting the `LDAP` method requires the script to be copied in the input box that appears upon LDAP selection:

![image](../img/auth_article/script_in_ldap.png)

## Suggested Development Environment

Gluu Server custom scripts are written in [Jython](http://www.jython.org/). It is recommended to use Eclipse for coding purposes.

Now, create some files:
- A Python file for your script
- One or more XHTML files if you have a custom form for your authentication
- One or more XML files (you'll need one for each XHTML file) that provide some information to the Tomcat server about how to display the XHTML file.

## Samples and Documentation

There are many good examples of authentication interception scripts checked into Gluu's  
[oxAuth integrations folder](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). Also, the respective `XHTML` and `XML` files are checked in to the [auth folder](https://github.com/GluuFederation/oxAuth/tree/master/Server/src/main/webapp/auth).
The interfaces for the authentication interception can be found in the [Gluu Documentation](http://www.gluu.org/docs/reference/interception-scripts/#authentication).

We used the [Basic Script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/basic/BasicExternalAuthenticator.py) 
as a template. The [Wikid forms](https://github.com/GluuFederation/oxAuth/tree/master/Server/src/main/webapp/auth/wikid) were also used as a template since it is required to pass the value of the "code" obtained from Twilio to step 2 of the authentication in order to validate and authenticate the user.

The [Wikid authentication](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/wikid/WikidExternalAuthenticator.py) script was also looked upon quite a bit for examples on how to process the form.

## Implement methods

Simple example of how to add a custom template and how to pass values between 2 steps of authentication and save the value temporarily for authentication of a user. Our Sample 
[Twilio script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/twilio_sms/twilio2FA.py)

1. Login to Gluu UI
2. Navigate to "Configuration" on the Menu panel to the left
3. Select Manage Custom Scripts
4. Scroll to the end of the page and click on "Add custom script configuration"
5. Enter the Name, Description, Programming Language (Python will be by default, may be in future Java or JavaSCript will be added)
6. Select the Level needed to set the security level to.
7. Select Location Type from the script to be executed.
8. Select the Usage Type required for the authentication.
9. Define Custom property which is provided by Twilio and can be noted down from Twilio account page of the signed up user. 
10. Click on Enabled to enable the added custom script.
11. Scroll down to the end of the update and click on Update button to submit the form. 
12. After the custom script is added, click on Manage Authenticaion on the Menu Panel to left. 
13. Select "Default Authentication Method" tab and change the oxTrust authentication mode to "Twilio" or "Name of the script" from the drop down.

**Note: All three below custom properties are mandatory for the Twilio Two-Factor Authentication script to work**

  - ACCOUNT_SID - Numerical sequence of numbers, to identify the token assigned to the user associated with Twilio.
  - AUTH TOKEN  - Alphanumerical number provided by Twilio for the account holder to identify the user.
  - FROM_NUMBER - Number which is either assigned by Twilio or can be a number user provides to send the code from.

As shown in the below illustration:

![image](https://github.com/GluuFederation/docs/blob/master/sources/img/auth_article/twilio.png?raw=true)

###Methods 
**authenticate():**

The most important method to implement is obviously the `authenticate` method. This is where the main business logic is located for
the authentication workflow. It is possible to switch on the step, with the `if (step == 1):` statement. In oxAuth, there is no
assumption that step 1 and step 2 happen on the same server, therefore the value stored in the LDAP using a temporarily created attribute and retrieved in step 2. There the step is sent into the `authenticate` method, which helps to save and retrieve the values whereever required.

Below are few Methods and Libraries used to Save the Value to LDAP and retrieve the values as per the requirement.

**random.randit()** 
random.randit("start number",""end number"), Generates the code as per designer or requirements. 
Example: random.randit(10000,99999)

**context.set()**
This particular method is obtained from jboss to pass the session attribute value to ldap, by creating a temporary attribute which has limited life time and can be retrieved within the life span, expires and session becomes invalid. Save the value of the code obtained through the code generator method. context.set("Name of the temp attribute", `<key>`). Where `<key>` is the value that needs to be stored temporarily in ldap.
Example:
context.set("code",code)

**UserService.instance()** 
Gets the user login instance

**ServerUtil.getFirstValue():**

To access  information from requestParameters in your script with `ServerUtil.getFirstValue(requestParameters, <key>)` where `<key>`
specifies the value you want to retrieve, you can also use another method `requestParameters.get("<key>")`
where `<key>` specifies the value you want to retrieve .

**userService.getUserByAttribute():**

`getUserByAttribute("LDAP Attribute", <key>)` method access the information in LDAP and retrieves the value of the attribute comparing the value of the `<Key>`.
Example:
userService.getUserByAttribute("uid", user_name)

**getAttribute():**
To retrieve the value of an attribute from LDAP, getAttribute("LDAP Attribute name") can be used. 
Example:
getAttribute("mobile")

**requestParameters.get():**
To retrieve values passed from the form through header can be obtained by using the method requestParameters.get(`<key>`). This will retrieve the values from the form via header and can be stored in a string. Where `<key>` is the value to be retrieved from header.
Example:
abc = requestParameters.get("passcode")[0].strip()


**getCountAuthenticationSteps():**

Another method usually needed to implement is `getCountAuthenticationSteps`. This method normally just returns 1, 2, or 3. If implementing an adaptive authentication strategy,
where the number of steps depends on the context. Check out the
Duo script for a good example of this. In our sample 
[Duo script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/duo/DuoExternalAuthenticator.py),

Duo Script was scripted only for those who wanted to use Duo
for the IT group. So this was checked for group membership, and dynamically adjusted the number of steps. And this can be scripted for any logic or attribute to the check the authentication, like "country" or "region".

**getExtraParametersForStep():**

If required to save session variables between steps, use the `getExtraParametersForStep` method. The Gluu Server persists
these variables in LDAP in able to support stateless clustered two
step authentications.

**getPageForStep():**

If required to display a special Web page for an interactive
login, (or even a custom first page) you'll need to implement the
`getPageForStep` which specifies the page you want to return for a given
step.

**session_attributes.get():**
The attribute value that are saved by the session using context.set. This method is derived from the oxauth core java libraries and called using the SessionState parameters which is defined in the code or programme.
session_attributes.get(`<key>`), where `<key>` is the session atribute value that is stored in the ldap.
Example:
session_attributes.get("code")


##Saving the value in LDAP and Passing values between two steps
 
####Saving Values:

**context.set** can be used to save values of the required key to an attribute temporarily and the created temporary attribute will be alive only for limited time and expires and gets removed, by that way, adding new attribute to the user is not messed up. And also the expired attribute kills the validity of the session and becomes invalid.

####Retriving and passing values between the authentication steps:

Using **session_attribute.get()** method, stored session attribute could be retrieved anywhere between the authentication method, by that way the values can be passed between two authentication methods for verification and validation.
Generated code and the entered "code" in the form can be verified using a simple if and the "code" from the form can be obtained using the requestParameters.get() method or serviceUtil.getFirstValue() method.

## Custom Properties

Sometimes it is helpful to enable system administrators to
enter properties that might change a lot. If administrators are
not allowed to modify the script, Custom Property feature can be used, as illustrated in below screenshot:

![image](../img/auth_article/07-custom-properties.jpg)

configurationAttributes.get("<key>").getValue2"():

To access this information in your script with 
`configurationAttributes.get("<key>").getValue2()`
where `<key>` specifies the value you want to retrieve.

## Returning a message to the user

It is possible to use the Context to return a message to the
user, which could be especially useful if an error occurs, or if
required to have some kind of user action.

## Adding Libraries

Pure Python libraries, can be added to `/opt/tomcat/conf/python`, 
jar files can be added to `/var/gluu/webapps/oxauth/libs`.

**Note:** jar files should be added within chroot. And not in the main `/var/` of the system.

## Testing

When the scripting is done, you can test the script by print
the statments to wrapper.log under `/opt/tomcat/logs/wrapper.log`. 

And by prefix the logs, will help to find the script at ease
using tail command `tail -f | grep <prefix>`, the prefix logs will
provide the script output while one trys to login using the script.

In the Twilio test script, a specific method called
`printOut` has been scripted to make it easier to add this prefix.

Also, remember that putting all the code in a `try / catch`
is a good practice to avoid unhandled exceptions. Since during
debugging, those exception may provide a hint pointing what causes the issue.

Further logs to debug and monitor the sequence can be done using oxauth_script.log and oxauth.log
under`/opt/tomcat/logs/` which is within the chroot.

## Reverting Authentication Method

It is not unlikely that one may get locked out of Gluu
Server, while testing the authentication script.

If there is any problem in it. In such a case the following
method can be used to revert back the older authentication method. 

As a secondary option, InPrivate or Incognito or Private Browser from various Browsers can be used.

Please see the [FAQ](../faq/troubleshooting.md) for details.
