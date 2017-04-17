# Gluu Server Logs

When it comes to troubleshooting issues in the Gluu Server--from service hiccups to outages--logs are the best place to start. 

The Gluu Server administrator can investigate logs from the oxTrust [View Logs](../oxtrust/configuration.md/#view-log-file) feature or directly with SSH access to the Gluu-Server container. 

Gluu Server logs can be found in the following locations:

## Log Levels
Gluu Server logs use the log4j logging levels which can be changed in the `log4j.xml` file under the `/opt/tomcat/webapps/oxauth/WEB-INF/classes` folder.
The available logging levels are :

|Level|Description|
|-----|-----------|
|ALL|All log levels are documented|
|DEBUG|Detailed events useful to debug application|
|ERROR|Errors are documented|
|INFO|Logs informational messages as the application runs|
|OFF|No logs are recorded|
|TRACE|Logs detailed events; more than DEBUG|

As mentioned above the `log4j.xml` contains the log levels. Open the file using the command below

```
# vi /opt/tomcat/webapps/oxauth/WEB-INF/classes/log4j.xml
```

The log leves are defined under the ` <level value=" " />` tags which can be changed to one of the above from the table. The following section is taken from a live Gluu Server `log4j.xml` file showing different log levels for different logs. The changes made this section will reflect in the logs.
```
 <logger name="org.xdi.oxauth.service.status.ldap" additivity="false">
        <level value="INFO"/>
        <appender-ref ref="OX_PERSISTENCE_LDAP_STATISTICS_FILE" />
    </logger>

    <logger name="org.xdi.service.PythonService" additivity="false">
        <level value="INFO"/>
        <appender-ref ref="OX_SCRIPT_LOG_FILE" />
    </logger>

    <logger name="org.xdi.service.custom.script" additivity="false">
        <level value="INFO"/>
        <appender-ref ref="OX_SCRIPT_LOG_FILE" />
    </logger>

    <logger name="org.xdi.oxauth.service.custom" additivity="false">
        <level value="TRACE"/>
        <appender-ref ref="OX_SCRIPT_LOG_FILE" />
    </logger>
```

Please restart `tomcat` after any change in log levels to allow the changes to take effect. Use the following command to restart tomcat:

```
# service tomcat restart
```
#### System logs 
- For Ubuntu: `/var/log/syslog`
- For RPM based systems: `/var/log/messages`

#### Web Server logs
- For Debian: `/var/log/apache2/`
- For RPM based systems: `/var/log/httpd/`

#### Core Gluu Server logs
- `opt/tomcat/logs/`

#### SAML transaction related logs
- `/opt/idp/logs/`

#### LDAP logs
- `/opt/opendj/logs/`

#### Miscellaneous logs
- `/var/logs/`

#### To escalate the log levels
- OpenID Connect or any core logging: `log4j.xml`, which is located in `/opt/tomcat/webapps/oxauth/WEB-INF/classes/`
- SAML logging: `logging.xml`, which is located in `/opt/idp.conf/`

## System Logs

Sometimes it worthy to check system logs like `/var/log/messages`. These logs contain global system messages.

## Web Server logs

Apache httpd / apache2 logs are available in `/var/log/httpd` or `/var/log/apache2` for Ubuntu.

1. `access_log`: This log contains information about requests coming into the Gluu Server, success status or requests, execution time for any request etc.     

2. `error_log`: This log shows error messages if the web server encounter any issue while processing incoming requests.    

3. `other_vhosts_access.log`: This log is specific to the Gluu Server setup and those links which are being requested by a user from a web browser. An example below:     

        test.gluu.org:443 192.168.201.184 - - [17/Jul/2016:18:25:21 +0000] "GET /index.html HTTP/1.1" 200 13239 "-" "Java/1.7.0_95"
        test.gluu.org:443 192.168.201.1 - - [17/Jul/2016:18:25:56 +0000] "GET / HTTP/1.1" 302 2185 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        test.gluu.org:443 192.168.201.1 - - [17/Jul/2016:18:25:56 +0000] "GET /identity/ HTTP/1.1" 200 583 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        test.gluu.org:443 192.168.201.1 - - [17/Jul/2016:18:25:56 +0000] "GET /identity/home.htm HTTP/1.1" 302 272 "https://test.gluu.org/identity/" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        test.gluu.org:443 192.168.201.1 - - [17/Jul/2016:18:25:56 +0000] "GET /identity/login?cid=4 HTTP/1.1" 302 474 "https://test.gluu.org/identity/" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        test.gluu.org:443 192.168.201.1 - - [17/Jul/2016:18:25:56 +0000] "GET /oxauth/authorize?scope=openid+profile+email+user_name&response_type=code+id_token&nonce=nonce&redirect_uri=https%3A%2F%2Ftest.gluu.org%2Fidentity%2Fauthentication%2Fauthcode&client_id=%40%21EFCB.890F.FB6C.2603%210001%210A49.F454%210008%21F047.7275 HTTP/1.1" 302 450 "https://test.gluu.org/identity/" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36" 

4. There are few other logs like `ssl_access_log` , `ssl_error_log` , and `ssl_request_log` which are collecting information on port 443 specifically.      

Remember the initial `GET` request will hit the Apache server first, and then be proxied via the AJP port 8009 to tomcat. If you see traffic on the web server, but not on tomcat, this is a good place to check to see if something is wrong. For example, you might want to check if the firewall is blocking port 8009 if you see somthing like this:

        [Thu Jul 14 23:49:19 2016] [error] ajp_read_header: ajp_ilink_receive failed
        [Thu Jul 14 23:49:19 2016] [error] (70007)The timeout specified has expired: proxy: read response failed from (null) (localhost)
        [Thu Jul 14 23:49:20 2016] [error] (70007)The timeout specified has expired: ajp_ilink_receive() can't receive header
        [Thu Jul 14 23:49:20 2016] [error] ajp_read_header: ajp_ilink_receive failed
        [Thu Jul 14 23:49:20 2016] [error] (70007)The timeout specified has expired: proxy: read response failed from (null) (localhost)
        [Thu Jul 14 23:49:20 2016] [error] (70007)The timeout specified has expired: ajp_ilink_receive() can't receive header
        [Thu Jul 14 23:49:20 2016] [error] ajp_read_header: ajp_ilink_receive failed
        [Thu Jul 14 23:49:20 2016] [error] (70007)The timeout specified has expired: proxy: read response failed from (null) (localhost)

## Core logs

### oxAuth logs

1. `oxauth.log`      
This log is gathering most of the authentication related information. Generally this is the first log to review for any authentication-related troubleshooting, like authentication failure or missing clients etc. Here's an example showing a successful user authentication:

        2016-07-16 15:43:28,232 INFO  [org.xdi.oxauth.auth.Authenticator] Authentication success for Client: '@!EFCB.890F.FB6C.2603!0001!0A49.F454!0008!F047.7275'
        2016-07-16 15:43:28,232 TRACE [org.xdi.oxauth.auth.Authenticator] Authentication successfully for '@!EFCB.890F.FB6C.2603!0001!0A49.F454!0008!F047.7275'
        2016-07-16 15:43:28,238 DEBUG [xdi.oxauth.token.ws.rs.TokenRestWebServiceImpl] Attempting to request access token: grantType = authorization_code, code = 61ba3c0d-42c4-4f1f-8420-fd5f6707f1b1, redirectUri = https://test.gluu.org/identity/authentication/authcode, username = null, refreshToken = null, clientId = null, ExtraParams = {grant_type=[Ljava.lang.String;@1add2a62, redirect_uri=[Ljava.lang.String;@2e0995b5, code=[Ljava.lang.String;@7743b5af}, isSecure = true, codeVerifier = null
        2016-07-16 15:43:28,249 DEBUG [org.xdi.oxauth.service.UserService] Getting user information from LDAP: userId = zico 

2. `oxauth_script.log`     
Most of the custom script's initialization and few more information are loaded here in this script. In the sample log below we can see 'Super Gluu' 2FA has been loaded in the Gluu Server:

        2016-07-16 19:06:32,705 INFO  [org.xdi.service.PythonService] (pool-2-thread-2) oxPush2. Initialization
        2016-07-16 19:06:32,713 INFO  [org.xdi.service.PythonService] (pool-2-thread-2) oxPush2. Initialize notification services
        2016-07-16 19:06:32,750 INFO  [org.xdi.service.PythonService] (pool-2-thread-2) oxPush2. Initialized successfully. oneStep: 'False', twoStep: 'True', pushNotifications: 'False'

### oxTrust logs

1. `oxtrust.log`     
This log gather logs related to Gluu Server Admin panel (called oxTrust). For example, what is the clientID of an oxTrust session? Or, what scopes are being used, etc. In the example below, you can see an admin user has successfuly logged into the `test.gluu.org` Gluu Server admin panel, has the proper authorizationCode, a redirectURI, and the user's role:

        2016-07-16 16:41:55,690 INFO  [org.gluu.oxtrust.action.Authenticator] authorizationCode : 555a7586-6ca2-4b39-ab39-2ac78ec81524
        2016-07-16 16:41:55,690 INFO  [org.gluu.oxtrust.action.Authenticator]  scopes : user_name email openid profile
        2016-07-16 16:41:55,691 INFO  [org.gluu.oxtrust.action.Authenticator] clientID : @!EFCB.890F.FB6C.2603!0001!0A49.F454!0008!F047.7275
        2016-07-16 16:41:55,691 INFO  [org.gluu.oxtrust.action.Authenticator] getting accessToken
        2016-07-16 16:41:55,691 INFO  [org.gluu.oxtrust.action.Authenticator] tokenURL : https://test.gluu.org/oxauth/seam/resource/restv1/oxauth/token
        2016-07-16 16:41:55,691 INFO  [org.gluu.oxtrust.action.Authenticator] Sending request to token endpoint
        2016-07-16 16:41:55,692 INFO  [org.gluu.oxtrust.action.Authenticator] redirectURI : https://test.gluu.org/identity/authentication/authcode
        2016-07-16 16:41:55,919 DEBUG [org.gluu.oxtrust.action.Authenticator]  tokenResponse : org.xdi.oxauth.client.TokenResponse@1914b8d
        2016-07-16 16:41:55,920 DEBUG [org.gluu.oxtrust.action.Authenticator]  tokenResponse.getErrorType() : null
        2016-07-16 16:41:55,921 DEBUG [org.gluu.oxtrust.action.Authenticator]  accessToken : d39bd11c-7bc0-45e1-b772-2d0a5f74e6fb
        2016-07-16 16:41:55,921 DEBUG [org.gluu.oxtrust.action.Authenticator]  validating AccessToken
        2016-07-16 16:41:56,004 DEBUG [org.gluu.oxtrust.action.Authenticator]  response3.getStatus() : 200
        2016-07-16 16:41:56,004 DEBUG [org.gluu.oxtrust.action.Authenticator] validate check session status:200
        2016-07-16 16:41:56,004 INFO  [org.gluu.oxtrust.action.Authenticator] Session validation successful. User is logged in
        2016-07-16 16:41:56,108 INFO  [org.gluu.oxtrust.action.Authenticator] user uid:admin
        2016-07-16 16:41:56,119 INFO  [org.gluu.oxtrust.action.Authenticator] Authenticating user 'admin'
        2016-07-16 16:41:56,125 DEBUG [org.gluu.oxtrust.action.Authenticator] Configuring application after user 'admin' login 

2. `oxtrust_script.log`     
This log collects information on oxTrust related scripts and their operations. For example, if an organization uses a custom attribute which populates values for every user, then the Gluu Server Administrator needs to use a custom script for their 'Cache Refresh' process. This log will receive information when the custom script runs.

3. `oxtrust_cache_refresh.log`    
Cache Refresh related information is available here, such as Status, Primary failure etc. In the sample snippet below we are seeing the status of users that have been synced into Gluu Server, number of failures, and total number of updated users.

        2016-07-16 17:18:17,691 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Updated person '@!EFCB.890F.FB6C.2603!0001!0A49.F454!0000!40EB.AB8E'
        2016-07-16 17:18:17,691 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Updated '2,002' entries
        2016-07-16 17:18:17,722 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Failed to update '0' entries
        2016-07-16 17:18:17,738 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Keep external persons: 'true'
        2016-07-16 17:18:17,739 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Count entries '0' for removal from target server
        2016-07-16 17:18:17,739 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Removed '0' persons from target server
        2016-07-16 17:18:17,739 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) There are '2,002' entries before updating inum list
        2016-07-16 17:18:17,740 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) There are '2,002' entries after removal '0' entries 

