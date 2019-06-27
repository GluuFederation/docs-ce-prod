# Change IP Address of existing Gluu CE Server

If your IP changes after initial setup, you need to change your Gluu Server's configuration.

1. Start the Gluu Server
1. Log into Gluu Server Chroot container
1. Update the Apache Configuration 
    - Navigate to `/etc/apache2/sites-available`
    - Open `https_gluu.conf` in a text editor
    - Change the IP address
    - [Restart](./services.md#restart) the `apache2` service
1. Update the LDAP Configuration
    - Open the LDAP in an LDAP editor or browser
    - Update 'gluuIpAddress', under the root ou=appliances DN
1. Change the IP address in `/etc/hosts` file
1. [Restart](./services.md#restart) the `opendj` service
1. [Restart](./services.md#restart) the `httpd` service
1. [Restart](./services.md#restart) the `idp` service
1. [Restart](./services.md#restart) the `identity` service
1. [Restart](./services.md#restart) the `oxauth` service
1. Test
