# Certificates 

## Certificates in Chroot

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

The Gluu Server is compatible with the [Java KeyGenerator](https://docs.oracle.com/javase/7/docs/api/javax/crypto/KeyGenerator.html) to create new cryptographic keys if needed.

To get KeyGenerator, run the following command inside the chroot:

```
wget https://ox.gluu.org/maven/org.gluu/oxauth-client/4.1/oxauth-client-4.1-jar-with-dependencies.jar -O oxauth-client.jar
```

Then, run KeyGenerator with the following command:

```
java -jar oxauth-client.jar <arguments>
```

The Gluu implementation of KeyGenerator accepts the following arguments:

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
    
There are many tools that can be used to update and renew certificates. By default Gluu uses OpenSSL. If you have questions about using other tools, like Let'sEncrypt, check the [Gluu support portal](http://support.gluu.org) for existing threads. If there is no existing information, sign up and open a ticket. 

!!! Warning
    The private key cannot be password protected, and the public key must be base64 X.509. 

!!! Note
    Please backup your full `/etc/certs` directory and `cacerts` file under `/opt/jdkx.y.z/jre/lib/security/` folder before updating certificates.

Please follow these steps shown below to update the Apache SSL cert:

- Save the latest SSL httpd key and certificate in the `/etc/certs` folder
- Rename them to `httpd.key` and `httpd.crt` respectively
- Import 'httpd.der' into the Java Keystore
/ Convertion to DER, command:<br/> `openssl x509 -outform der -in httpd.crt -out httpd.der`
    - Delete the existing certificate to avoid ambiguity due to presence of 2 different certificates for the same entity after importing the new one: 
    `/opt/amazon-corretto-x.x.x.x/jre/bin/keytool -delete -alias <hostname_of_your_Gluu_Server>_httpd -keystore /opt/amazon-corretto-x.x.x.x/jre/lib/security/cacerts -storepass changeit`
    - Import certificate into the Java Keystore(cacerts):
    `/opt/amazon-corretto-x.x.x.x/jre/bin/keytool -importcert -file httpd.der -keystore /opt/amazon-corretto-x.x.x.x/jre/lib/security/cacerts -alias <hostname_of_your_Gluu_Server>_httpd -storepass changeit`
- [Restart](../operation/services.md#restart) `opendj`, `apache2/httpd`, `oxauth` and `identity` services.

## Install Intermediate Certificates
Please follow the steps below to install intermediate certificates:

1. Log in to the Gluu Server container.
2. Keep your intermediate certificate in the file `/etc/certs/`.
3. Modify `/etc/httpd/conf.d/https_gluu.conf`, and add  
  `SSLCertificateChainFile /etc/certs/name_of_your_interm_root_cert.crt`.
4. [Restart](../operation/services.md#restart) the `httpd` service.

## Updating  Certificates and keys instructions for Kubernetes

The following table shows all the keys that can be replaced inside the gluu secret.

| Key                                       |
| ----------------------------------------- |
| `api_rp_jks_base64`                       |
| `api_rs_jks_base64`                       |
| `gluu_ro_client_base64_jwks`              |
| `idp3EncryptionCertificateText`           |
| `idp3EncryptionKeyText`                   |
| `idp3SigningCertificateText`              |
| `idp3SigningKeyText`                      |
| `ldap_pkcs12_base64`                      |
| `ldap_ssl_cacert`                         |
| `ldap_ssl_cert`                           |
| `ldap_ssl_key`                            |
| `oxauth_jks_base64`                       |
| `oxauth_openid_key_base64`                |
| `passport_rp_client_base64_jwks`          |
| `passport_rp_client_cert_base64`          |
| `passport_rp_jks_base64`                  |
| `passport_rs_client_base64_jwks`          |
| `passport_rs_jks_base64`                  |
| `passport_sp_cert_base64`                 |
| `passport_sp_key_base64`                  |
| `radius_jks_base64`                       |
| `scim_rp_client_base64_jwks`              |
| `scim_rp_jks_base64`                      |
| `scim_rs_client_base64_jwks`              |
| `scim_rs_jks_base64`                      |
| `shibIDP_cert`                            |
| `shibIDP_jks_base64`                      |
| `shibIDP_key`                             |
| `ssl_cert`                                |
| `ssl_key`                                 |

1. Login the vm controlling the kubernetes cluster. 

1. Make a directory called `update`.

    ```bash
    mkdir update && cd update
    ```

1. Grab the gluu secret and store it as `gluu_secret.yaml`

    ```bash
    kubectl get secrets gluu -n <namespace> -o yaml > gluu_secret.yaml
    ```

1. Optional: If the gluu https crt and key are being updated the ingress tls needs to be copied as well.

    ```bash
    kubectl get secrets tls-certificate -n <namespace> -o yaml > gluu_tls_certificate.yaml
    ```
1. Optional: Make a copy of this secret.

    ```bash
    cp gluu_tls_certificate.yaml original_gluu_tls_certificate.yaml
    ```
    
1. Make a copy of the gluu secret.

    ```bash
    cp gluu_secret.yaml original_secret.yaml
    ```

1. For every key in the table above that will be updated create a file with the same name as the key name and the contents of the key that will be updated. Forexample, we will update `ssl_cert` and `ssl_key`.

    ```
    vi ssl_cert
    ```
    and pasted the new cert content i.e `-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----`

    ```
    vi ssl_key
    ```
    and pasted the new key content i.e `-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----`
    

1. Download latest [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases) and run `update-secret` command.

    ```bash
    ./pygluu-kubernetes.pyz update-secret
    ```
    
1. `gluu_secret.yaml` should have been modified now. Delete the existing secret so the updated one can replace it. 

    ```bash
    kubectl delete secret gluu -n <namespace>
    ```
    
1. Create the modified secret. 

    ```bash
    kubectl create -f gluu_secret.yaml
    ```

1. Optional: If the gluu https crt and key are being updated the ingress tls needs to be updated as well.

    ```bash
    kubectl apply -f  gluu_tls_certificate.yaml
    ```
    
    Please update  the certificate and key  associated with the load balancer on cloud deployments.
 
 1. Restart pods to reload crts and keys in order `oxauth`, `oxtrust`, `oxpassport`, `oxshibboleth`, `radius`
 
    ```bash
    kubectl scale deploy oxauth -n <namespace> --replicas=0
    kubectl scale deploy oxauth -n <namespace> --replicas=1
    # Wait until oxauth is up
    kubectl scale statefulset oxtrust -n <namespace> --replicas=0
    kubectl scale statefulset oxtrust -n <namespace> --replicas=0
    ...
    ```
    
    
    
