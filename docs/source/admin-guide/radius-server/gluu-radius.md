# Gluu Radius

## Gluu Radius Overview
  The Gluu Server now ships with a [radius](https://en.wikipedia.org/wiki/RADIUS) server called
Gluu Radius. It is based on the [tinyradius](http://tinyradius.sourceforge.net/) java library. 
It supports radius authentication, but does not provide radius accounting support. Radius accounting 
packets are simply ignored.

## Installing Gluu Radius 
  Gluu Radius ships with Gluu CE as from version 4.0. Installation is straightforward. 
During the Gluu Server 4.0 CE installation , while [running setup.py](../../installation-guide/install.md#run-setuppy),
simply select `Y` when you are asked to install Gluu Radius.

## Performance Considerations 
As said before, the Gluu Radius server is based on the tinyradius java library. 
The library uses a single threaded, synchronous model to handle requests. 
This implies significant performance  degradation when handling a large volume of requests, or 
long lived requests. That said , Gluu Radius *should not be used in a production setting*. 
If you are interested in handling a large volume radius requests in production , consider purchasing 
[radiator](https://radiatorsoftware.com/products/radiator/) and using [our plugin](./gluu-radiator.md)
for authentication.


## The Gluu Radius Service 
Gluu Radius basically runs as a service from within the 
linux container. There are some configuration settings which require a service restart,
which is why we're mentioning the service here and the commands to start/stop it.
The service name is `gluu-radius` and you will have to be logged into the gluu container 
in order to start/stop it. 

### Starting the service 
Below are the commands to start the Gluu Radius Service for various platforms.

#### Ubuntu Server 16.x.x and 18.x.x
```
# service gluu-radius start
```

#### CentOS 7.x and RedHat 7.x
```
# systemctl start gluu-radius
```

### Stopping the service 
Below are the commands to stop the Gluu Radius Service for various platforms.

#### Ubuntu Server 16.x.x and 18.x.x
```
# service gluu-radius stop
```

#### CentOS 7.x and RedHat 7.x
```
# systemctl stop gluu-radius
```

## Gluu Radius Configuration 
 Installing Gluu Radius will give you access to a sidebar menu item on the oxTrust UI called `Radius` which 
can be used to perform the following operations:
  * Configure the running instance of gluu-radius 
  * Add/Edit/Remove NAS/Radius clients .

### Basic Configuration 
 From the oxTrust UI , go to `Radius > Server` Configuration and select the `Basic Configuration` tab.
 You can configure the following:
   - `Authentication Listen Port`. This is the port on which the server listens for authentication requests.
   - `Accounting Listen Port`. This is the port on which the server listens list accounting requests. As we 
      said before , currently , the server simply ignores accounting packets.
   - `Authentication Timeout` , This is the maximum amount of time in milliseconds between when an authentication
     request is initiated and the user approves authentication. This applies only for long lived two-factor 
     authentication based requests (e.g. Super-Gluu).
  
> Note: A change to any of these configuration parameters will require a restart of the `gluu-radius`
> service for the changes to take effect.
> Also , make sure that the ports you select for authentication and accounting are actually open.

![gluu-radius-basic-config](../../img/admin-guide/radius-server/gluu-radius-basic-config.png).

### OpenID Configuration 
 From the oxTrust UI , go to `Radius > Server Configuration` and select the `OpenID Configuration` tab. 
 You can configure the following:
   - `Acr Value`. Gluu Radius relies on a custom script of type `Resource Owner Password Credentials`
     You can select another script of the same type that can be used for authentication within certain
     constraints which will be given later.
   - `OpenID Client`. Gluu Radius relies on an OpenID client for authentication. You may specify another
     client here,  but this is also possible within certain constraints which will be given later.
   - `OpenID Scopes`. These are the scopes used during the password grant token request. For proper operation, 
      the scope list *must* contain the `openid` scope.
> Note : A change to any of these configuration parameters will require a restart of the `gluu-radius`
> service for the changes to take effect.
![gluu-radius-openid-config](../../img/admin-guide/radius-server/gluu-radius-openid-config.png)

### Radius Clients 
 From the oxTrust UI , go to `Radius > Radius Clients`. You will be greeted with a list of Radius / Nas Clients
 which are authorized to authenticate via the radius server.
 Clicking on `Add Radius Client` will allow you to add a new Radius Client. 
 Clicking on an existing client's name will allow you to edit the client's details.
 You can also select one or more radius clients and delete them.
![gluu-radius-clients](../../img/admin-guide/radius-server/gluu-radius-clients.png)

### Adding/Updating A Radius Client 
From the oxTrust UI, go to 'Radius > Radius Clients' , then click on `Add Radius Client` and specify the following:
  - `Client Name`. An easy mnemonic to recognize the client. 
  - `Ip Address/Network`. You can either specify an IPv4 address here (xxx.xxx.xxx.xxx) or a CIDR subnet
    (xxx.xxx.xxx.xxx/xxx). The CIDR notation will match all Radius/NAS clients originating from that network. 
  - `Client Secret`. The Radius Client's secret.
  - `Priority` . Radius clients are matched by the gluu-radius not only by Ip Address/Network  but also by priority, 
     so, if two entries _may_ match for one client (Ip Address/Network) , the entry with the highest priority will be selected. 
![gluu-radius-add-client](../../img/admin-guide/radius-server/gluu-radius-add-client.png)

## Advanced Topics 
This section covers advanced configuration topics. They are optional and can be skipped.

### The Gluu Radius configuration File 
 The Gluu Radius configuration file can be found under `/etc/gluu/conf/radius/gluu-radius.properties` 
in the linux container. There are a couple things you can change from the configuration file.

#### Changing the algorithm used for JWT authentication
By default `RS512` (RSASSA-PKCS1-v1_5 using SHA-512) is the algorithm used by Gluu Radius for authentication.
First, from the oxTrust UI , go to the configuration settings for the OpenID client used by Gluu Radius
(see `OpenId Configuration` in this document) and go to the `Encryption/Signing` Tab.
Change the option `JWS alg Algorithm for Authentication Method to Token Endpoint` to the algorithm of your choice.
The algorithm *must* be a keypair algorithm.
In the JWKS section (or in your jwks if you provided a url), copy the `kid` corresponding to the algorithm you selected,
and change the following line in the gluu radius configuration file.

```
radius.jwt.auth.keyId = <kid>
```
Once you are done , restart `gluu-radius`.

#### Using an external jwks 
Using an external jwks requires you pasting the contents of the jwks into the `JWKS` section in the `Encryption/Signing` tab
of the OpenID client used by `gluu-radius` for authentication.
You also need to provide a keystore , which contains all of the keys , with each entry name having the corresponding `kid`
for each JWKS entry. Generation of a keystore file and/or a `JWKS` is outside the scope of this document.
You will need to change the following in the configuration file.
```
radius.jwt.keyStoreFile = <location of keystore file>
radius.jwt.auth.keyId = <kid of public key used for authentication>
radius.jwt.auth.keyStorePin = <encrypted pin for the keystore>
```
You can use the utility `/opt/gluu/bin/encode.py` to encrypt the plaintext keyStore password.


### Constraints on using a custom OpenID client and/or a custom authentication script 
There are a couple of constraints if you will like to use your own OpenID client or custom script to authenticate
using `gluu-radius`.

#### Constraints on using a custom OpenID client 
1. The client *must* support private key JWT authentication.
1. The client *must* have the `super_gluu_ro_session` scope or any scope which will add a `__session_id`
   claim containing an authenticated session id to the idtoken for `password` token grant requests.
1. The client *must* have the `password` grant type 
1. The client *must* be enabled to include claims in the Id Token.
1. The keys used in the jwks for the client need to be saved in a keystore and have `gluu-radius` point 
   to them as specified in the [section above](./gluu-radius.md#using-an-external-jwks).
You can take a look at the default OpenID client that ships with Gluu Radius to have an idea.

#### Constraints on using a custom authentication script
1. The script must be of type `Resource Owner Password Credentials` 
1. The script *must* accept and process a `__password` http post parameter containing the user's password and not the `password`
   http post parameter.
1. The script *must* accept and process a `__step` http post parameter.
   1. When `__step` is equal to `initiate_auth` , the custom script *must* authenticate the user using the provided credentials      and *must* create a session on the server (authenticated or not) and return the session id in the idtoken with a claim
      name of `__session_id`. If the user can't be authenticated, the script must return false. 
   1. When `__step` is equal to `verify_auth`, the custom script *must* get the http post parameter called `__session_id`
      and verify if the associated session is authenticated. If it's not authenticated , the script *must* return `false`.
You can take a look at the default Custom Script that ships with gluu radius to have an idea.






     

