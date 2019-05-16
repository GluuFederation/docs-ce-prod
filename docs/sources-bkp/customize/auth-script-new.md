[TOC]

# Writing a Custom Authentication Script

To develop Multi-factor Authentication with Custom Script. It was decided to write a script to use [Twilio](http://twilio.com) to send an SMS code to implement a two-step out-of-band authentication mechanism.

To use Twilio, registration with Twilio is required. For U2F, it is recommended to use token which is available online and register with Gluu.
To use Super Gluu authentication, Super Gluu mobile app available for iOS and android in their respective stores. 

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

Gluu Server User Interface allows the developer to specify the path to script rather than use the text box from oxTrust. The script will be loaded from the specified path. This feature will improve script development and there is an option to revert back
to working script, if the script is faulty or needs further enhancement. The administrator can select `File` from the Script Location
Type in oxTrust and the file input box will be displayed:

![image](../img/auth_article/script_upload_box.png)

The 'LDAP' option in the Script Location Type can be used to store the script in the LDAP tree once the development is complete. Remember that selecting the `LDAP` method requires that the script has to be copied in the input box
that appears upon LDAP selection:

![image](../img/auth_article/script_in_ldap.png)

## Suggested Development Environment

Gluu Server custom scripts are written in [Jython](http://www.jython.org/). It is recommended to use Eclipse for coding purposes.

Now, create some files:
- A Python file for your script
- Zero or more XHTML files if you have a custom form for your authentication
- Zero or more XML files (you'll need one for each XHTML file) that provide some information to the Tomcat server about how to display the XHTML file.

## Samples and Documentation

There are many good examples of authentication interception scripts checked into the 
[integrations folder](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations)
of the oxAuth project. Also, the respective `XHTML` and
`XML` files are checked in to the [auth folder](https://github.com/GluuFederation/oxAuth/tree/master/Server/src/main/webapp/auth).
The interfaces for the authentication interception can be found in the [Gluu Documentation](http://www.gluu.org/docs/reference/interception-scripts/#authentication).

In Twilio script, BAsic scripts are used [Basic Script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/basic/BasicExternalAuthenticator.py)

as a template. I also used the [Wikid Forms](https://github.com/GluuFederation/oxAuth/tree/master/Server/src/main/webapp/auth/wikid)
as my templates for the forms, because I remembered that I'd basically

need to get a code in step 2.

I also looked at the [Wikid Authentication](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/wikid/WikidExternalAuthenticator.py) script quite a bit for examples of how to process the form.

## Implement methods

authenticate():

The most important method to implement is obviously the
`authenticate` method. This is where the main business logic is located for
the authentication workflow. It is possible to switch on the
step, with the `if (step == 1):` statement. In oxAuth, there is no
assumption that step 1 and step 2 happen on the same server, so the step is sent
into the `authenticate` method.

ServerUtil.getFirstValue():

To access  information from requestParameters in your script with `ServerUtil.getFirstValue(requestParameters, <key>)` where `<key>`
specifies the value you want to retrieve, you can also use another method `requestParameters.get("<key>")`
where `<key>` specifies the value you want to retrieve .

getCountAuthenticationSteps():

Another method usually needed to implement is `getCountAuthenticationSteps`. This method normally just returns 1, 2, or 3. If implementing an adaptive authentication strategy,
where the number of steps depends on the context. Check out the
Duo script for a good example of this. In our sample [Duo script]
(https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/duo/DuoExternalAuthenticator.py),

Duo Script was scripted only for those who wanted to use Duo
for the IT group. So this was checked for group membership, and dynamically adjusted the number of steps. And this can be scripted for any logic or
attribute to the check the authentication, like "country" or "region".

getExtraParametersForStep():

If required to save session variables between steps, use the `getExtraParametersForStep` method. The Gluu Server persists
these variables in LDAP in able to support stateless clustered two
step authentications.

getPageForStep():

If required to display a special Web page for an interactive
login, (or even a custom first page) you'll need to implement the
`getPageForStep` which specifies the page you want to return for a given
step.

## Custom Properties

Sometimes it is helpful to enable system administrators to
enter properties that might change a lot. If administrators are
not allowed to modify the script, Custom Property feature can be used, as seen
in this screenshot:

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

Pure Python libraries, can be added to `/opt/tomcat/conf/python`, jar files can be added to `/opt/tomcat/endorsed`.

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

# Reverting Authentication Method

It is not unlikely that one may get locked out of Gluu
Server, while testing the authentication script.

If there is any problem in it. In such a case the following
method can be used to revert back the older authentication method. 

Please see the [FAQ](../faq/troubleshooting.md) for details.
