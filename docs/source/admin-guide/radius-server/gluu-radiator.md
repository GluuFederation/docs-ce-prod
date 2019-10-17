# Gluu Radiator

## Overview 

Gluu Radiator is an authentication plugin for [Radiator](https://radiatorsoftware.com/products/radiator/), a robust AAA server built for ISPs and carriers. With this plugin, the Gluu Server can be used for authentication and single sign-on (SSO) to RADIUS applications like VPN and Wi-fi.  

!!! Attention 
    This plugin does not handle RADIUS `Accounting-Request` packets, and simply returns `Access-Accept` for these packets.

## Prerequisites

### Perl
[Radiator](https://radiatorsoftware.com/products/radiator/) and its plugins are written in Perl. Consult the [Radiator documentation](https://open.com.au/radiator/ref.pdf) for information about how to install Perl and Radiator. 

In addition to Perl and the Perl modules Radiator is dependent upon, this authentication plugin has the following Perl module dependencies:

- `Data::UUID`
- `Encode`
- `Crypt::JWT`
- `HTTP::Async`
- `HTTP::Request`
- `JSON`

If using [ActiveState Perl](https://www.activestate.com/products/activeperl/), modules can be installed using the command:

```
ppm install <module_name>
```

If using Perl on Linux or [Strawberry Perl](http://strawberryperl.com/), modules can be installed using the command:

```
cpan <module_name>
```

!!! Attention
    We recommend installing Radiator on Linux, since some Perl module dependencies are difficult to get working on Windows. 

### OpenSSL 
A working OpenSSL installation is required to generate keys used to authenticate against the Gluu Server.

## Gluu Server Configuration

First make sure the Gluu Server is properly configured to support Radiator. 

### Gluu Radius Installation

Although not used in this case in its capacity as a RADIUS server, Gluu Radius, during installation, comes with all the components required to make the GluuRadiator plugin work seamlessly with Gluu Server.

Install Gluu Radius by following the instructions [here](./gluu-radius.md). 

If Radiator and the Gluu Server will run on the same system, one additional step needs to be taken: configure Gluu Radius to use different listening ports than the ones Radiator will use. Instructions can be found [here](./gluu-radius.md#basic-configuration).

### Authentication Keys Generation 

The plugin, same as Gluu Radius uses private key JWT authentication to perform authentication against the Gluu Radius Server. This implies the usage of private and public keys. In this section, we'll generate them. The examples here will assume generation of an 2048 RSA KeyPair , and the signing algorithm used will be RS512.

1. Generate the private key. Create or use an existing directory, and from the terminal , run the following command:
    
    ```
    openssl genrsa -aes256 -out gluu-radiator-pkey.pem 2048
    ```
    
    A passphrase (password) will be prompted for. Use a password of relatively good complexity and keep it safe. Make sure the private key is not world-readable.

1. Generate the public key. From the working directory mentioned above, run the following command:

    ```
    openssl rsa -in gluu-radiator-pkey.pem -outform PEM -pubout -out gluu-radiator-pubkey.crt
    ```
    
    Enter the passphrase from step `1` when prompted for a passphrase

### Gluu RO OpenID Configuration 

We will first generate a JWK (JSON Web Key) using [this tool](https://russelldavies.github.io/jwk-creator/). Open the tool in your browser. Set `Public Key Use` to `Signing` , `Algorithm` to `RS512` and `Key ID` to `gluu-radiator-auth-sign-rs-512`. A JWK will be generated. This tool only supports RSA keys.

A more unique `Key ID` can be chosen too. Copy the contents of the public key in `gluu-radiator-pubkey.crt` and paste 
in the `PEM Encoded Key` section.

Now, log in to Gluu Server from the browser. Navigate to `OpenID Connect` > `Clients` and select `Gluu RO OpenID Client`.

Click on the `Encryption Signing Settings Tab`. Add the generated JWK to the existing ones in the `JWKS` section. 
It is recommended that the contents of the `JWKS` section be copied in a text editor before performing this operation, 
then re-copied into the `JWKS` section. Save the effected changes changes.

## Plugin Installation and Configuration 
Radiator installation is covered in the [user manual](https://open.com.au/radiator/ref.pdf) provided during purchase of evaluation and is therefore out of the scope of this document. 

As for the plugin itself, the only file needed is `AuthGLUU.pm` in the `Radius` directory. It has to be copied into the 
`Radius` directory where Radiator will be installed. 

In the Radiator configuration file, add the plugin as an authenticator, as shown below alongside the Plugin parameters
(will be explained later).

```
<Handler>
     <AuthBy GLUU>
          gluuServerUrl https://gluu.local/
          clientId xxxxxxxxxxx
          signaturePkeyPassword admin
          signaturePkey file:"path_to_key"
          signaturePkeyId gluu-radiator-auth-sign-rs512
          signatureAlgorithm RS512
          sslVerifyCert yes
     </AuthBy>
</Handler>
```

### Plugin Configuration Parameters 
The `AuthGLUU` plugin takes many parameters. They will be described below. 

- `acrValue`. This is an optional string parameter containing the name of `Resource Owner Password Grant Interception Script`s which will be invoked during authentication. Default: `super_gluu_ro`.

- `scopes`. This is an optional string parameter containing the openId scopes which will be used invoked during 
authentication. Default: `openid`,`super_gluu_ro_session`.

- `gluuServerlUrl`. This is a mandatory string parameter containing the URL of the Gluu Server Instance this plugin 
will authenticate against.

- `clientId`. This is a mandatory string parameter containing the clientID of the `Gluu RO OpenID Client` OpenID client 
configured in [this section](./gluu-radiator.md#gluu-ro-openid-configuration).

- `signaturePkey`. This is a mandatory string parameter containing the contents of the private key used for token authentication. Note as, in the above sample configuration, we used the notation `file:"/file/path/"` to read the contents.

- `signaturePkeyPassword`. This is a mandatory string parameter containing the password of the `signaturePkey` parameter.
   It goes without saying, since the configuration file contains such a sensitive parameter, it should be set to have the 
   appropriate permissions.

- `signaturePkeyId`. This is a mandatory string parameter containing the Key ID of the JWK public key previously generated. In the previous section, the value was set to `gluu-radiator-auth-sign-rs-512`.

- `signatureAlgorithm`. This is a mandatory string parameter containing the JWA algorithm used for token endpoint authentication signature verification. It must match the `JWS alg Algorithm for Authentication method to Token Endpoint:` parameter for the corresponding OpenID client.

- `sslVerifyCert`. This is an optional flag parameter which can take the values `yes` or `no`. If set to `yes` SSL certificate verification is turned on. If set to `no` SSL certification is turned off. Default value is `yes`.

- `sslCAPath`. This is an optional string parameter which contains the path of a directory containing CA certificates used for validation. See the OpenSSL documentation for more information.

- `sslCAFile`. This is an optional string parameter which contains the path to a file containing the CA certificate for the server. This may come in handy if the SSL certificate verification cannot be turned off (bad idea all the same), and the server certificate is self-signed.

- `sslVerifyCnScheme`. This is an optional string containing the scheme used to perform certificate verification. See the perl package `IO::Socket::SSL` for details.

- `sslVerifyCnName`. This is an optional string containing the name which is used in hostname verification. See the per l package `IO::Socket::SSL` for details.

- `unreachableServerAction`. This is an optional string containing the action to take as long as the Gluu Server is unreachable. The valid values are `accept`, `ignore` and `reject` , representing the various Radius return values for each request , notably `Access-Accept` , `Access-Ignore` and `Access-Reject`. Default value is `reject`.

- `maxRequests`. This is an optional integer containing the maximum number of simultaneous requests to the Gluu Server.

- `httpRequestTimeout`. This is an optional integer containing the time (in seconds) after which an http request will be 
marked as failed

- `httpMaxRequestTime`. This is an optional integer containing the maximum time (in seconds) an http request can last.

- `authTimeout`. This is an optional integer containing the maximum time (in seconds).an entire authentication cycle can last. Set larger values if authentication is expected to take (too) long. Default of 30 seconds

- `pollInterval`. This is an optional integer containing the interval (in seconds) responses will be polled from the server via HTTP. Default is 1 second

## Testing 

1. Create a user or use an existing user on Gluu Server. Make sure the user has at least one enrolled [Super Gluu](https://super.gluu.org) device associated with their account.    

1. Run Radiator (see Radiator documentation)    

1. Use a RADIUS client (e.g. `NTRadPing`) to attempt to authenticate. A Super Gluu authentication prompt should appear on the user's device. Tap `Approve` to proceed with authentication. Radiator will then return an `Access-Accept`response.









