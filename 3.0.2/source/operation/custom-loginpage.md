# Customize Login Page

Gluu provides you with the feasibility to customize your login page and styles as per the 
organization standards.
 
## Style Customizations
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
## Page Customizations

Gluu server Community Edition makes editing public-facing pages easy
withour requiring the building of new war file. The files are in the
`xhtml` format and it is recommended to take backups so that no 
important element is deleted from the pages.

The availbale pages are inside the two directories 

`/opt/jetty-9.3/temp/jetty-localhost-8082-identity.war-_identity-any-{random number}.dir`

`opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir`.

oxAuth Pages:

- Default login page: `/opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir/webapp/login.xhtml`
- Authorization page: `/opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir/webapp/authorize.xhtml`
- Error page: `/opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir/webapp/error.xhtml`
- Custom authentication scripts: XHTML files in `/opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir/webapp/auth`

oxTrust Pages:

- Default registration page: `/opt/jetty-9.3/temp/jetty-localhost-8082-identity.war-_identity-any-6948849492655524434.dir/webapp/register.xhtml`

To remove the Gluu copyright icon from your login page, 
navigate to the file template.xhtml that is located under
 
`/opt/jetty-9.3/temp/jetty-localhost-8082-identity.war-_identity-any-{random number}.dir/webapp/WEB-INF/incl/layout`. 

Then, simply remove this snippet:

```
<s:fragment rendered="#{not isLogin}">
    <div class="footer">
        <p>Copyright <a href="http://www.gluu.org">Gluu</a> All rights reserved.</p>
    </div>
</s:fragment>
```

## Customizing Pages
A new location is added inside the Gluu Server `chroot` to make the customizations easy. 
The `/opt/gluu/jetty/` folder contains the `oxauth` and `identity` folder.

The structure can be illustrated as follows:


```
   /opt/gluu/jetty/
	|-- oxauth
	|   |-- libs
		`--	ext
    	|-- custom
	|	`-- pages
	|	`-- static
	`-- identity
    		|-- libs
			`--	ext
    		|-- custom
			`-- pages
			`-- static
```

Customized `libs` are to be placed under 

`/opt/gluu/jetty/identity/lib/ext`
`/opt/gluu/jetty/oxauth/lib/ext`

Custom `xhtml`, `page.xml`, etc should be placed under 

`/opt/gluu/jetty/identity/custom/pages`
`/opt/gluu/jetty/oxauth/custom/pages`

To place static resources like `jpg`, `css`, etc are placed under the below folder

`/opt/gluu/jetty/identity/custom/static`
`/opt/gluu/jetty/oxauth/custom/static`

To avoid collisions with static resources 
from war files, Gluu maps this folder to next URL: `/{oxauth|identity}/ext/resources`

!!! Warning:
        Log into the Gluu Server chroot before working on the customized pages

* Please make way to the default pages folder to copy the default file to the external resource folder.

```
# cd /opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-{random number}.dir/webapp/
# cp login.xhtml /opt/gluu/jetty/oxauth/custom/pages 
```

The example above shows that the `login.xhtml` file is copied to the external pages. 
The changes can be made here and restarting jetty will display the changes 
made to the specific customized page. The customizations must not be made by people 
will little/no web-development knowledge.

## Jetty Restart Policy
Restart `identity` and `oxauth` services for the following to be executed:
```
# service identity stop
# service identity start
# service oxauth stop
# service oxauth start
```

1. Default Page overriden with custom page as JSF may cache path to original version

2. Removal of page to replace context with empty page to invalidate it

3. New environment variable is introduces

**Note:** There is a 10 second delay on page modification reload.