### Wrapper logs

1. `catalina.log`    
A standard servlet contianer log. For example: 

        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view.
        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view.
        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view.
        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view.
        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view.
        Jul 16, 2016 7:06:26 PM com.sun.faces.renderkit.html_basic.HtmlBasicRenderer getForComponent
        WARNING: Unable to find component with ID j_idt244 in view. 

2. `localhost.log`     
Standard logs on web applications. For example: 

        Jul 16, 2016 3:33:31 PM org.apache.catalina.core.ApplicationContext log
        INFO: Closing Spring root WebApplicationContext
        Jul 16, 2016 3:33:32 PM org.apache.catalina.core.ApplicationContext log
        INFO: Closing Spring root WebApplicationContext
        Jul 16, 2016 3:37:27 PM org.apache.catalina.core.ApplicationContext log
        INFO: Initializing Spring root WebApplicationContext
        Jul 16, 2016 3:37:42 PM org.apache.catalina.core.ApplicationContext log
        INFO: No Spring WebApplicationInitializer types detected on classpath
        Jul 16, 2016 3:37:43 PM org.apache.catalina.core.ApplicationContext log
        INFO: Initializing Spring root WebApplicationContext
        Jul 16, 2016 3:37:54 PM org.apache.catalina.core.ApplicationContext log
        INFO: Initializing Spring FrameworkServlet 'cas' 

