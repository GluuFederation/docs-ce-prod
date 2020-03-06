## Overview

The Config Init job creates a set of secrets and configurations used by all Gluu services.

To check the values of the secret keys on the current deployment run :

```bash
kubectl get secrets gluu -n <namespace> -o yaml
```

To check the values of the configuration keys on the current deployment run :

```bash
kubectl get configmap  gluu -n <namespace> -o yaml
```

## Gluu Configuration Keys

| Parameter                                       | Example Values                                     |
| ----------------------------------------------- | -------------------------------------------------- |
| `admin_email`                                   | `support@gluu.org`                                 |
| `admin_inum`                                    | `d3afef58-c026-4514-9d4c-e0a3efb4c29d `            |
| `api_rp_client_jks_fn`                          | `/etc/certs/api-rp.jks`                            |
| `api_rp_client_jwks_fn`                         | `/etc/certs/api-rp-keys.json`                      |
| `api_rs_client_jks_fn`                          | `/etc/certs/api-rs.jks`                            |
| `api_rs_client_jwks_fn`                         | `/etc/certs/api-rs-keys.json`                      |
| `api_test_client_id`                            | `0008-db36db1f-025e-4164-aeed-f82df064eee8`        |
| `city`                                          | `Austin`                                           |
| `couchbaseTrustStoreFn`                         | `/etc/certs/couchbase.pkcs12`                      |
| `country_code`                                  | `US`                                               |
| `default_openid_jks_dn_name`                    | `CN=oxAuth CA Certificates`                        |
| `fido2ConfigFolder`                             | `/etc/gluu/conf/fido2`                             |
| `gluu_radius_client_id`                         | `1701.9c798f32-1b01-42e9-99fe-415060e69e8e`        |
| `hostname`                                      | `demoexample.gluu.org`                             |
| `idp3Folder`                                    | `/opt/shibboleth-idp`                              |
| `idp_client_id`                                 | `1101.638504bc-d445-4559-a192-66f0d4e919a8`        |
| `jetty_base`                                    | `/opt/gluu/jetty`                                  |
| `ldapTrustStoreFn`                              | `/etc/certs/opendj.pkcs12`                         |
| `ldap_binddn`                                   | `cn=directory manager`                             |
| `ldap_init_host`                                | `opendj`                                           |
| `ldap_init_port`                                | `1636`                                             |
| `ldap_peers`                                    | `["gluu-opendj-0.opendj.gluu.svc.cluster.local"]`  |
| `ldap_port`                                     | `1389`                                             |
| `ldap_site_binddn`                              | `cn=directory manager`                             |
| `ldaps_port`                                    | `1636`                                             |
| `orgName`                                       | `Gluu`                                             |
| `oxauth_client_id`                              | `1001.1c2946c9-b913-43e7-b82e-6215ad4e87c1`        |
| `oxauth_key_rotated_at`                         | `1581608454`                                       |
| `oxauth_legacyIdTokenClaims`                    | `true`                                             |
| `oxauth_openidScopeBackwardCompatibility`       | `true`                                             |
| `oxauth_openid_jks_fn`                          | `/etc/certs/oxauth-keys.jks`                       | 
| `oxauth_openid_jwks_fn`                         | `/etc/certs/oxauth-keys.json`                      |
| `oxtrust_requesting_party_client_id`            | `1402.f611f06c-1946-4c45-8eac-a57795a324b7`        |
| `oxtrust_resource_id`                           | `1403.aff108f4-ed21-4d5c-81fb-a588e70e07f1`        |
| `oxtrust_resource_server_client_id`             | `1401.ece0dc1e-a53c-462e-b161-43867b6a4aa1`        |
| `passportSpJksFn`                               | `/etc/certs/passport-sp.jks`                       |
| `passportSpTLSCACert`                           | `/etc/certs/passport-sp.pem`                       |
| `passportSpTLSCert`                             | `/etc/certs/passport-sp.crt`                       |
| `passportSpTLSKey`                              | `/etc/certs/passport-sp.key`                       |
| `passport_resource_id`                          | `1504.85bdbfac-6338-4b9c-b945-2dc245067c1a`        |
| `passport_rp_client_cert_alg`                   | `RS512`                                            |
| `passport_rp_client_cert_alias`                 | `78882060-4214-4317-a402-79960fca7901_sig_rs512`   |
| `passport_rp_client_cert_fn`                    | `/etc/certs/passport-rp.pem`                       |
| `passport_rp_client_id`                         | `1502.d9b8c3aa-60a0-404c-afec-e13811a708ec`        |
| `passport_rp_client_jks_fn`                     | `/etc/certs/passport-rp.jks`                       |
| `passport_rp_client_jwks_fn`                    | `/etc/certs/passport-rp-keys.json`                 |
| `passport_rp_ii_client_id`                      | `1503.3bda64b7-293e-4160-9c97-a5592c1fbd0a`        |
| `passport_rs_client_id`                         | `1501.c7165c37-8208-4b72-9378-de60deb279b4`        |
| `passport_rs_client_jks_fn`                     | `/etc/certs/passport-rs.jks`                       |
| `passport_rs_client_jwks_fn`                    | `/etc/certs/passport-rs-keys.json`                 |
| `radius_jwt_keyId`                              | `996e281b-a63a-44a9-badf-197f9fd1aa0f_sig_rs512`   |
| `scim_resource_oxid`                            | `1203.`                                            |
| `scim_rp_client_id`                             | `1202.4099a09e-f300-4fa8-8cfd-cb1347149652`        |
| `scim_rp_client_jks_fn`                         | `etc/certs/scim-rp.jks`                            |
| `scim_rp_client_jwks_fn`                        | `/etc/certs/scim-rp-keys.json`                     |
| `scim_rs_client_id`                             | `1201.70bb198a-a10f-461b-81a1-68fa52ca0646`        |
| `scim_rs_client_jks_fn`                         | `/etc/certs/scim-rs.jks`                           |
| `scim_rs_client_jwks_fn`                        | `/etc/certs/scim-rs-keys.json`                     | 
| `scim_test_client_id`                           | `0008-1b21974a-5d5c-43f3-b332-e66a6399f2b5`        |
| `shibJksFn`                                     | `/etc/certs/shibIDP.jks`                           | 
| `shibboleth_version`                            | `v3`                                               |
| `state`                                         | `TX`                                               | 

