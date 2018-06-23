# Replacing expired JKS files for SCIM

When your SCIM service is protected with UMA, your client application makes use of the file `scim-rp.jks` bundled with your Gluu Server. Additionally, in server side a file called `scim-rs.jks` is also used. This couple of Java Keystore files are generated upon installation and have an expiration time of one year. 

The following lists the steps required to update the keystores so that your server and client behave properly after expiration:

1. Login to Gluu server chroot (e.g `service gluu-server-3.1.3 login`)

1. Create a temporary folder to copy some files needed (e.g. `mkdir tmp`) and `cd` to it

1. Extract java libraries needed: `jar -xf /opt/gluu/jetty/oxauth/webapps/oxauth.war WEB-INF/lib`

1. `cd` to lib dir (e.g. `cd WEB-INF/lib`)

1. Set an environment variable as in the following: 
    
    ```
    JARS=bcprov-jdk15on-1.54.jar:bcpkix-jdk15on-1.54.jar:commons-lang-2.6.jar:commons-codec-1.7.jar:commons-cli-1.3.1.jar:commons-io-2.4.jar:jackson-core-2.8.10.jar:jackson-core-asl-1.9.11.jar:jackson-mapper-asl-1.9.11.jar:jackson-xc-1.9.13.jar:jettison-1.3.2.jar:oxauth-model-3.1.1.Final.jar:oxauth-client-3.1.1.Final.jar:log4j-api-2.8.2.jar:log4j-1.2-api-2.8.2.jar:log4j-core-2.8.2.jar

    export JARS
    ```
    
    Note this is a list of files which must exist already in the current directory. Ensure every file is found there. Pay special attention to specific version of files. As an example you may have to adjust `oxauth-model-3.1.1.Final.jar` to match the exact version of the file residing in `lib` (eg. `oxauth-model-3.1.3.Final.jar`).
    
1. Create two JKS files using this commands: 

    ```
    keytool -genkey -alias dummy -keystore fresher-scim-rp.jks -storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'

    keytool -delete -alias dummy -keystore fresher-scim-rp.jks -storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'
    
    keytool -genkey -alias dummy -keystore fresher-scim-rs.jks -storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'

    keytool -delete -alias dummy -keystore fresher-scim-rs.jks -storepass secret -keypass secret -dname 'CN=oxAuth CA Certificates'
    ```
    
    This will create two files: `fresher-scim-rp.jks` and `fresher-scim-rs.jks`. You may like using different names and provide a password other than "secret". Files can have different passwords.
    
1. Add suitable keys and export two json files: 

    ```
    java -cp $JARS org.xdi.oxauth.util.KeyGenerator 
		-keystore fresher-scim-rp.jks -keypasswd secret 
                -sig_keys RS256 RS384 RS512 ES256 ES384 ES512
                -enc_keys RS256 RS384 RS512 ES256 ES384 ES512
                -dnname "CN=oxAuth CA Certificates"
                -expiration 365 > keys-rp.json
                
    java -cp $JARS org.xdi.oxauth.util.KeyGenerator 
		-keystore fresher-scim-rs.jks -keypasswd secret 
                -sig_keys RS256 RS384 RS512 ES256 ES384 ES512
                -enc_keys RS256 RS384 RS512 ES256 ES384 ES512
                -dnname "CN=oxAuth CA Certificates"
                -expiration 365 > keys-rs.json
    ```

    In this example expiration of 365 days was used. Replace "secret" with right passwords.

1. Verify two files with **valid** json content have been created. Otherwise, check you are properly following the instructions.

1. Login to oxTrust and go to `OpenId connect` > `Clients` > `SCIM Requesting Party Client`. Scroll down to `JWKS` text box and paste the contents of file `keys-rp.json`. Back up previous content before applying the edit. 

1. In oxTrust, go to `OpenId connect` > `Clients` > `SCIM Resource Server Client`. Scroll down to `JWKS` text box and paste the contents of file `keys-rs.json`. Back up previous content before applying the edit.

1. Compute the encrypted password used for file `fresher-scim-rs.jks`. While logged in at Gluu Server chroot, type `python` and press Enter. Paste the following in the interpreter:
    
    ```
    import base64
    from pyDes import *
    
    data = '<password>'
    engine = triple_des('<salt>', ECB, pad=None, padmode=PAD_PKCS5)
    data = data.encode('ascii')
    en_data = engine.encrypt(data)
    print base64.b64encode(en_data)
    ```

    Replace `<password>` with the password you used for the `fresher-scim-rs` keystore. Replace `<salt>` with the value of `encodeSalt` found in file `/etc/gluu/conf/salt`

    The last line printed has the value needed. Type `quit()` to return to prompt.

1. In oxTrust, visit `Configuration` > `Json configuration` > `oxTrust configuration`. Update the field "scimUmaClientKeyStoreFile" to point to new keystore (e.g. `/etc/certs/fresher-scim-rs.jks`), andn paste the value obtained in previous step in the field "scimUmaClientKeyStorePassword".  Press "Save" at the bottom of the page.

1. Update your client SCIM application to use `fresher-scim-rp.jks` with its corresponding password and test it.

1. Finally, remove `tmp` dir in your server.

Something went wrong? Feel free to open a [support ticket](https://support.gluu.org).