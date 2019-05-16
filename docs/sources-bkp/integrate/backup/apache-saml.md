# Apache SAML

## Configuring Apache Shibboleth SP in CentOS

### System Preparation

__Add Shibboleth repository for CentOS__

* The file `shib.repo` contains the following entry:

```
[security_shibboleth]
name=Shibboleth (CentOS_CentOS-6)
type=rpm-md
baseurl=http://download.opensuse.org/repositories/security:/shibboleth/CentOS_CentOS-6/
gpgcheck=1
gpgkey=http://download.opensuse.org/repositories/security:/shibboleth/CentOS_CentOS-6/repodata/repomd.xml.key
enabled=1
```

* Download the Shibboleth security repo key from here:

```
http://download.opensuse.org/repositories/security:/shibboleth/CentOS_CentOS-6/security:shibboleth.repo
```

### Shibboleth SP Installation

To install the Shibboleth SP, run the following commands in a terminal:

```
# yum install shibboleth
# service shibd start
# chkconfig shibd on
```

### Install and Configure httpd
#### Installation

The following commands will both install, and start the Apache web
server on your machine/Linux environment:

```
# yum install httpd
# service httpd start
# service iptables stop 
```

#### Configuration

Edit the file `httpd.conf`, and do the following changes:

* Change the `ServerName` directive to the server name of the SP.

* Set `UseCanonicalName On`.

* Restart the httpd service using the command `service httpd restart`.

#### Httpd Testing

* Create an `index.html` file inside the directory `/var/www/html`.

* Restart the httpd service using the command `service httpd restart`.

* Check from your browser if the file `index.html` is visible.

#### SP Key Certificate

* Create both a private key, and a certificate, and place those in the
  file `/etc/shibboleth`.

* Change the permissions of these files so that the web server can read
  the files.

### Shibboleth SP Configuration

This section describes how to configure the file `shibboleth2.xml`.

* Provide the `entityID` of the according SP in:
	
	* `<ApplicationDefaults entityID="http://sp.example.org/Shibboleth"> section`

* Provide the `entityID` of the IdP in:

	* `<SSO entityID="https://idp.gluu.org/idp/shibboleth"> section`

* Adjust the entry of the metadata provider. In most cases this is the
  Gluu IdP metadata link:

	* `<MetadataProvider type="XML" uri="https://idp.gluu.org/idp/shibboleth"> section`

* Provide both the key and certificate of the SP in:

	* `<CredentialResolver type="File" key="spkey.key" certificate="spcrt.crt"> section`

### Shibboleth Manual Configuration (one Physical SP):

* Create a directory named under `/var/www/secure`.

* Change the permissions for that directory `secure` to
  `apache:apache` (owner and group of the web server).

* `httpd.conf`

	* change the ServerName `<hostname_of_server>`

	* Define the Location, and the authorization type:

		```
		<Location /secure>
			AuthType shibboleth
			ShibRequestSetting requireSession 1
			ShibUseHeaders on
			Require valid-user
		</Location>
		```

* configure `shibboleth2.xml`

	* Set the EntityID of the SP: `ApplicationDefaults entityID="http://hostname/secure"`

	* Provide the EntityID of the IDP: `SSO entityID="https://idp.gluu.org/idp/shibboleth"`

	* Set both the Metadata Provider, and the IDP: `MetadataProvider type="XML" uri="https://idp.gluu.org/idp/shibboleth"`

* Restart both shibd and Apache2 using these lines:

```
service shibd restart
service httpd restart
```

* Create a Trust Relationship for this SP in your desired IdP.