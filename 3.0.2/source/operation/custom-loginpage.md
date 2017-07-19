# Customizing Public Pages

Most organizations will want to edit and customize the look and feel of public-facing Gluu Server pages, 
like the login and registration pages, to match their own corporate branding. 
The below documentation will provide the file locations of public facing pages, 
as well as instructions for adding custom html, css, and javascript files to your Gluu Server. 

## Overview
The Gluu Server's public facing pages are `xhtml` files. Before changing any files we recommended taking backups so that no important elements are lost.

The available pages are in the `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/` directory. The file which represents the primary login page is included in the `oxauth-any` directory.

Each Gluu Server component is deployed as a separate archive in WAR format. When any component's service is started, its archive is unpacked ("exploded") to Jetty's temporary file directory located under `/opt/jetty-9.3/temp/`. 

To customize any files used by a component, the file needs to be changed either at the location where they are unpacked, or in the corresponding archive itself. Note that, changes to files done "in place" won't be persisted--each time a component's service is restarted its `.war` archive will be re-exploded, overwritting the existing content on the disk.

A typical example would be customizing oxAuth's login page. There are two ways to acheive this:

1. Un-pack the needed files from oxauth.war with a tool like `jar`, update them and add them back to the archive with all required dependencies (Not recommended);

2. Put the files under the `/opt/gluu/jetty/oxauth/custom/` directory, which will be used instead of the standard files in `oxauth.war`. (Explained below. Note: the same approach will work for oxTrust if files are placed under `/opt/gluu/jetty/identity/custom/`). The benefit of using this approach is that your customizations won't be disturbed by any changes to oxauth.war or identity.war (for example, in case this Gluu instance will be patched and a component's WAR archive will be overwritten)

## Directory structure and mappings used by the feature

A new location is added inside the Gluu Server `chroot` to make the customizations easy. 
The `/opt/gluu/jetty/` folder contains the `oxauth` and `identity` folder.

The structure can be illustrated as follows:

oxAuth:

```
/opt/gluu/jetty/oxauth/
|-- custom
|   |-- pages
|   `-- static
|-- lib
|   `-- ext
```

oxTrust:

```
/opt/gluu/jetty/identity/
|-- custom
|   |-- pages
|   `-- static
|-- lib
|   `-- ext
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

To avoid collisions with static resources from WAR files, Gluu maps 
this folder to the URL: `/{oxauth|identity}/ext/resources`     

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

## Custom CSS, JS, Images

Custom CSS or images should be placed inside `/opt/gluu/jetty/oxauth/custom/static` with corresponding naming. 

For example, all images should be inserted under: 

`/opt/gluu/jetty/oxauth/custom/static/img` 

And all CSS are inside:

`/opt/gluu/jetty/oxauth/custom/static/stylesheet`

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
oxTrust is responsible for displaying the Gluu Server's default registration page. 

- You can find the default registration page here:

    `/opt/jetty-x.x/temp/jetty-localhost-xxxx-oxauth.war-_oxauth-any-1234.dir/webapp/register.xhtml`

## Jetty Restart 

Restart the `identity` and `oxauth` services for the customizations to be applied using the following commands:

```
# service identity stop
# service identity start
# service oxauth stop
# service oxauth start
```

**Note:** There is a 10 second delay on page modification reload.
