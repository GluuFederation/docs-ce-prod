# Replace Expired Key Files

## oxAuth

### Backup

 - Back up the existing `/etc/certs/oxauth-keys.jks` and `/etc/certs/oxauth-keys.json` 
 - Back up the full `o=gluu` LDAP data
 
### Manually generate and apply key
 
1. Log in to the chroot - `gluu-serverd login`
1. Backup existing `oxauth-keys.jks` and `oxauth-keys.json` from `/etc/certs/`
1. Grab the password/keypass/keypasswd of your oxauth jsk with: `cat /install/community-edition-setup/setup.properties.last | grep -i oxauth_openid_jks_pass`
1. Replace above `oxauth_openid_jks_pass` in below command and run command.
    
```
/opt/jre/bin/java -Dlog4j.defaultInitOverride=true -cp "/home/jetty/lib/*" org.gluu.oxauth.util.KeyGenerator -keystore oxauth-keys.jks -keypasswd <oxauth_openid_jks_pass> -sig_keys RS256 RS384 RS512 ES256 ES384 ES512 PS256 PS384 PS512 RSA1_5 -enc_keys RSA1_5 RSA-OAEP -dnname "CN=oxAuth CA Certificates" -expiration 365 > oxauth-keys.json
```

1. `cp oxauth-keys.j* /etc/certs/`
1. Inject the new key in LDAP (Gluu CE Database) as well
1. Download and install JXplorer in your local machine http://jxplorer.org/downloads/users.html
1. Create a tunnel to the server - `ssh -L 1636:localhost:1636 [username]@[server_host]`
1. Open JXplorer and fill it per the below screenshot
1. Get the LDAP password inside chroot `cat /install/community-edition-setup/setup.properties.last|grep 'ldapPass='`. Use this password in JXplorer connection and click on `OK` button and in next popup click on `This Session Only` button.

      ![ldap-jsxplorer-connection](https://user-images.githubusercontent.com/2329776/73589144-71337f80-44f8-11ea-86c0-9b9dadc305d3.png)
      
1. Next is to copy content of `oxauth-keys.json` into LDAP. Navigate to path as per below screenshot and replace content in the `oxAuthConfWebKeys` field. `gluu > configuration > oxauth` --> `Table Editor` tab --> click on `oxAuthConfWebKeys` value --> Replace value --> click on `Submit`.
      
      ![ldap_oxauth_key_replace](https://user-images.githubusercontent.com/2329776/73589260-e0f63a00-44f9-11ea-91f9-c6aab2cf1609.png)
      
1. Exit from chroot
1. `gluu-serverd stop`
1. `gluu-serverd start`

## SCIM

When your SCIM service is protected with UMA, your client application uses the `scim-rp.jks` file bundled with your Gluu Server. Additionally, the server uses the `scim-rs.jks` file. These Java Keystore files are generated upon installation and expire after one year. 

The following steps are required to update the keystores so that your server and client behave properly after expiration:

First, log in to the Gluu Server chroot.

Create a temporary folder (e.g. `mkdir tmp`) and `cd` to it.
   
Create two JKS files using these commands: 

```  
keytool -genkey -alias dummy -keystore fresher-scim-rp.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
    
keytool -delete -alias dummy -keystore fresher-scim-rp.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates' 
   
keytool -genkey -alias dummy -keystore fresher-scim-rs.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
    
keytool -delete -alias dummy -keystore fresher-scim-rs.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
```  
    
This will create two files: `fresher-scim-rp.jks` and `fresher-scim-rs.jks`. You may prefer to change the names and provide a password other than "secret". The files can have different passwords.
    
Add suitable keys and export two JSON files: 
  
```  
java -cp '/home/jetty/lib/*' org.gluu.oxauth.util.KeyGenerator \  
-keystore fresher-scim-rp.jks -keypasswd secret \  
-sig_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-enc_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-dnname "CN=oxAuth CA Certificates" \  
-expiration 365 > keys-rp.json  
  
java -cp '/home/jetty/lib/*' org.gluu.oxauth.util.KeyGenerator \  
-keystore fresher-scim-rs.jks -keypasswd secret \  
-sig_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-enc_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-dnname "CN=oxAuth CA Certificates" \  
-expiration 365 > keys-rs.json  
```  
  
In this example, the files expire in 365 days. Replace "secret" with the correct passwords.
  
Verify that two files with **valid** JSON content have been created. Otherwise, check that you properly followed the instructions.
  
Log into oxTrust and navigate to`OpenId connect` > `Clients` > `SCIM Requesting Party Client`. Scroll down to `JWKS` text box and paste the contents of the `keys-rp.json` file. Back up previous content before applying the edit. 
  
In oxTrust, go to `OpenId connect` > `Clients` > `SCIM Resource Server Client`. Scroll down to the `JWKS` text box and paste the contents of the `keys-rs.json` file. Back up previous content before applying the edit.
  
Compute the encrypted password used for file `fresher-scim-rs.jks`. While logged into the Gluu Server chroot, type `python` and press Enter. Paste the following in the interpreter:
  
```
import base64
from pyDes import *

data = '<password>'
engine = triple_des('<salt>', ECB, pad=None, padmode=PAD_PKCS5)
data = data.encode('ascii')
en_data = engine.encrypt(data)
print base64.b64encode(en_data) 
```
 
  - Replace `<password>` with the password you used for the `fresher-scim-rs` keystore. Replace `<salt>` with the value of `encodeSalt` found in the `/etc/gluu/conf/salt` file.

  - The last line printed has the value needed. Type `quit()` to return to the prompt.

In oxTrust, visit `Configuration` > `JSON configuration` > `oxTrust configuration`. Update the "scimUmaClientKeyStoreFile" field to point to the new keystore (e.g. `/etc/certs/fresher-scim-rs.jks`), and paste the value obtained in the previous step in the`scimUmaClientKeyStorePassword` field.  Press "Save" at the bottom of the page.

Update your client's SCIM application to use `fresher-scim-rp.jks` with its corresponding password and test it.

Finally, remove the `tmp` directory in your server.

Something went wrong? Feel free to open a [support ticket](https://support.gluu.org).
