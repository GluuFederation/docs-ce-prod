# Certificates 

## Certificates in  Chroot

Gluu Server components have cryptographic keys and X.509 certificates that are stored inside the`chroot`. Details for certificates associated with each component are provided below. The following certificates are available in the `/etc/certs` folder.

|IDP		                  |Shibboleth	       |APACHE		       |OPENDJ         |
|---------------        |---------------   |---------------|---------------  |
|idp-encryption.crt    	|shibIDP.crt	      |httpd.crt	     |opendj.crt	   |
|idp-encryption.csr    	|shibIDP.csr	      |https.csr	     |opendj.pksc12	   |
|idp-encryption.key 	   |shibIDP.jks	      |httpd.key      |               |
|idp-encryption.key.orig|shibIDP.key	      |httpd.key.orig |             |
|idp-signing.crt	       |shibIDP.key.orig  |		             |	            |
|idp-signing.csr       	|shibIDP.pkcs12  	 |               |		           |
|idp-signing.key        |                  |               |             |
|idp-signing.key.orig   |                  |               |             |

The certificates for `Passport` authentication are `passport-rp.jks, passport-rp.pem, passport-rs.jks`. 

The SCIM certificate is named `scim-rs.jks` and the OTP certificate is named `otp_configuration.json`.

### Certificates for Deprecated Services

|ASIMBA		    |OPENLDAP         |
|---------------|--------------- |
|asimba.crt   	|openldap.crt	   |
|asimba.csr 	|openldap.csr	   |
|asimba.key 	|openldap.key	   |
|asimba.key.orig|openldap.key.orig|
|asimba.pkcs12	|openldap.pem	   |
|asimbaIDP.jks	|	           |

### Custom Script JSON Files

Additionally the following `json` files are available which are used in different custom scripts for multi-factor authentication.
 
* `cert_creds.json`    
* `duo_creds.json`    
* `gplus_client_secrets.json`     
* `otp_configuration.json`    
* `oxauth-keys.json`     
* `super_gluu_creds.json`  
* `vericloud_gluu_creds.json`

### Generating Cryptographic Keys

The Gluu Server is compatible with the [Java KeyGenerator](https://docs.oracle.com/javase/7/docs/api/javax/crypto/KeyGenerator.html)
to create new cryptographic keys if needed.

To get KeyGenerator, run the following command inside the Chroot:

```
wget https://ox.gluu.org/maven/org/xdi/oxauth-client/4.0.sp1/oxauth-client-4.0-jar-with-dependencies.jar -O oxauth-client.jar
```

Then, run KeyGenerator with the following command:

```
java -jar oxauth-client.jar <arguments>
```

Our implementation of KeyGenerator accepts the following arguments:

| Argument | Description |
| --- | --- |
| -at <arg> | oxEleven Access Token |
| -dnname <arg> | DN of certificate issuer |
| -enc_keys <arg> | Encryption keys to generate (For example: RSA_OAEP, RSA1_5) |
| -expiration <arg> | Expiration in days |
| -expiration_hours <arg> | Expiration in hours |
| -h | Show help |
| -keypasswd <arg> | Key Store password |
| -keystore <arg> | Key Store file (such as /etc/certs/api-rs.jks)|
| -ox11 <arg> | oxEleven Generate Key Endpoint. |
| -sig_keys <arg> | Signature keys to generate. (For example: RS256 RS384 RS512 ES256 ES384 ES512 PS256 PS384 PS512) |

## Certificates in oxTrust

Certificates commonly used for SSO typically have a short expiration date, and can now be easily viewed and downloaded in oxTrust. Navigate to `Configuration` > `Certificates` to access these certificates. 

The following are available:

- OpenDJ SSL   
- httpd SSL   
- IDP Signing   
- IDP Encryption   

![Example Certs in oxTrust](../img/admin-guide/oxtrust-certs.png)

## Updating Apache Certificate

The certificates must be manually updated from the `/etc/certs/` folder. 
    
There are many tools that can be used to update and renew certificates. By default Gluu uses OpenSSL. 
If you have questions about using other tools, like Let'sEncrypt, 
check the [Gluu support portal](http://support.gluu.org) for existing threads. 
If there is no existing information, sign up and open a ticket. 

!!! Warning
    The private key cannot be password protected, and the public key must be base64 X.509. 

!!! Note
    Please backup your full `/etc/certs` directory and `cacerts` file under `/opt/jdkx.y.z/jre/lib/security/` folder before updating certificates.

Please follow these steps shown below to update the Apache SSL cert:

- Save the latest SSL httpd key and certificate in the `/etc/certs` folder
- Rename them to `httpd.key` and `httpd.crt` respectively
- Import 'httpd.der' into the java keystore
/ Convertion to DER, command:<br/> `openssl x509 -outform der -in httpd.crt -out httpd.der`
    - Delete the existing certificate to avoid ambiguity due to presense of 2 different 
    certificates for the same entity after importing the new one:
       `/opt/jdkx.x.x.x/jre/bin/keytool -delete -alias <hostname_of_your_Gluu_Server>_httpd -keystore /opt/jdkx.x.x.x/jre/lib/security/cacerts -storepass changeit`
    - Import certificate in to Java Keystore(cacerts):
    <br/> `/opt/jdkx.x.x.x/jre/bin/keytool -importcert -file httpd.der -keystore /opt/jdkx.x.x.x/jre/lib/security/cacerts -alias <hostname_of_your_Gluu_Server>_httpd -storepass changeit`
- [Restart](../operation/services.md#restart) `opendj`, `apache2/httpd`, `oxauth` and `identity` services.

## Install Intermediate Certificates
Please follow the steps below to install intermediate certificates:

1. Log in to your Gluu Server container.
2. Keep your intermediate certificate in the file `/etc/certs/`.
3. Modify `/etc/httpd/conf.d/https_gluu.conf`, and add<br/>
  `SSLCertificateChainFile /etc/certs/name_of_your_interm_root_cert.crt`.
4. [Restart](../operation/services.md#restart) the `httpd` service.
