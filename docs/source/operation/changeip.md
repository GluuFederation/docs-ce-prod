# Change IP Address of existing Gluu CE Server

If your IP changes after initial setup, you need to change your Gluu Server's configuration.

1. Start the Gluu Server
1. Log into Gluu Server Chroot container
1. Update the Apache Configuration 
    - Navigate to `/etc/apache2/sites-available`
    - Open `https_gluu.conf` in a text editor
    - Change the IP address
    - Restart Apache2 with `service httpd restart`
1. Update the LDAP Configuration
    - Open the LDAP in an LDAP editor or browser
    - Update 'gluuIpAddress', under the root ou=appliances DN
1. Change the IP address in `/etc/hosts` file
1. Restart Solserver with `service solserver restart`
1. Restart Apache2 with `service httpd restart`
1. Restart the IDP if you have Shibboleth installed
1. Restart Identity with `service identity stop` and `service identity start`
1. Restart oxAuth with `service oxauth stop` and `service oxauth start`
1. Test
