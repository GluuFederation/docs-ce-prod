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

 


[MTLS spec](https://tools.ietf.org/html/draft-ietf-oauth-mtls-12)
