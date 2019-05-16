[TOC]

# Style Customizations
Static style elements like CSS, JavaScript and images are packaged into
separate jar files. They are named _\<ProjectName\>_ Static-
_\<version\>_ .jar, e.g. 'oxTrustStatic-1.3.0.Final.jar' and
'oxAuthStatic-1.4.0x.Final.jar'. These files are added to the deployable
war during build time.

Post deployment, the structure of the jar allows its context to be
accessible from the Web context root. For example, the default values of
the CSS and JavaScript locations are *\<contextPath\>/stylesheet* and
*\<contextPath\>/js* in the configuration file.

It is possible to unpack the contents of the said jar into a folder
hosted by a web server, and change the default cssLocation, jsLocation
and imgLocation attributes in the file `oxTrust.properties` and/or in
`oxauth-config.xml`.

* CSS: The location is specified using the property `cssLocation`.

* JavaScript: The location is specified using the property `jsLocation`.

* Images: The location is specified using the property `imgLocation`.

For example, in `oxTrust.properties` it looks like that:

```
cssLocation=https://idp.gluu.org/static/stylesheet
jsLocation=https://idp.gluu.org/static/js
imgLocation=https://idp.gluu.org/static/img
```

In the file `oxauth-config.xml` (as a children of \<configuration\>
node) it looks like that:

```
<cssLocation>https://idp.gluu.org/static/stylesheet</cssLocation>
<jsLocation>=https://idp.gluu.org/static/js<jsLocation>
<imgLocation>=https://idp.gluu.org/static/img<imgLocation>
```

# Page Customizations

Gluu server Community Edition makes editing public-facing pages easy
withour requiring the building of new war file. The files are in the
`xhtml` format and it is recommended to take backups so that no 
important element is deleted from the pages.

The availbale pages are inside the two directories `/opt/tomcat/webapps/identity` and
`/opt/tomcat/webapps/oxauth`.

oxAuth Pages:
- Default login page: `/opt/tomcat/webapps/oxauth/login.xhtml`
- Authorization page: `/opt/tomcat/webapps/oxauth/authorize.xhtml`
- Error page: `/opt/tomcat/webapps/oxauth/error.xhtml`
- Custom authentication scripts: XHTML files in `/opt/tomcat/webapps/oxauth/auth`

oxTrust Pages:

- Default registration page: `/opt/tomcat/webapps/identity/register.xhtml`

To remove the Gluu copyright icon from your login page, navigate to the file template.xhtml that is located under /opt/tomcat/webapps/identity/WEB-INF/incl/layout. Then, simply remove this snippet:
```
<s:fragment rendered="#{not isLogin}">
    <div class="footer">
        <p>Copyright <a href="http://www.gluu.org">Gluu</a> All rights reserved.</p>
    </div>
</s:fragment>
```
A new tomcat wrapper variable is added to avoid hard coding or changing application configurations. 
```
wrapper.java.additional.20=-Dgluu.external.resource.base=/var/gluu/webapps
```

## Customizing Pages
A new location is added inside the Gluu Server `chroot` to make the customizations easy. The `/var/gluu/webapps/` folder contains the `oxauth` and `oxtrust` folder which contains the `libs`, `pages` and `resources` folder where the customized pages can be placed to overwrite the default pages. The structure can be illustrated as follows:

```
    /var/gluu/webapps/
	|-- oxauth
	|   |-- libs
	|   |-- pages
	|   `-- resources
	`-- oxtrust
    		|-- libs
    		|-- pages
    		`-- resources
```

!!! Warning
    Log into the Gluu Server chroot before working on the customized pages

* Please make way to the default pages folder to copy the default file to the external resource folder
```
# cd /opt/tomcat/webapps/oxauth/
# cp login.xhtml /var/gluu/webapps/oxauth/pages/ 
```
The example above shows that the `login.xhtml` file is copied to the external pages. The changes can be made here and restarting Tomcat server will display the changes made to the specific customized page. The customizations must not be made by people will little/no web-development knowledge.

## Tomcat Restart Policy
Tomcat Server does not need restart generally when custom pages are added in Gluu Server. However in the following cases, please restart Tomcat.

1. Default Page overriden with custom page as JSF may cache path to original version

2. Removal of page to replace context with empty page to invalidate it

3. New environment variable is introduces

**Note:** There is a 10 second delay on page modification reload
