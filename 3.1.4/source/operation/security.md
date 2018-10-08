# Security recommendations

To make initial deployment easier for adopters with different levels of expertise, Gluu Server package is shipped with security-related settings some users may find not strict enough for their intended use cases. This document tries to enumerate most important security controls and best practices you may want to keep in mind when developing your own solutions based on the framework.

## Storing setup.properties.last 

File `setup.properties.last` created under `/install/community-edition-setup/` directory during `setup.py` phase of initial installation contains sensitive data like credentials and keystore passwords. Though most of those items can still be retrieved from corresponding configuration files on disk - assuming an intruder has access to file system and knows where to look for them - there is no need to make their life easier. **Preserve the contents of the file as part of process of documenting your enviroment for future reference, while removing the original file inside container.**

## Apache config

As Apache works as a frontend web server in default setup, its configuration items found under `/etc/httpd/` (CentOS/RHEL) and `/etc/apache2/` (Ubuntu/Debian) directories inside container will greatly impact security of the whole instance. Next controls found within Gluu Server's virtual host's definition in `/etc/httpd/conf.d/https_gluu.conf` and `/etc/apache2/sites-enabled/https_gluu.conf` files, correspondingly, are of particular interest:

  - Enabled SSL/TLS cipher suites; depending on your requirements some of them may not be considered secure enough
  
  - "Content-Security-Policy" and "X-Frame-Options" clauses which are commented out by default; keep in mind those haven't been properly tested and default settings may need to be adjusted to be compatible with the current Gluu Server package
  
  - We recommend to block access to oxTrust web UI from public networks. This can be achieved, for example, by limiting access to a specific ip address/network range only, by updating corresponding "Location" directive in `/etc/httpd/conf.d/https_gluu.conf` (note that oxTrust also implements SCIM API thus you may need to include your SCIM-enabled apps there as well):
  
    ```
        <Location /identity>
                ProxyPass http://localhost:8082/identity retry=5 connectiontimeout=5 timeout=15
                Require ip 45.55.232.15
        </Location>
    ```

## 2FA to oxTrust