3. `wrapper.log`     
This log is the godfather of all Gluu Server logs, accounting for roughly 95% of log information. As you can see in the example snippet below, this log is showing that one CAS module loaded, one user is trying to authenticate, there's a search happening for this user in LDAP, etc.:

        INFO   | jvm 1    | 2016/07/16 19:17:48 | 2016-07-16 19:17:48,855 INFO [org.jasig.cas.services.DefaultServicesManagerImpl] - <Reloading registered services.>
        INFO   | jvm 1    | 2016/07/16 19:17:48 | 2016-07-16 19:17:48,855 INFO [org.jasig.cas.services.DefaultServicesManagerImpl] - <Loaded 1 services.>
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,835 TRACE [org.xdi.oxauth.service.SessionStateService] Found session_state cookie: '2f73dc6e-7421-48ff-9b49-7c59565bfe50'
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,838 TRACE [org.xdi.oxauth.service.SessionStateService] Try to get session by id: 2f73dc6e-7421-48ff-9b49-7c59565bfe50 ...
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,838 TRACE [org.xdi.oxauth.service.SessionStateService] Session dn: uniqueIdentifier=2f73dc6e-7421-48ff-9b49-7c59565bfe50,ou=session,o=@!EFCB.890F.FB6C.2603!0001!0A49.F454,o=gluu
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,839 DEBUG [org.xdi.oxauth.service.external.ExternalAuthenticationService] Executing python 'authenticate' authenticator method
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,840 DEBUG [org.xdi.oxauth.service.AuthenticationService] Authenticating user with LDAP: username: support@gluu.org
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,840 DEBUG [org.xdi.oxauth.service.AuthenticationService] Attempting to find userDN by primary key: 'mail' and key value: 'support@gluu.org'
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,840 DEBUG [org.xdi.oxauth.service.AuthenticationService] Getting user information from LDAP: attributeName = 'mail', attributeValue = 'support@gluu.org'
        INFO   | jvm 1    | 2016/07/16 19:17:51 | 2016-07-16 19:17:51,844 DEBUG [org.xdi.oxauth.service.AuthenticationService] Found '2' entries 

