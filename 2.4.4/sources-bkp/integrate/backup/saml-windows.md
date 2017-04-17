# Configuring Apache Shibboleth SP in Windows

## Shibboleth SP Installation

1. Download the MSI of Shibboleth-SP from:
   http://www.shibboleth.net/downloads/service-provider/latest/ .

2. Start the installation

![IMAGE](../img/sp_setup/admin_sp_click.png)

3. Define the destination folder (by default it is: C:\opt\shibboleth-sp).

![IMAGE](../img/sp_setup/admin_sp_destination.png)

4. Select the Shibboleth Daemon port. By default it is 1600, and you may
   keep it for testing it, locally.

![IMAGE](../img/sp_setup/admin_sp_port.png)

5. Now, there are two options. According to your target you will have to
choose one.

	1. Option 1: If you install Shibboleth for the Apache Web Server

	2. Option 2: If you install Shibboleth for Microsoft IIS Web Server

		a. For the Microsoft IIS Web Server, CHECK “Install ISAPI filter
		and configure IIS”. Remember to put the file Extension ”.sso” --
		this is necessary.

![IMAGE](../img/sp_setup/admin_sp_microsoft.png)

		
		b. For the Apache Web Server, UNCHECK "Install ISAPI filter and
		configure IIS".

![IMAGE](../img/sp_setup/admin_sp_apachesetup.png)

	3. UAC of Windows 7 may block this program, so allow it.

![IMAGE](../img/sp_setup/admin_sp_uac.png)

## Apache Configuration

1. Download the Apache HTTP server MSI Installer with OpenSSL:
   http://httpd.apache.org/download.cgi#apache22 .

![IMAGE](../img/sp_setup/admin_sp_apacheclick.png)

2. Select the destination. You can keep the default destination for your
local testing. But, make sure that there is no other “Apache Software
Foundation” directory in your current “C:\Program Files\” location.

![IMAGE](../img/sp_setup/admin_sp_apachedestination.png)

3. Provide the Server Information. For local testing you can use
   `localdomain/localhost`.

![IMAGE](../img/sp_setup/admin_sp_serverinfo.png)

4. Test whether the Apache web server is installed or not. Open your web
browser and use `localhost`. If you see something like the image shown
below--you are done!

a![IMAGE](../img/sp_setup/admin_sp_apachetest.png)

### Shibboleth and Apache Configuration

1. Change the permission of the Apache installation directory, and
   provide “write” access.

2. `httpd.conf` configuration

	1. Change “ServerName localhost:80” (for your local testing)

	2. Copy `apache22.conf` from the Shibboleth directory to `~/apache/conf/extra/`

3. `Shibboleth2.xml` configuration

	1. Change: Host name=“localhost” (for local testing)
    
	2. Change: entityID=“https://localhost/shibboleth” (for local testing)
    
	3. Change: ApplicationOverride id=“admin” entityID=“https://localhost/shibboleth/”

4. Reboot your windows machine.

## Test SP Installation with Windows and Apache

1. Open the web browser, and provide the address:
   `localhost/Shibboleth.sso/Status`
2. If you can see some XML page like the one shown below--you are done
   with your SP installation in Windows through Apache2.

 a![IMAGE](../img/sp_setup/admin_sp_checkstatus.png)