Consider enforcing 2FA for access to your oxTrust administrator interface of your instance. Gluu Server offers an assortment of 2FA methods out of the box in form of custom authentication scripts, like [Duo](https://gluu.org/docs/ce/3.1.3/authn-guide/duo/), [SuperGluu](https://gluu.org/docs/ce/3.1.3/authn-guide/supergluu/) or [FIDO U2F](https://gluu.org/docs/ce/3.1.3/authn-guide/U2F/).

## Enabled extensions

"Configuration -> Organization configuration" page contains several controls which may impact security of the instance if left enabled. Consider disabling them unless you intend to employ this functionality.

- "SCIM Support" - enables [SCIM protocol](https://gluu.org/docs/ce/3.1.4/user-management/scim2/) implementation which allows remote clients to conduct reads and writes of user data stored locally at the instance. Being a powerful tool for conducting user management-related batch jobs it may become as much powerful tool of destruction in possession of a malicious mind
- "Passport Support" - enabling passport opens a full new world of authentication methods' options, together with assosiated additional possibilities of them being exploited by a malicious user
- "Enabled" checkbox at "Configuration Manage -> Authentication -> CAS Protocol" - this control enables CAS protocol v2 implementation which comes pre-packaged with Shibboleth IDPv3 Gluu Server uses to offer support for SAML2 protocol. CAS is gradually phasing out nowdays and unless you must support some legacy services which still use it, you can rule out one potential attack vector by keeping it disabled.

## User registration

Gluu Server offers set of a basic user management features, which inlcude simplistic sign up feature. Generally, it's not recommended to employ those features in production unless there is no way around it at that moment. Otherwise, consider next:

- Make sure no scripts are enabled at "Configuration -> Manage Custom scripts -> User Registration" page
- Make sure that "Self-Service Password Reset" control at "Configuration -> Organization configuration" page is set to "Disabled"

## oxAuth / Authentication

oxAuth is at heart of Gluu Server framework, handling authentication for the rest of components. Its secureness is paramount for the integrity of the whole instance.

- Make sure only needed authentication scripts are enabled at "Configuration -> Manage Custom scripts -> Person Authentication". It's extremely important to disable any authentication method you don't consider secure enough (or needed) there, as otherwise a malicious third party may try to manipulate an user into using a less secure authentication method by pre-selecting it explicitly through adding "acr_values=" parameter to OIDC authorization request
- Consider enabling brute-force attack protection by setting "authenticationProtectionConfiguration" to "True" at "Configuration -> JSON Configuration -> oxAuth" page
- Review values chosen for "sessionIdUnusedLifetime" and "sessionIdLifetime" at "Configuration -> JSON Configuration -> oxAuth" page and make sure sessions won't last longer than an average user would need; longer living sessions present higher risks of session hijacking and unauthorized access from shared/public devices 
- Review configuration of oxAuth's inbulit filter implementing [CORS protocol](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) located in section "corsConfigurationFilters" at "Configuration -> JSON Configuration -> oxAuth". These controls dictate web services at which domains are expected to host on-page scripts which may generate requests to oxAuth API's endpoints - and thus should be allowed to access data send in responses to them. This is especially important if you as OP must support on-page OIDC clients employing implicit or hybrid flows. By default the filter will allow RPs at any domain the right to view the data.

## Open ports 

Make sure you don't have any services listening on external interfaces except for those that are absolutely required. In a basic standalone instance of Gluu Server 3.1.4, only Apache's listener at TCP port 443 is required to be open to the world. In previous versions of Gluu, OpenDJ listens on ports 4444 and 1636 for all interfaces. You can obtain a list of current listeners with `# netstat nlpt` (for TCP) and `# netstat -nlpu` (for UDP). In particular, make sure the internal LDAP server used by Gluu to store all its configuration data listens only at loopback interface.

In cases when listeners at external interfaces cannot be avoided (clustered setups be the most obvious example) we suggest to ensure that those ports will only be accessible from a very limited set of authorized peers by fine-tunining firewal rules and underlying network's topology

## Dynamic Client Registration

Consider whether you require support of [OpenID Connect Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html) in your setup and disable it otherwise by setting "dynamicRegistrationEnabled" to "False" at "Configuration -> JSON Configuration -> oxAuth" page.

In case you need this feature enabled, next controls must be re-visited to minimize potential exposure of your sensitive data:

- "trustedClientEnabled" and "dynamicRegistrationPersistClientAuthorizations" at "Configuration -> JSON Configuration -> oxAuth" - control whether clients are allowed to setup an entry for them in such way users won't be asked for consent on releasing their personal data while accessing corresponding RP
- "dynamicRegistrationScopesParamEnabled" at "Configuration -> JSON Configuration -> oxAuth" - controls whether clients are allowed to specify which scopes (out of set of default scopes - see below) they would like to receive from OP for users trying to access correponding RP
- list of scopes at "OpenID Connect -> Scopes", column "Allow for dynamic registration" - allows to quickly assess which scopes clients can potentially add to their registration entry without consent of OP's administrator; set "Allow for dynamic registration" property to "False" for all scopes you want to assign in a controlled fashion; in addition, make sure none of sensitive scopes have their type set to "Default" as scopes of that type will be automatically added to any dynamically enrolled client entry (**WHAT IS THE SYNERGY BETWEEN THOSE 2 FLAGS? WE NEED YURIY Z./JAVIER TO COMMENT ON THIS**)

## UMA

User Managed Access allows adopters to designate the task of making authorization decision to a dedicated 3rd party service capable of automatically handling requests to access a resource even without its owner being present online, following a set of rules defined for it. Needess to say such feature-rich framework can provide a lot of attack vectors for those seeking unauthorized access.

Next controls allow to fine-tune Gluu's UMA implementation's behaviour, allowing more secure interactions:

- "umaGrantAccessIfNoPolicies" at "Configuration -> JSON Configuration -> oxAuth" - allows access to a resource even if no policies are defined for the realted scopes; though it simplifies initial testing, we recommend to disabling this feature in production setups
- "umaRestrictResourceToAssociatedClient" at "Configuration -> JSON Configuration -> oxAuth" - won't allow any other client except the one which registered the resource initially to acquire a RPT for it; it's recommended to have it enabled for production setups

## Upgrades

Needless to say, keeping your instance up to date is paramount for maintaining its security. List of the latest vulnerabilities in the Gluu Server suite itself and corresponding patches can be found [here](https://gluu.org/docs/ce/3.1.4/upgrade/patches/). In addition,  updates should be conducted for all system components both inside and outside of container on regular basis (please note you must disable Gluu's repository before trying to updated any packages outside of container as described [here](https://gluu.org/docs/ce/3.1.3/installation-guide/install/#5-disable-gluu-repositories)):

  - For RHEL/CentOS distros, use `# yum update` inside and outside of container
  
  - For Ubuntu/Debian distros, use `# apt-get upgrade` or `# apt-get dist-upgrade` outside of container and `# apt-get upgrade` inside of it  ("apt-get dist-upgrade" is not safe to run inside container!)
  
## General security best practices still apply

Regardless of how specialized application is, general considerations still apply. This includes (but is not limited to):

  - Ensure physcial security of the machine where Gluu Server dwells, even if in a vastly virtualized world of today that term has become rather vague. Make sure booting from CD/DVD, External Devices, Floppy Drive is disabled in its BIOS and any physical (or "physical") I/O ports or devices (USB, FireWire, directly attached keyboard etc) are not accessible for un-authorized public
  - Minimize number of packages to minimize number of associated vulnerabilities (avoid installation of unnecessary packages and uninstall packages you don't need)
  - Make sure you use only highly secure means when accessing the server for administration purposes; using the most recent SSH server package is a no-brainer, we also suggest to configure it to deny login as a root user and disable password authentication (use public key instead), and move its listener to a port different from the standart TCP 22
  - Back up your system on regular basis; frequency may depend on data velocity and volume, but keep in mind that in case of a compromised system restoring from a backed up copy predating the incident may become the only option to ensure its integrity without losing months (even years) of work, and often a lot of time may pass since intrusion before security alarms will be triggered; keep in mind that backups on itself is a high priority target for potential intruder, and thus must be properly secured (locked up and/or encrypted); that includes controls of the system conducting back up as well to prevent manipulations with the state of the protected resource (i.e. to prevent restoring system to pre-patched state with a known vulnerability)

## Ongoing Security Audits

Even with all possible requirements met, regular security audits conducted by experienced security professionals are invaluable source of objective opinions on how secure your environment really is. Feel free to contact us at mailto:security@gluu.org with head-ups on any issues discovered during your internal investigations - we'll try our best to offer remediation instructions ASAP. We greatly appreciate your efforts in making Gluu products better and safer for everyone!