### Cache Refresh logs

1. `oxtrust_cache_refresh.log`     

Cache Refresh related information such as status, primary failure, etc., is available in this log. In the sample snippet below we see the total number of users that have been synced into the Gluu Server, number of failures, and total number of updated users. 

        2016-07-16 17:18:17,691 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Updated person '@!EFCB.890F.FB6C.2603!0001!0A49.F454!0000!40EB.AB8E'
        2016-07-16 17:18:17,691 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Updated '2,002' entries
        2016-07-16 17:18:17,722 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Failed to update '0' entries
        2016-07-16 17:18:17,738 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Keep external persons: 'true'
        2016-07-16 17:18:17,739 DEBUG [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Count entries '0' for removal from target server
        2016-07-16 17:18:17,739 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) Removed '0' persons from target server
        2016-07-16 17:18:17,739 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) There are '2,002' entries before updating inum list
        2016-07-16 17:18:17,740 INFO  [gluu.oxtrust.ldap.cache.service.CacheRefreshTimer] (pool-1-thread-9) There are '2,002' entries after removal '0' entries 

### CAS logs

1. `cas.log`    

If oxCAS is enabled in the Gluu Server then this log will have information about any CAS transactions. In the example snippet below, we see a CAS service validate a response from the Gluu Server:

        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.web.ServiceValidateController] - Successfully validated service ticket ST-237741-1LZ4eWcHvBS75FAXTICY-myldap.gluu.org for service [https://testcas1.gluu.org/c?pkg=https://testcas1.gluu.org/portal.p_redirect]
        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.support.saml.authentication.principal.SamlService] - Attempted to extract Request from HttpServletRequest. Results:
        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.support.saml.authentication.principal.SamlService] - Request Body:
        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.support.saml.authentication.principal.SamlService] - Extracted ArtifactId: null
        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.support.saml.authentication.principal.SamlService] - Extracted Request Id: null
        2016-07-16 15:50:39,211 DEBUG [org.jasig.cas.support.saml.web.support.SamlArgumentExtractor] - Extractor generated service for: https://testcas1.gluu.org/c/?pkg=https://testcas1.gluu.org/portal.p_redirect
        2016-07-16 15:50:41,878 DEBUG [org.jasig.cas.web.support.CasArgumentExtractor] - Extractor generated service for: https://testcas1.gluu.org/c/
        2016-07-16 15:50:41,880 DEBUG [org.jasig.cas.ticket.registry.MemCacheTicketRegistry] - Updating ticket ST-237742-beBEaYMCtoiRJBCYJLKt-myldap.gluu.org
        2016-07-16 15:50:41,882 DEBUG [org.jasig.cas.services.support.RegisteredServiceDefaultAttributeFilter] - Found attribute [uid] in the list of allowed attributes for service [zico]
        2016-07-16 15:50:41,882 DEBUG [org.jasig.cas.services.support.RegisteredServiceDefaultAttributeFilter] - Found attribute [sn] in the list of allowed attributes for service [mohib]
        2016-07-16 15:50:41,882 DEBUG [org.jasig.cas.CentralAuthenticationServiceImpl] - Principal id to return for service [mohib zico] is [mzico]. The default principal id is [mzico].
        2016-07-16 15:50:41,883 DEBUG [org.jasig.cas.ticket.registry.MemCacheTicketRegistry] - Deleting ticket         ST-237742-beBEaYMCtoiRJBCYJLKt-myldap.gluu.org
        2016-07-16 15:50:41,884 INFO [com.github.inspektr.audit.support.Slf4jLoggingAuditTrailManager] - Audit trail record BEGIN
        =============================================================
        WHO: audit:unknown
        WHAT: ST-237742-beBEaYMCtoiRJBCYJLKt-myldap.gluu.org
        ACTION: SERVICE_TICKET_VALIDATED
        APPLICATION: CAS
        WHEN: Sat Jul 16 15:50:41 EDT 2016
        CLIENT IP ADDRESS: 192.168.1.2
        SERVER IP ADDRESS: test.gluu.org
        ============================================================= 

