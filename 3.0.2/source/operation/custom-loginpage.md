# Customizing Public Pages

Most organizations will want to edit and customize the look and feel of public-facing Gluu Server pages, 
like the login and registration pages, to match their own corporate branding. 
The below documentation will provide the file locations of public facing pages, 
as well as instructions for adding custom html, css, and javascript files to your Gluu Server. 

## Overview
The Gluu Server's public facing pages are `xhtml` files. Before changing any files, we recommended taking backups so that no important elements are deleted from the pages.

The availbale pages are in the `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/` directory. 

The file which represents the primary login page is included in the `oxauth-any` directory.

## oxAuth Pages
You can find the public facing oxAuth pages in the following locations: 

- Default login page:
    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/login.xhtml`
- Authorization page:
    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/authorize.xhtml`
- Error page:
    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/error.xhtml`
- Custom authentication scripts: XHTML files in
    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/auth`

### How to remove the Gluu copyright 
To remove the Gluu copyright icon from your login page, navigate to the file template.xhtml that is located under
 
`/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/WEB-INF/incl/layout`.     

Then, simply remove this snippet:

```
<s:fragment rendered="#{not isLogin}">
    <div class="footer">
        <p>Copyright <a href="http://www.gluu.org">Gluu</a> All rights reserved.</p>
    </div>
</s:fragment>
```

## oxTrust Pages
You can find the public facing oxTrust pages in the following locations: 

- Default registration page:

    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/register.xhtml`

## Custom CSS, JS, Images

Custom CSS or images should be placed inside `/opt/gluu/jetty/oxauth/custom/static` with corresponding naming. 

For example, all images should be inserted under: 

`/opt/gluu/jetty/oxauth/custom/static/img` 

And all CSS are inside:

`/opt/gluu/jetty/oxauth/custom/static/stylesheet`

## Structure and paths for customizing pages 
A new location is added inside the Gluu Server `chroot` to make the customizations easy. The `/opt/gluu/jetty/` folder contains the `oxauth` and `identity` folder.

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

Customized `libs` can be placed in the following directories:

`/opt/gluu/jetty/identity/lib/ext`    
`/opt/gluu/jetty/oxauth/lib/ext`     

Custom `xhtml`, `page.xml`, etc should be placed in the following directories: 

`/opt/gluu/jetty/identity/custom/pages`    
`/opt/gluu/jetty/oxauth/custom/pages`    

Place static resources like `jpg`, `css`, etc. under the following directories:

`/opt/gluu/jetty/identity/custom/static`      
`/opt/gluu/jetty/oxauth/custom/static`       

To avoid collisions with static resources from WAR files, Gluu maps this folder to the URL: `/{oxauth|identity}/ext/resources`     

!!! Warning:
        Log into the Gluu Server chroot before working on design customizations for any pages.

Copy the default file(login.xhtml) to the external resource folder as shown in the below example

```
# cd /opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/    
# cp login.xhtml /opt/gluu/jetty/oxauth/custom/pages     
```

The example above shows that the `login.xhtml` file is copied to the external pages. The changes can be made here. 
Restarting jetty will display the changes. 

!!! Warning: 
    Customizations should only be made by people with a solid understanding of web-development.

## Jetty Restart 

Restart the `identity` and `oxauth` services for the customizations to be applied using the following commands:

```
# service identity stop
# service identity start
# service oxauth stop
# service oxauth start
```

**Note:** There is a 10 second delay on page modification reload.
