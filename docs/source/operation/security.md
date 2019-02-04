# Security recommendations

The Gluu Server is designed to be easy to deploy. Its default security settings may not be strict enough for certain organizations or use cases. This document highlights important security controls and offers best practices for increasing security related to a Gluu Server infrastructure

## Storing setup.properties.last 

The `setup.properties.last` file created under the `/install/community-edition-setup/` directory during `setup.py` phase of initial installation contains sensitive data like credentials and keystore passwords. The original file should be removed from inside the container and a copy of its contents should be stored securely for future reference.

## Apache config

Apache is the frontend web server in a default Gluu Server setup. Its configuration will greatly impact security for the whole instance. Of particular interest are items found inside the container under `/etc/httpd/` (CentOS/RHEL) and `/etc/apache2/` (Ubuntu/Debian). 

The following controls within the Gluu Server's virtual host files in `/etc/httpd/conf.d/https_gluu.conf` and `/etc/apache2/sites-enabled/https_gluu.conf` should be reviewed: 

  - Enabled SSL/TLS cipher suites; depending on project-specific requirements some of them may not be considered secure enough
  
  - "Content-Security-Policy" and "X-Frame-Options" clauses which are commented out by default; keep in mind those haven't been properly tested and default settings may need to be adjusted to be compatible with the current Gluu Server package
  

## Securing oxTrust

### Block access

We recommend blocking access to the oxTrust web UI from public networks. This can be achieved, for example, by limiting access to a specific IP address/network range only, by updating corresponding "Location" directive in `/etc/httpd/conf.d/https_gluu.conf` In example below access is only allowed from one specific private range ip address, three private network ip address ranges, and from localhost (what is useful if you prefer to access oxTrust by forwarding TCP port 443 of your remote Gluu Server instance to your local machine):


```
        <Location /identity>
                ProxyPass http://localhost:8082/identity retry=5 connectiontimeout=5 timeout=15
                <RequireAny>
                    Require ip 192.168.240.2
                    Require ip 10 172.20 192.168.248
                    Require ip 127.0.0.1
                </RequireAny>
        </Location>
```

!!! Note
    oxTrust is responsible for publishing SCIM APIs. If SCIM is in use, the IP address of the SCIM client should be included to the rule above as well


### Configure 2FA 