## Gluu Secret Keys

| Secret                                          | 
| ----------------------------------------------- |
| `api_rp_client_base64_jwks`                     |
| `api_rp_client_jks_pass`                        |
| `api_rp_client_jks_pass_encoded`                |
| `api_rp_jks_base64`                             |
| `api_rs_client_base64_jwks`                     |
| `api_rs_client_jks_pass`                        |
| `api_rs_client_jks_pass_encoded`                |
| `api_rs_jks_base64`                             |
| `api_test_client_secret`                        |
| `encoded_ldapTrustStorePass`                    |
| `encoded_ox_ldap_pw`                            |
| `encoded_oxtrust_admin_password`                |
| `encoded_salt`                                  |
| `encoded_shib_jks_pw`                           |
| `gluu_ro_client_base64_jwks`                    |
| `gluu_ro_encoded_pw`                            |
| `idp3EncryptionCertificateText`                 | 
| `idp3EncryptionKeyText`                         |
| `idp3SigningCertificateText`                    |
| `idp3SigningKeyText`                            |
| `idpClient_encoded_pw`                          |
| `ldap_pkcs12_base64`                            |
| `ldap_ssl_cacert`                               |
| `ldap_ssl_cert`                                 |
| `ldap_ssl_key`                                  |
| `ldap_truststore_pass`                          |
| `oxauthClient_encoded_pw`                       |
| `oxauth_jks_base64`                             |
| `oxauth_openid_jks_pass`                        |
| `oxauth_openid_key_base64`                      | 
| `pairwiseCalculationKey`                        |
| `pairwiseCalculationSalt`                       |
| `passportSpJksPass`                             |
| `passportSpKeyPass`                             |
| `passport_rp_client_base64_jwks`                |
| `passport_rp_client_cert_base64`                |
| `passport_rp_client_jks_pass`                   |
| `passport_rp_jks_base64`                        |
| `passport_rs_client_base64_jwks`                |
| `passport_rs_client_jks_pass`                   |
| `passport_rs_client_jks_pass_encoded`           |
| `passport_rs_jks_base64`                        |
| `passport_sp_cert_base64`                       |
| `passport_sp_key_base64`                        |
| `radius_jks_base64`                             |
| `radius_jwt_pass`                               |
| `scim_rp_client_base64_jwks`                    |
| `scim_rp_client_jks_pass`                       | 
| `scim_rp_client_jks_pass_encoded`               | 
| `scim_rp_jks_base64`                            | 
| `scim_rs_client_base64_jwks`                    |
| `scim_rs_client_jks_pass`                       |
| `scim_rs_client_jks_pass_encoded`               |
| `scim_rs_jks_base64`                            |
| `scim_test_client_secret`                       |
| `shibIDP_cert`                                  |
| `shibIDP_jks_base64`                            |
| `shibIDP_key`                                   |
| `shibJksPass`                                   |
| `ssl_cert`                                      |
| `ssl_cert_pass`                                 |
| `ssl_key`                                       |
