# Change IP Address of existing Gluu CE Server

Question: What if my IP changes? Do I need to reinstall whole Gluu Server? 

Answer: No. Here is how you can apply new IP in Gluu Server 3.1.x

- Start container
- Log into Gluu Server container
- Configuration in apache2: 
    - https_gluu.conf (location: /etc/apache2/sites-available )
    - Apply new IP by replacing old one
    - Restart apache2
    
    `service httpd stop`
    
    `service httpd start`
    
- Configuration in ldap: (open LDAP in LDAP editor/browser)
    - Change 'gluuIpAddress'. It's under root ou=appliances DN
- Change IP address in `/etc/hosts` file
- Restart 'solserver'

    `service solserver stop`
    
    `service solserver start`
    
- Restart apache2

    `service httpd restart`
    
- Restart idp ( If you have Shibboleth installed )
- Restart identity

    `service identity stop`
    
    `service identity start`
    
- Restart oxauth

    `service oxauth stop`
    
    `service oxauth start`
    
- Test