### Asimba logs 

1. `wrapper.log`     

Any Asimba SAML proxy transactions are logged in `wrapper.log`. In the below example we see the requestor (from where the SSO request is coming), we see the SAML proxy server's information (`test.gluu.org`), and the authentication server (`nest.gluu.org`) which is performing the authentication, releasing attributes, etc. 

        INFO   | jvm 1    | 2016/07/17 15:40:33 | (ASIMBAWA) [2016-07-17 15:40:33] [DEBUG] WebBrowserSSO <?xml version="1.0" encoding="UTF-8"?>
        INFO   | jvm 1    | 2016/07/17 15:40:33 | <samlp:AuthnRequest
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     AssertionConsumerServiceURL="https://sp.gluu.org/Shibboleth.sso/SAML2/POST"
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     Destination="https://test.gluu.org/asimba/profiles/saml2/sso/web"
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     ID="_a5704abd6d2f2e5b0eba5a1671f6c658"
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     IssueInstant="2016-07-17T15:40:33Z"
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     Version="2.0" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">https://sp.gluu.org/shibboleth</saml:Issuer>
        INFO   | jvm 1    | 2016/07/17 15:40:33 |     <samlp:NameIDPolicy AllowCreate="1"/>
        INFO   | jvm 1    | 2016/07/17 15:40:33 | </samlp:AuthnRequest>
        INFO   | jvm 1    | 2016/07/17 15:40:33 |
        INFO   | jvm 1    | 2016/07/17 15:40:33 | (ASIMBAWA) [2016-07-17 15:40:33] [DEBUG] WebBrowserSSO Put on map? urlpath.context=web 
        ......................
        ......................
        ......................
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] WebBrowserSSOProfile Request recieved: https://test.gluu.org/asimba/sso/web
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] SAML2IDP Creating new MetadataProvider from configured source for SAML2 IDP 'https://nest.gluu.org/idp/shibboleth'
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [INFO] NamedFilesystemMetadataProvider Created for file with name /opt/tomcat/webapps/asimba/WEB-INF/sample-data/idp/2185528996791210207.xml
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [INFO] AbstractReloadingMetadataProvider New metadata succesfully loaded for '/opt/tomcat/webapps/asimba/WEB-INF/sample-data/idp/2185528996791210207.xml'
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [INFO] AbstractReloadingMetadataProvider Next refresh cycle for metadata provider '/opt/tomcat/webapps/asimba/WEB-INF/sample-data/idp/2185528996791210207.xml' will occur on '2016-07-17T18:40:37.746Z' ('2016-07-17T18:40:37.746Z' local time)
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] StandardMetadataProviderManager No EntitiesDescriptor was returned, so no IDPList to create.
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] WebBrowserSSOProfile Using binding: urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] SAML2IDP Returning existing MetadataProvider for SAML2 IDP 'https://nest.gluu.org/idp/shibboleth'
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [INFO] MemorySessionFactory Existing session(s) updated: fQUnP-s1K_fdxK2wdLjp4A for requestor 'https://sp.gluu.org/shibboleth'
        INFO   | jvm 1    | 2016/07/17 15:40:37 | (ASIMBAWA) [2016-07-17 15:40:37] [DEBUG] AbstractAuthNMethodSAML2Profile <?xml version="1.0" encoding="UTF-8"?>
        INFO   | jvm 1    | 2016/07/17 15:40:37 | <saml2p:AuthnRequest AssertionConsumerServiceIndex="0"
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     Destination="https://nest.gluu.org/idp/profile/SAML2/POST/SSO"
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     ForceAuthn="false"
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     ID="_ee01f578f94409aa41af080cc74787b8fQUnP-s1K_fdxK2wdLjp4A"
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     IssueInstant="2016-07-17T15:40:37.771Z" ProviderName="Sp.gluu.org"
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     Version="2.0" xmlns:saml2p="urn:oasis:names:tc:SAML:2.0:protocol">
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     <saml2:Issuer xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">https://test.gluu.org/asimba/profiles/saml2</saml2:Issuer>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |     <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        INFO   | jvm 1    | 2016/07/17 15:40:37 |         <ds:SignedInfo>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |             <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |             <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |             <ds:Reference URI="#_ee01f578f94409aa41af080cc74787b8fQUnP-s1K_fdxK2wdLjp4A">
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                 <ds:Transforms>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                     <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                     <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                 </ds:Transforms>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                 <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |                 <ds:DigestValue>okTsHKhXes6hA7cKbLjsBwFZhtM=</ds:DigestValue>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |             </ds:Reference>
        INFO   | jvm 1    | 2016/07/17 15:40:37 |         </ds:SignedInfo>
        ............................INFO   | jvm 1    | 2016/07/17 15:40:56 |             <saml2:Attribute FriendlyName="uid"
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                 Name="urn:oid:0.9.2342.19200300.100.1.1" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                 <saml2:AttributeValue
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">admin</saml2:AttributeValue>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |             </saml2:Attribute>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |             <saml2:Attribute FriendlyName="sn" Name="urn:oid:2.5.4.4" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                 <saml2:AttributeValue
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">User</saml2:AttributeValue>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |             </saml2:Attribute>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |             <saml2:Attribute FriendlyName="givenName"
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                 Name="urn:oid:2.5.4.42" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                 <saml2:AttributeValue
        INFO   | jvm 1    | 2016/07/17 15:40:56 |                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">Admin</saml2:AttributeValue>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |             </saml2:Attribute>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |         </saml2:AttributeStatement>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |     </saml2:Assertion>
        INFO   | jvm 1    | 2016/07/17 15:40:56 | </saml2p:Response>
        INFO   | jvm 1    | 2016/07/17 15:40:56 |

