# Introduction

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

The Gluu Server is an identity and access management suite comprised of
free open source software (FOSS) components. Some of the software was
written by Gluu (everything with an "ox" prefix, like "oxAuth"), and
some of the software we forked from existing open source projects like
the Shibboleth SAML identity provider, Forgerock community release of
OpenDJ, the Asimba SAML proxy, the CAS authentication server and many
more components that are part of the Linux distributions.

## History
Gluu was founded in 2009 by Mike Schwartz. After selling his ISP to
Verio in 1998, Mike advised many large companies on identity and access
management, directory services, and application security. In late 2008,
Mike had a hunch that Web single sign-on was too complex, too
proprietary and too expensive for many organizations. He felt that a
utility approach to SSO using open source software could provide an
alternative to expensive enterprise solutions. The Gluu Server was
envisioned as an integrated identity platform, based on free open source
software, to make application security available to significantly
greater number of organizations.([Read More](./history.md))

## Design Goals
At OSCON 2014, Gluu introduced easier to install packages for the Gluu
Server, and support for the Ubuntu Juju orchestration framework. The
goal of these distributions was to promote adoption of OX in the major
distributions of Linux...([Read More](./design.md))

## Architecture
There are several key components that make Gluu Server a reality and 
while choosing, the open-source softwares were given preference. Most 
of the components of the Gluu Server are written in Java, and
deployed as a web application in a J2EE servlet container.([Read More](./architecture.md))

## License
Any software published by Gluu in the OX Project is under the [MIT License](http://opensource.org/licenses/MIT).
The third party components have separate licenses.

|	Component	|	License	|
|-----------------------|---------------|
|	Shibboleth  |	[Apache2](http://www.apache.org/licenses/LICENSE-2.0)|
|	OpenDJ		|	[CDDL-1.0](http://opensource.org/licenses/CDDL-1.0)|
|	Asimba		|	[GNU APGL 3.0](http://www.gnu.org/licenses/agpl-3.0.html)|
|	Jagger		|	[MIT License](http://opensource.org/licenses/MIT)|

Note: Gluu maintains a fork of OpenDJ 3 in [our Github](https://github.com/GluuFederation/gluu-opendj3).
