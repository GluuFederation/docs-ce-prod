# Certificates 
Many of the components of the Gluu Server have cryptographic keys and
X.509 certificates. There are many key formats, and keystore formats.
Navigate to the sections below to find what you need for each of the

## Asimba
`asimba.crt`, `asimba.csr`, `asimba.key`, `asimba.key.orig`,
`asimba.pkcs12` and `asimbaIDP.jks` are associated with the
Asimba SAML Proxy Server. If you install the server 
in your Gluu Server, you have to deal with these certificates
and keys.

## Apache
`httpd.crt`, `httpd.csr`, `httpd.key`, `httpd.key.orig` are Apache SSL
related certificates and keys. If you want to update your Apache SSL
certificate do not worry about the file extension `.csr` and `.key.orig`.

### Updating Apache Certificate
If you are using the Gluu Server CE binaries or latest Gluu Servers, you
need to manually update certificates and keys from the file
`/etc/certs/`. Please note that your private key cannot be password
protected, and the public key should be base64 X.509. It's recommended to
backup your full `/etc/certs` directory and `cacerts` file before
proceeding, as well as to remove previous versions of certificates
you are about to update from the `cacerts` storage.

For example, follow these steps in order to update the Apache SSL cert:

- save both the latest SSL httpd key and certificate in the file 
  `/etc/certs`.
- rename them to `httpd.key` and `httpd.crt`, respectively.
- import 'httpd.der' into java keystore
  - Convertion to DER, command: `openssl x509 -outform der -in httpd.crt -out httpd.der`
  - Import this DER into java keystore (cacerts), command: `keytool -importcert -file httpd.der -keystore cacerts -alias <hostname_of_your_Gluu_Server>_httpd`
- restart LDAP server, apache2/httpd and tomcat.

You may find more info on certificates Gluu CE uses, as well as detailed steps to update them, in [this article](../operation/update-certificate.md)

### Installing Intermediate Certificates

To install intermediate certificates follow these steps:

1. Log into your Gluu Server container.
2. Keep your intermediate certificate in the file `/etc/certs/`.
3. Modify `/etc/httpd/conf.d/https_gluu.conf`, and add
   `SSLCertificateChainFile /etc/certs/name_of_your_interm_root_cert.crt`.
4. Restart the service of the httpd server.

## OpenDJ
`opendj.crt` is the public certificate being used by oxAuth to make a
connection to the internal Gluu-LDAP.

## oxAuth
`oxauth-web-keys.json` is being used by Gluu's OpenID Connect & UMA
server.

## Shibboleth IDP
`shibIDP.crt`, `shibIDP.csr`, `shibIDP.jks`, `shibIDP.key`,
`shibIDP.key.orig`, `shibIDP.pkcs12` are required if you use the Gluu
Server's Shibboleth SAML server for SAML transactions.