## SAML logs

1. `idp-access.log`     
Each time the IDP is accessed a log entry is made detailing whether or not information sent back. These messages include request time, remote host making the rreuqest, server host name and port, and the request path. This log is written in the machine parsable format:

        20160717T162519Z|192.168.201.1|test.gluu.org:443|/profile/SAML2/Redirect/SSO|

2. `idp-process.log`    
This is one of the most important logs for SAML transactions in the Gluu Server. It includes the Issuer's information, released attributes, certificate information etc. Here's an example: 

         <?xml version="1.0" encoding="UTF-8"?>
        <saml2p:Response
            Destination="https://sp.gluu.org/Shibboleth.sso/SAML2/POST"
            ID="_322f0ff5e516e8ecb3b7ecd21aaf457c"
            InResponseTo="_a05a4d01389b7904c7e4d40a4d099285"
            IssueInstant="2016-07-17T16:25:19.165Z" Version="2.0" xmlns:saml2p="urn:oasis:names:tc:SAML:2.0:protocol">
            <saml2:Issuer
                Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity" xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">https://test.gluu.org/idp/shibboleth</saml2:Issuer>
            <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                <ds:SignedInfo>
        ...................
        ...................
        ...................
        eLiXH2CuvJrwkHhcSQSyKAs4WPXbLE5hhzEd9GGRmiovGmdZJvDU5zRX74m80GcL0d+mf6WzLRZBVmcPcs/2Dk1+J2Sw67W0DF0vgpoDvhgKHMdkKI8Ex
        Z38cVHo1xJqpQvUq0StjGPgdRBWUJoMe4BVRD8sM7BDbjFoY5H3TJxzYbnjsxwDZaqIZQt+4=</xenc:CipherValue>
                    </xenc:CipherData>
                </xenc:EncryptedData>
            </saml2:EncryptedAssertion>
        </saml2p:Response>

        16:25:19.395 - INFO [Shibboleth-Audit:1028] - 20160717T162519Z|urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect|_a05a4d01389b7904c7e4d40a4d099285|https://sp.gluu.org/shibboleth|urn:mace:shibboleth:2.0:profiles:saml2:sso|https://test.gluu.org/idp/shibboleth|urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST|_322f0ff5e516e8ecb3b7ecd21aaf457c|admin|urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport|uid,mail,sn,givenName,||| 

## LDAP logs

1. `access.log`     
`access.log` is in active mode all the time. The `access.log` messages provide information about the types of LDAP operations processed by the Gluu Server.

2. `audit.log`    
All changes / modifications of LDAP server are being logged here in audit log.

3. `errors.log`    
LDAP server startup and shutdown related information are available in `errors.log`.
