# Mutual TLS Client Authentication and Certificate Bound Access Tokens
 
CE supports MTLS Client Authentication (available in Financial Edition of Gluu Server). 

`token_endpoint_auth_method` client property can accept two new values:

  - `tls_client_auth` - indicates that client authentication to the authorization server will occur with mutual TLS utilizing the PKI method of associating a certificate to a client.
  - `self_signed_tls_client_auth` - Indicates that client authentication to the authorization server will occur using mutual TLS with the client utilizing a self-signed certificate.
  
There is new client property `tls_client_auth_subject_dn` used to compare Subject DN of the certificate with configured value of client entry when authentication method is set to `tls_client_auth` (saved in `tls_client_auth_subject_dn` or `oxAttributes` on persistence layer).

If MTLS Authentication is used then `access_token` automatically saves certificate S256 hash of certificates which can be validated by RP.
If `access_token` is JWT then `x5t#S256` claim is added to payload of the token. Otherwise token can be introspected.

Example of introspection response with token which was created with MTLS:
```json
     HTTP/1.1 200 OK
     Content-Type: application/json

     {
       "active": true,
       "iss": "https://server.example.com",
       "sub": "ty.webb@example.com",
       "exp": 1493726400,
       "nbf": 1493722800,
       "cnf":{
         "x5t#S256": "bwcK0esc3ACC3DB2Y5_lESsXE8o9ltc05O89jdN-dg2"
       }
     }
``` 

It is critical to configure certificates validation on Apache 2 correctly, since actual validation of the certificates is performed by Apache 2. After Apache certificate validation is configured correctly, make sure there is client certificate forward to `oxauth` application. `oxauth` (AS) expects certificate in `X-ClientCert` header. 

```
<LocationMatch /oxauth>
    SSLVerifyClient require
    SSLVerifyDepth 10
    SSLOptions -StdEnvVars +ExportCertData

    # Forward certificate to destination server (oxauth)
    RequestHeader set X-ClientCert %{SSL_CLIENT_CERT}s
</LocationMatch>

``` 

## Configuring Apache For MTLS

The information below belongs to apache and web client(usually web browser) mutual authentication setup method. This also includes basic checks to be performed for the setup.

Is mod_ssl installed:
Run below command to confirm if the ssl module is installed. 
`apachectl -M | grep ssl`

If we get ssl_module related output, then we're good to proceed.
The output could look like:

```
GLUU.root@localhost:~# apachectl -M | grep ssl
 ssl_module (shared)
GLUU.root@localhost:~# 
```

Now, we're covering the case if you want to deploy your own CA Cert.

Run below command to create self-signed CA Cert:

`openssl req -newkey rsa:2048 -nodes -keyform PEM -keyout example-ca.key -x509 -days 3650 -outform PEM -out example-ca.crt`

Below is a sample run of the command:

```
GLUU.root@localhost:~# openssl req -newkey rsa:2048 -nodes -keyform PEM -keyout example-ca.key -x509 -days 3650 -outform PEM -out example-ca.crt
Generating a 2048 bit RSA private key
.+++
............................+++
writing new private key to 'example-ca.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:EX
State or Province Name (full name) [Some-State]:Example
Locality Name (eg, city) []:example
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Example Company Pvt. Ltd.
Organizational Unit Name (eg, section) []:IT
Common Name (e.g. server FQDN or YOUR name) []:accounts.example.com
Email Address []:example@example.com
```

Above command will create two files: **example-ca.key** and **example-ca.crt**

```
GLUU.root@localhost:~# ls
example-ca.crt  example-ca.key
GLUU.root@localhost:~#    
```

Next generate csr for self-signed certificate which we'll sign with our own CA Cert.

Create SSL server private key:
`openssl genrsa -out example.key 2048 `

Here is the sample run of the command:

```
GLUU.root@localhost:~# openssl genrsa -out example.key 2048
Generating RSA private key, 2048 bit long modulus
..............+++
............................................+++
e is 65537 (0x10001)
```

Above command creates **example.key**

See the output:

```
GLUU.root@localhost:~# ls
example-ca.crt  example-ca.key  example.key
GLUU.root@localhost:~# 
```


Next create the CSR(Certificate Signing Request) for the server:

`openssl req -new -key example.key -out example.csr `

The sample run is:
```
GLUU.root@localhost:~# openssl req -new -key example.key -out example.csr 
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:example-city
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:sample.example.com  
Email Address []:sample@example.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
GLUU.root@localhost:~# 
```

The command will create **example.csr** as seen below:

```
GLUU.root@localhost:~# ls
example-ca.crt  example-ca.key  example.csr  example.key
GLUU.root@localhost:~# 
```


Next we will sign the Apache server CSR **example.csr** we just generated as below:

`openssl x509 -req -in example.csr -CA example-ca.crt -CAkey example-ca.key -set_serial 100 -days 365 -outform PEM -out example.crt`

