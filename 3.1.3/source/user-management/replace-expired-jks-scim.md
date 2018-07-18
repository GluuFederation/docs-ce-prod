# Replacing expired JKS files for SCIM

When your SCIM service is protected with UMA, your client application uses the `scim-rp.jks` file bundled with your Gluu Server. Additionally, the server uses the `scim-rs.jks` file. These Java Keystore files are generated upon installation and expire after one year. 

The following steps are required to update the keystores so that your server and client behave properly after expiration:

First, log into the Gluu Server chroot (e.g. `service gluu-server-3.1.3 login`).

Create a temporary folder to copy some needed files (e.g. `mkdir tmp`) and `cd` to it.

Extract needed Java libraries: `jar -xf /opt/gluu/jetty/oxauth/webapps/oxauth.war WEB-INF/lib`.

`cd` to the lib directory (e.g. `cd WEB-INF/lib`).

Set an environment variable, as follows: 
    
```  
JARS=bcprov-jdk15on-1.54.jar:bcpkix-jdk15on-1.54.jar:commons-lang-2.6.jar:commons-codec-1.7.jar:commons-cli-1.3.1.jar:commons-io-2.4.jar:jackson-core-2.8.10.jar:jackson-core-asl-1.9.11.jar:jackson-mapper-asl-1.9.11.jar:jackson-xc-1.9.13.jar:jettison-1.3.2.jar:oxauth-model-3.1.3.Final.jar:oxauth-client-3.1.3.Final.jar:log4j-api-2.8.2.jar:log4j-1.2-api-2.8.2.jar:log4j-core-2.8.2.jar 

  export JARS
```  

This is a list of files which must exist already in the current directory. Ensure every file is found there. Pay special attention to specific version of files. Make sure that the version for `oxauth-model` and `oxauth-client` matches your version (3.1.3 here).
    
Create two JKS files using these commands: 

```  
/opt/jdk1.8.0_162/bin/keytool -genkey -alias dummy -keystore fresher-scim-rp.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
    
/opt/jdk1.8.0_162/bin/keytool -delete -alias dummy -keystore fresher-scim-rp.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates' 
   
/opt/jdk1.8.0_162/bin/keytool -genkey -alias dummy -keystore fresher-scim-rs.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
    
/opt/jdk1.8.0_162/bin/keytool -delete -alias dummy -keystore fresher-scim-rs.jks \
-storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'  
```  
    
This will create two files: `fresher-scim-rp.jks` and `fresher-scim-rs.jks`. You may prefer to change the names and provide a password other than "secret". The files can have different passwords.
    
Add suitable keys and export two JSON files: 
  
```  
/opt/jdk1.8.0_162/bin/java -cp $JARS org.xdi.oxauth.util.KeyGenerator \  
-keystore fresher-scim-rp.jks -keypasswd secret \  
-sig_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-enc_keys RS256 RS384 RS512 ES256 ES384 ES512 \  
-dnname "CN=oxAuth CA Certificates" \  
-expiration 365 > keys-rp.json  
  
/opt/jdk1.8.0_162/bin/java -cp $JARS org.xdi.oxauth.util.KeyGenerator \  
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

In oxTrust, visit `Configuration` > `Json configuration` > `oxTrust configuration`. Update the "scimUmaClientKeyStoreFile" field to point to the new keystore (e.g. `/etc/certs/fresher-scim-rs.jks`), and paste the value obtained in the previous step in the`scimUmaClientKeyStorePassword` field.  Press "Save" at the bottom of the page.

Update your client's SCIM application to use `fresher-scim-rp.jks` with its corresponding password and test it.

Finally, remove the `tmp` directory in your server.

Something went wrong? Feel free to open a [support ticket](https://support.gluu.org).