Consider enforcing 2FA for access to oxTrust. Gluu supports an assortment of 2FA methods out-of-the-box, including [Duo Security](https://gluu.org/docs/ce/3.1.3/authn-guide/duo/), [Super Gluu](https://gluu.org/docs/ce/3.1.3/authn-guide/supergluu/) or [FIDO U2F](https://gluu.org/docs/ce/3.1.3/authn-guide/U2F/).

## Enabled extensions

`Configuration` > `Organization configuration` page contains several controls which may impact security of the instance if left enabled. Consider disabling the following settings unless otherwise required:   

- "SCIM Support" - enables [SCIM protocol](https://gluu.org/docs/ce/3.1.4/user-management/scim2/) implementation which allows remote clients to conduct reads and writes of user data stored locally at the instance. Being a powerful tool for conducting user management-related batch jobs, it could become a powerful tool for destruction in the wrong hands.

- "Passport Support" - Passport enables many new user authentication methods, like social login, but also increases the surface area for security issues. Any time a new authentication method is added, its security should be thoroughly tested for both positive and negative scenarios.  

- "CAS Support" - CAS support comes pre-packaged with the Shibboleth IDPv3 used by the Gluu Server to support SAML2. CAS is a legacy protocol, and unless it is required, support should be disabled in order to reduce attack surface area. 

## User registration

Gluu Server offers a few basic user management features, inlcuding user registration. Generally, it's not recommended to employ those features in production. Unless Gluu's user registration features must be used, consider the following:

- Make sure no scripts are enabled at `Configuration` > `Manage Custom scripts` > `User Registration` page    
- Make sure that `Self-Service Password Reset` control at `Configuration` > `Organization configuration` page is set to `Disabled`    

## oxAuth / Authentication

oxAuth is the core auth engine for the Gluu Server. Its security is paramount for the integrity of the whole instance. A few notes and considerations:  

- Make sure only needed authentication scripts are enabled at `Configuration` > `Manage Custom scripts` > `Person Authentication`. It's extremely important to disable any authentication not in use. 

- Consider enabling brute-force attack protection by setting `authenticationProtectionConfiguration` to `True` in `Configuration` > `JSON Configuration` > `oxAuth`

- Review values chosen for `sessionIdUnusedLifetime` and `sessionIdLifetime` at `Configuration` > `JSON Configuration` > `oxAuth` page and make sure sessions won't last longer than an average user would need; longer living sessions present higher risks of session hijacking and unauthorized access from shared/public devices 

- Review configuration of oxAuth's built-in filter implementing [CORS protocol](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) located in section `corsConfigurationFilters` at `Configuration` > `JSON Configuration` > `oxAuth`. These controls dictate web services at which domains are expected to host on-page scripts which may generate requests to oxAuth API's endpoints - and thus should be allowed to access data sent in responses to them. This is especially important if the OP must support on-page OIDC clients employing implicit or hybrid flows. By default the filter will allow RPs at any domain the right to view the data.

## Open ports 

Make sure no services are listening on external interfaces except for those that are absolutely required. 

In a standalone instance of Gluu Server 3.1.4, only Apache's listener at TCP port 443 is required to be open to the world. 

A list of current listeners can be obtained with `# netstat nlpt` (for TCP) and `# netstat -nlpu` (for UDP). In particular, make sure the internal LDAP server used by Gluu to store all its configuration data listens only at loopback interface.

In previous versions of Gluu Server OpenDJ can be seen listening on ports 4444 and 1636 for all interfaces, thus it's recommended to reconfigure it following the recommendation above (please refer to [corresponding documentation](https://backstage.forgerock.com/docs/opendj/3/admin-guide/#configure-ldap-port) for detailed steps).

In cases when listeners at external interfaces cannot be avoided (clustered setups be the most obvious example) we suggest to ensure that those ports will only be accessible from a very limited set of authorized peers by fine-tunining firewal rules and underlying network's topology.

## Dynamic Client Registration

Consider whether support of [OpenID Connect Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html) extension is required. If not, disable it by setting `dynamicRegistrationEnabled` to `False` at `Configuration` > `JSON Configuration` > `oxAuth` page.

In case this feature must be enabled, next controls must be re-visited to minimize potential exposure of sensitive personal data:

- `trustedClientEnabled` and `dynamicRegistrationPersistClientAuthorizations` at `Configuration` > `JSON Configuration` > `oxAuth` - control whether clients are allowed to setup an entry for them in such way users won't be asked for consent on releasing their personal data while accessing corresponding RP

- list of scopes at `OpenID Connect` > `Scopes`, column "Allow for dynamic registration" - allows to quickly assess which scopes clients can potentially add to their registration entry without consent of OP's administrator; set `Allow for dynamic registration` property to `False` for all scopes you want to assign in a controlled fashion; in addition, make sure none of sensitive scopes have their type set to `Default` if `dynamicRegistrationScopesParamEnabled` is set to `True` (see below)

- `dynamicRegistrationScopesParamEnabled` at `Configuration` > `JSON Configuration` > `oxAuth` - controls whether default scopes are globally enabled at this instance; scopes defined as default will be automatically added to any dynamically registered client entry

## UMA

[User Managed Access](https://gluu.org/docs/ce/3.1.4/admin-guide/uma/) allows adopters to designate the task of making access authorization decisions for an resource to a dedicated 3rd party service capable of automatically handling requests to access a resource even without its owner being present online, following a set of rules defined for it. Needless to say such feature-rich framework can provide a lot of attack vectors for those seeking unauthorized access.

Next controls allow you to fine-tune Gluu's UMA implementation's behaviour, resulting in more secure interactions:

- `umaGrantAccessIfNoPolicies` at `Configuration` > `JSON Configuration` > `oxAuth` page - allows access to a resource even if no policies are defined for the realted scopes; though it simplifies initial testing, we recommend disabling this feature in production setups

- `umaRestrictResourceToAssociatedClient` at `Configuration` > `JSON Configuration` > `oxAuth` page - won't allow any other client except the one which registered the resource initially to acquire a RPT for it; it's recommended to have it enabled for production setups

## Upgrades

Needless to say, keeping your instance up to date is paramount for maintaining its security. List of the latest vulnerabilities in the Gluu Server suite itself and corresponding patches can be found [here](https://gluu.org/docs/ce/3.1.4/upgrade/patches/). In addition,  updates should be conducted for all system components both inside and outside of container on regular basis.

!!! Warning
    Gluu's repository must be disabled before any attempt to update packages outside of container as described [here](https://gluu.org/docs/ce/3.1.3/installation-guide/install/#5-disable-gluu-repositories)):

  - For RHEL/CentOS distros, use `# yum update` inside and outside of container
  
  - For Ubuntu/Debian distros, use `# apt-get upgrade` or `# apt-get dist-upgrade` outside of container and `# apt-get upgrade` inside of it

!!! Warning
    `# apt-get dist-upgrade` command is not safe to run inside Ubuntu/Debian containers!
  
## General security best practices still apply

Regardless of how specialized application is, general considerations still apply. This includes (but is not limited to):

  - Ensure physcial security of the machine where Gluu Server dwells, even if in a vastly virtualized world of today that term has become rather vague. Make sure booting from CD/DVD, External Devices, Floppy Drive is disabled in its BIOS and any physical (or "physical") I/O ports or devices (USB, FireWire, directly attached keyboard etc) are not accessible for un-authorized public
  
  - Minimize number of packages to minimize number of associated vulnerabilities (avoid installation of unnecessary packages and uninstall packages you don't need)
  
  - Make sure that only highly secure means are used when accessing the server for administration purposes; using the most recent SSH server package is a no-brainer, we also suggest to configure it to deny login as a root user and disable password authentication (use public key instead), and move its listener to a port different from the standart TCP 22
  
  - The system must be backed up on regular basis; frequency may depend on data velocity and volume, but keep in mind that in case of a compromised system restoring from a backed up copy predating the incident may become the only option to ensure its integrity without losing months (even years) of work, and often a lot of time may pass since intrusion before security alarms will be triggered; moreover, as backups on itself is a high priority target for potential intruder, they thus must be properly secured (locked up and/or encrypted); that includes controls of the system conducting back up as well to prevent manipulations with state of the protected resource (i.e. to prevent restoring system to a pre-patched state with a known vulnerability)

## Ongoing Security Audits

Even with all possible requirements met, regular security audits conducted by experienced security professionals are invaluable source of objective opinions on how secure your environment really is. Feel free to contact us at [here](mailto:security@gluu.org) with head-ups on any issues discovered during your internal investigations - we'll try our best to offer remediation instructions ASAP. We greatly appreciate your efforts in making Gluu products better and safer for everyone!