Below is the sample run of the command above:

```
GLUU.root@localhost:~# openssl x509 -req -in example.csr -CA example-ca.crt -CAkey example-ca.key -set_serial 100 -days 365 -outform PEM -out example.crt
Signature ok
subject=/C=AU/ST=Some-State/L=example-city/O=Internet Widgits Pty Ltd/CN=sample.example.com/emailAddress=sample@example.com
Getting CA Private Key
GLUU.root@localhost:~# 
```
 

The command will create: **example.crt** and for 10 years.

```
GLUU.root@localhost:~# 
GLUU.root@localhost:~# ls
example-ca.crt  example-ca.key  example.crt  example.csr  example.key
GLUU.root@localhost:~# 
```



The following lines should be included in Apache configuration which is responsible for ssl connection. The paths of cert files could be different. Like for CentOS **/etc/pki/tls** is the path. **/etc/ssl/** is for Debian based distros. So, use yours.

```
SSLEngine On
SSLCertificateFile /etc/pki/tls/example.crt
SSLCertificateKeyFile /etc/pki/tls/example.key
SSLCACertificateFile /etc/pki/tls/example-ca.crt
```

Once changes are done, reload apache configuration by running:

RHEL or CentOS 6 or below:
`service apache2 reload`

Debian 8, Ubuntu 14 or lower
`service httpd reload`

RHEL or CentOS 7:
`systemctl restart httpd`

Debian 9, Ubuntu 16 or newer:
`systemctl restart apache2`

To check if SSL cert on apache works:
`Openssl s_client -connect sample.example.com:443`


Mutual Authentication Setup

First thing is to generate private key for client. Run the command below to generate private key:

`openssl genrsa -out example-cli.key 2048`

```
ganesh@rddwiw0001:~/client$ openssl genrsa -out example-cli.key 2048
Generating RSA private key, 2048 bit long modulus
....................................................................................+++++
.................................................................+++++
e is 65537 (0x010001)
ganesh@rddwiw0001:~/client$ 
```

The command creates **example-cli.key** as seen below:

```
ganesh@rddwiw0001:~/client$ ls
example-cli.key
ganesh@rddwiw0001:~/client$ 
```

Next create the client CSR with below command:
`openssl req -new -key example-cli.key -out example-cli.csr `

The sample run is like:
```
ganesh@rddwiw0001:~/client$ openssl req -new -key example-cli.key -out example-cli.csr 
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:IN
State or Province Name (full name) [Some-State]:Punjab
Locality Name (eg, city) []:Rupnagar
Organization Name (eg, company) [Internet Widgits Pty Ltd]:WorldisWelcome
Organizational Unit Name (eg, section) []:IT
Common Name (e.g. server FQDN or YOUR name) []:client.example.com
Email Address []:example@somedomain.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

This run will create **example-cli.csr** as seen below:
```
ganesh@rddwiw0001:~/client$ ls
example-cli.csr  example-cli.key
ganesh@rddwiw0001:~/client$ 
```



Sign the client CSR:
`openssl x509 -req -in example-cli.csr -CA example-ca.crt -CAkey example-ca.key -set_serial 101 -days 365 -outform PEM -out example-cli.crt `

```
ganesh@rddwiw0001:~/client$ openssl x509 -req -in example-cli.csr -CA example-ca.crt -CAkey example-ca.key -set_serial 101 -days 365 -outform PEM -out example-cli.crt 
Signature ok
subject=C = IN, ST = Punjab, L = Rupnagar, O = WorldisWelcome, OU = IT, CN = client.example.com, emailAddress = example@somedomain.com
Getting CA Private Key
ganesh@rddwiw0001:~/client$ 
```

The run creates **example-cli.crt** as seen below.
```
ganesh@rddwiw0001:~/client$ ls
example-ca.crt  example-cli.crt  example-cli.key  example.csr
example-ca.key  example-cli.csr  example.crt      example.key
ganesh@rddwiw0001:~/client$ 
```

Some browsers like firefox need client certs to be in the format pkcs12. So run the below command to bundle the client's certificate and client's key into a p12 pack:
`openssl pkcs12 -export -inkey example-cli.key -in example-cli.crt -out example-cli.p12`

Above command will create example-cli.p12. Below is the sample run:

```
ganesh@rddwiw0001:~/client$ openssl pkcs12 -export -inkey example-cli.key -in example-cli.crt -out example-cli.p12
Enter Export Password:
Verifying - Enter Export Password:
ganesh@rddwiw0001:~/client$ ls
example-ca.crt  example-cli.crt  example-cli.key  example.crt  example.key
example-ca.key  example-cli.csr  example-cli.p12  example.csr
ganesh@rddwiw0001:~/client$ 
```





[MTLS spec](https://tools.ietf.org/html/draft-ietf-oauth-mtls-12)
