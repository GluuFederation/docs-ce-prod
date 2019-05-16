# Architecture

Following is a list of the technical components that comprise the Gluu Server.

## J2EE Servlet container
Most of the components of the Gluu Server are written in Java, and
deployed as a web application in a J2EE servlet container. Java was
chosen because there is a wide array of high quality libraries,
convenient container services, and tools for managing high performance
applications at run-time. In order to run the Gluu Server, you don't
have to be a Java expert. But it does help to have some knowledge of how
Java applications are deployed and managed in tomcat, or a similar
servlet container.

## Apache HTTP front end web server
Although there are pros and cons, we think its best to use the Apache
HTTP server as the Internet facing Web server. There are a number of
Apache HTTP denial of service plugins. It is easier to handle re-directs
for things like discovery. And its convenient to have a non-J2EE way to
publish static content. ![Gluu Web
Communication](../img/design/gluu_http-tomcat_overview.png)

## LDAP for Persistence
LDAP was chosen for persistence for a number of reasons: (1) we understood
how to scale an LDAP directory service horizontally to accommodate a data set
of any size; (2) LDAP servers offer cost-effective and reliable replication
services; (3) as LDAP is a standard, the Gluu server would not be locked into
the persistence solution of one vendor; (4) LDAP had built-in support for SAML
and OAuth2 components. In the future the OX project may develop additional
persistence backends. But this is not likely for the near-term.

## Web container plugins
Today, Web access management tools like CA Siteminder predominantly use
the web agent approach. Many large organizations have hundreds or
thousands of "web agents" running on Apache and IIS.

Web agents are a great approach. Programmers don't have to know much
about the protocols. System administrators can configure the web server
to use the central authorization server so we don't have to rely on the
programmers to get security right. The programmers can obtain the user
session information in the environment variables. In OAuth2 information
is serialized using JSON. For example, the entire id_token JWT is sent
in one environment variable.

If developers want even more control, they can use the Gluu Server's
API's directly: SAML, OpenID Connect, or UMA.

