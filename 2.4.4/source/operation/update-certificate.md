#Update Certificate

## Procedure for manually updating certificates of a live Gluu CE instance.

This page describes how to manually update SSL/TLS certificates used by different components of Gluu CE instance. Ubuntu-based container's environment will be used for all command examples, if not stated otherwise explicitly. Commands may differ slightly for other distro families.

## Before you start changing anything

Backup all your current certificates, keys and java key storages that may be affected:

1. Log into your instance: `# service gluu-server-2.4.3 login`
(if you use Gluu CE older than 2.4 you should update to current version)
2. Backup everything under `/etc/certs/` directory, then also backup your container's default java key storage (`cacerts` file); it can be located under `/etc/ssl/certs/java/` for Ubuntu- and Debian-based container, and under `/etc/pki/java/` for CentOS- and RHEL-based containers. It also usually has symbolic link insalled for it, which is the same for both families: `/usr/java/latest/lib/security/cacerts`

Note: In order to have the new cert used for anything in oxtrust, i.e. anything hitting `/identity` and `/oxauth`, you only need to follow the instructions for [updating the Apache web server](#apache-web-server-certificate-update-process).

## Default JVM Keystore

Java programs making SSL connections to an external server may use the default JVM truststore, `/usr/java/latest/lib/security/cacerts`, to establish trust for certificates they are presented with. During installation, `setup.py` generates self-signed certificates for all components and adds them to the `cacerts` truststore.

## Apache Web Server Certificate Update Process

This is a common task. Before you launch your production Gluu Server, you may want to install a certificate from a well known certification authority like Verisign or Godaddy. Also, Web SSL certificates usually expire each year. To import it into Gluu CE:

1. Log into your instance: `# service gluu-server-2.4.3 login`
    (if you use Gluu CE older than 2.4.x you should update to current version)
2. Create a file containing full set of all intermediary CA certificates and root certificates for the commercial CA which issued your Web SSL certificate. You can name the file whatever you want, but place it under `/etc/certs`. The file should contain intermediate certificate(s), followed by the root CA'a certificate. ![image]() For more info see doc page about the [SSLCertificateChainFile directive](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatechainfile)
3. Put your new commercial certificate in PEM format in one file, and the private key you used to generate the CSR for this certificate in the other file under `/etc/certs/`; make sure your private key isn't password protected.
4. Verify that user under which your Apache process runs has read permissions to all three files: certificate chain, server ssl certificate, key.
5. Update `SSLCertificateFile`, `SSLCertificateKeyFil` and `SSLCertificateChainFile` directives in Gluu's Apcache configuration file so they point to the files you've added; in Ubuntu you can find the configuration in `/etc/apache2/sites-enabled/https_gluu.conf`. For Centos and RedHat, it is located in `/etc/httpd/conf.d/https_gluu.conf`.

Now its time to update the default keystore of your JVM:

1. Create a copy of your commercial certificate encoded in DER format: `# openssl x509 -in pem-formatted-cert.crt -outform der -out der-formatted-cert.der`
2. Find out the exact alias name of your current (self-signed) Apache certificate in the cacerts file: `# keytool -list -v -keystore /usr/java/latest/lib/security/cacerts -storepass changeit | grep -i '_httpd'` It should have an alias of sort “your-instance-hostname_httpd”
3. Remove your old certificate from the store: `# keytool -delete -alias your-instance-hostname_httpd -keystore /usr/java/latest/lib/security/cacerts \
-storepass changeit`
4. Import the new one with the same alias: `# keytool -import -alias your-instance-hostname_httpd --trustcacerts -file /etc/certs/der-formatted-cert.der \
-keystore /usr/java/latest/lib/security/cacerts -storepass changeit`
5. Restart Tomcat service: `# /etc/init.d/tomcat restart`
6. Restart Apache service: `# /etc/init.d/apache2 restart`

### How to test

You have next options:

1. Checking how certificate chain is visualized and its healthiness is evaluated by your browser. For example, correctly configured certificate chain may look like this in Firefox: ![image]()
2. You could use one of online validation tools, like the Qualys® SSL Labs' SSL Server Test
3. Using console tools, like connecting to the SSL/TLS enabled port your Gluu's Apache listens on (443 by default) with `# openssl s_client -showcerts -connect <host>:<port>`. It will display the whole certificate chain sent by the web server together with secure overlay's parameters which were negotiated during SSL/TLS handshake.

## Updating certificate used by Shibboleth module (idp.war)

Shibboleth has it's own java keystore protected by a password that is unique to each instance. Due to this just copying previous Shibboleth keystore file is not the easiest way to proceed, as you would need to find all possible places in configuration files from which it's being referenced and update all settings in them mentioning that password. It's better to recreate this keystore using key pair imported from your previous instance and password which the new instance uses, with the same console commands `setup.py` script employs. To properly install your previous Shibboleth certificate:

1. Log into the your new instance: `# service gluu-server-2.4.3 login` (if you use Gluu CE older than 2.4.x you should update to current version)
2. Copy your Shibboleth's secret key (in non-encrypted form) and certificate in PEM format into `/etc/certs` directory, overwriting corresponding files there. In Gluu CE 2.4.x these files are named `shibIDP.key` and `shibIDP.crt`, respectively.
3. Acquire Shibboleth's keystore's password this instance uses. One option is to get it from the `setup.properties.last` file: `# cat /install/community-edition-setup/setup.properties.last | grep -i 'shibJksPass'`
4. Merge together certificate and key files into PKCS12 archive: `# openssl pkcs12 -export -inkey /etc/certs/shibIDP.key -in /etc/certs/shibIDP.crt -out /etc/certs/shibIDP.pkcs12 \
-passout pass:YOUR_SHIB_KEYSTORE_PASS -name your-instance-hostname`
5. Transform your PKCS12 archive into new instance's Shibboleth's java keystore file (this command will overwrite your privous keystore in `/etc/certs`): `# keytool -importkeystore -srckeystore /etc/certs/shibIDP.pkcs12 -srcstorepass YOUR_SHIB_KEYSTORE_PASS \
-srcstoretype PKCS12 -destkeystore /etc/certs/shibIDP.jks -deststoretype JKS -deststorepass YOUR_SHIB_KEYSTORE_PASS \
-keyalg RSA -noprompt`
6. Verify that user “tomcat” has read access to all 4 files mentioned (shibIDP.key, shibIDP.crt, shibIDP.pkcs12 and shibIDP.jks)
7. Create a copy of your Shibboleth certificate encoded in DER format: `# openssl x509 -in /etc/certs/shibIDP.crt -outform der -out /etc/certs/shibIDP.der`
8. Find out the exact alias name of your current Shibboleth's certificate in the `cacerts` file: `# keytool -list -v -keystore /usr/java/latest/lib/security/cacerts -storepass changeit | grep -i '_shibidp'`. It should have an alias of sort “your-instance-hostname_shibidp”
9. Remove your old certificate from the store: `# keytool -delete -alias your-instance-hostname_shibidp -keystore /usr/java/latest/lib/security/cacerts \
-storepass changeit`
10. Import the new one with the same alias: `# keytool -import -alias your-instance-hostname_shibidp --trustcacerts -file /etc/certs/shibIDP.der \
-keystore /usr/java/latest/lib/security/cacerts -storepass changeit`
11. Restart Tomcat service: `# /etc/init.d/tomcat restart`
12. Restart Apache service: `# /etc/init.d/apache2 restart`

### How to test

After Tomcat's restart Shibboleth's configuration generated from a set of Velocity templates should be updated to include your changes to it. One way to test they have been applied is to check the current certificate the module includes in its SAML metadata that is shown at url like [https://your-instance-hostname/idp/shibboleth](https://your-instance-hostname/idp/shibboleth), or can be found in the file `/opt/idp/metadata/YOUR-ORG-INUM-idp-metadata.xml` - it should show the same certificate you tried to import following steps above. If it does not, try to wait until Tomcat has fully started and restart it one more time. Please also pay attention to any error messages appearing in `/opt/idp/logs/idp-process.log` during Tomcat's startup.

## Updating certificate used by Asimba module (asimba.war)

This procedure is quite similar to updating Shibboleth's certificate: 

1. Log into your instance: `# service gluu-server-2.4.3 login` (if you use Gluu CE older than 2.4 you should update to current version)
2. Copy your Asimba's secret key (in non-encrypted form) and certificate in PEM format into `/etc/certs` directory, overwriting corresponding files there. In Gluu CE 2.4.x these files are named `asimba.key` and `asimba.crt`, respectively.
3. Acquire Shibboleth keystore's password this instance uses. One option is to get it from the `setup.properties.last` file: `# cat /install/community-edition-setup/setup.properties.last | grep -i 'asimbaJksPass'`
4. Merge together certificate and key files into PKCS12 archive: `# openssl pkcs12 -export -inkey /etc/certs/asimba.key -in /etc/certs/asimba.crt -out /etc/certs/asimba.pkcs12 \
-passout pass:YOUR_ASIMBA_KEYSTORE_PASS -name your-instance-hostname`
5. Transform your PKCS12 archive into new instance's Asimba's java keystore file: `# keytool -importkeystore -srckeystore /etc/certs/asimba.pkcs12 -srcstorepass YOUR_ASIMBA_KEYSTORE_PASS \
-srcstoretype PKCS12 -destkeystore /etc/certs/asimbaIDP.jks -deststoretype JKS -deststorepass YOUR_ASIMBA_KEYSTORE_PASS \
-keyalg RSA -noprompt`
6. Verify that user “tomcat” has read access to all 4 files mentioned (asimba.key, asimba.crt, asimba.pkcs12 and asimbaIDP.jks)
7. Create a copy of your Shibboleth certificate encoded in DER format: `# openssl x509 -in /etc/certs/asimba.crt -outform der -out /etc/certs/asimba.der`
8. Find out the exact alias name of your current Shibboleth's certificate in the cacerts file: `# keytool -list -v -keystore /usr/java/latest/lib/security/cacerts -storepass changeit | grep -i '_asimba'`
It should have an alias of sort “your-instance-hostname_asimba”
9. Remove your old certificate from the store: `# keytool -delete -alias your-instance-hostname_asimba -keystore /usr/java/latest/lib/security/cacerts \
-storepass changeit`
10. Import the new one with the same alias: `# keytool -import -alias your-instance-hostname_asimba --trustcacerts -file /etc/certs/asimba.der \
-keystore /usr/java/latest/lib/security/cacerts -storepass changeit`
11. Restart Tomcat service: `# /etc/init.d/tomcat restart`
12. Restart Apache service: `# /etc/init.d/apache2 restart`

## Updating OpenDJ's certificate in the default java keystore

As was mentioned before, if some component of Gluu CE package needs to connect to OpenDJ via LDAPS, it must be able to verify the authenticity and credibility of certificate presented by it by referencing java default keystore. Sometimes you may need to import cacerts file from your previous instance, overwriting corresponding file of the new container. After that it will contain your OpenDJ's certificate from the previous instance which won't match the certificate used by OpenDJ in this one.

OpenDJ has its own password-protected java keystore where it stores his key pair together with certificate. It can be found at this path: `/opt/opendj/config/keystore`. Your options are either to recreate this keystore using the key pair and certificate from your previous instance (not recommended; you should refer to OpenDJ's documentation for requirements to this keystore's composition if you choose to do so), or remove the certificate of previous OpenDJ's instance from default keystore, and add the current certificate to it. To achieve the later: 

1. Log into your instance: `# service gluu-server-2.4.3 login` (if you use Gluu CE older than 2.4 you should update to current version)
2. If you didn't preserve original certificates from the `/etc/certs` directory of the new container (you should do that) and OpenDJ certificate which is also placed there by setup scripts (it should be named “opendj.crt”) got overwritten by the certificate transferred from the previous one, you still can export it from the OpenDJ's own keystore with command like that:
    1. Acquire password for your keystore: `# cat /opt/opendj/config/keystore.pin`
    2. Find out the exact alias name of your current OpenDJ certificate: `# keytool -list -v -keystore /opt/opendj/config/keystore -storepass YOUR_OPENDJ_JKS_PIN` It should have alias “server-cert” and there should be no other entries in the keystore, but it may change in the future.
    3. Fetch the certificate from the store: `# keytool -export -alias alias_you_discovered -file /etc/certs/opendj-exported-cert.der \
    -keystore /opt/opendj/config/keystore -storepass opendj_jks_pin` Now you are ready to import it into default java keystore

3. Find out the exact alias name of your current OpenDJ's certificate in the cacerts file: `# keytool -list -v -keystore /usr/java/latest/lib/security/cacerts -storepass changeit | \
grep -i '_opendj'` It should have an alias of sort “your-instance-hostname_opendj”
4. Remove your old certificate from the store: `# keytool -delete -alias your-instance-hostname_opendj -keystore /usr/java/latest/lib/security/cacerts \
-storepass changeit`
5. Import the new one with the same alias: `# keytool -import -alias your-instance-hostname_opendj --trustcacerts -file /etc/certs/opendj-exported-cert.der \
-keystore /usr/java/latest/lib/security/cacerts -storepass changeit`
6. Restart Tomcat service: `# /etc/init.d/tomcat restart`
7. Restart Apache service: `# /etc/init.d/apache2 restart`

### How to test

You can verify that the certificate in cacerts file is the same as in the OpenDJ's keystore using the same “keytool -list” commands as before. Failure when establishing SSL/TLS connection with OpenDJ will result in errors appearing in `/opt/idp/logs/idp-process.log` and `/opt/tomcat/logs/wrapper.log` during Tomcat's startup.