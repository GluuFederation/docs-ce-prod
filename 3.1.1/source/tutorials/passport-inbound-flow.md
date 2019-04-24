# Inbound SAML Tutorial

## Overview

This tutorial offers a step-by-step guide for setting up a basic proof-of-concept environment showcasing an Inbound SAML user authentication flow. Refer to general documentation describing each component for more details.

## Foreword

For the sake of illustration we'll use the following three abstract servers:

 - `[passport_dns_name]` is the host where Gluu Server v3.1.4 with Shibboleth IDP and Passport components is installed
 
 - `[remote_idp_dns_name]` is another Gluu Server v3.1.4 instance with Shibboleth IDP installed which will serve as remote IDP in this example
 
 - `[sp_dns_name]` is the remote SP Gluu Server with the Shibboleth SP v2.6.1 installed

Whenever you see any of the three placeholders in the text below, you'll have to substitute them with real DNS names used for corresponding machines in your environment. 

You also need to make sure those names can be resolved at all three server machines, plus the device that will be used as the user's machine during the test (the device where web browser used to access servers is running), either through enlisting them in DNS server's registry, or by adding them to `hosts` files at each of the machine. 

In case of Gluu Server machine(s), it needs to be done inside container, not outside of it.

!!! Warning  
    Ensure that clocks are perfectly synced between all participating machines so the flow works without issues. An NTP daemon running on each machine is the easiest solution to this problem.

!!! Warning  
    The setup described here uses minimalistic configuration developed with the sole purpose of showcasing how end-to-end Passport-driven inbound SAML flow functions in Passport. It is thus strongly discouraged to leave all involved applications running longer than they are needed for the sake of showcasing without taking additional measures to secure the setup.

## Configure `[sp_dns_name]` host

We'll need Shibboleth SP v3.x and Apache running on the `[sp_dns_name]` machine to procceed.

### Install and configure Apache

#### Installation

Run these commands to install required packages:

```
# yum install httpd mod_ssl
# service httpd start
# service iptables stop
```

#### Configuration

1. Issue a new self-signed certificate:
    - `# mkdir /etc/httpd/ssl`
    - Run this command to create a certificate;  and : `# openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/httpd/ssl/apache.key -out /etc/httpd/ssl/apache.crt`
    - When asked for a "Common Name", provide `[sp_dns_name]`
1. Prepare the directory/files layout for the test VirtualHost:
    - `# mkdir /var/www/html/test_shib_protected_site`
    - `# mkdir /var/www/html/test_shib_protected_site/protected_dir`
    - `# echo "Hello I'm a public page"'!' > /var/www/html/test_shib_protected_site/index.html`
    - `# echo "Hi I'm a hidden page"'!' > /var/www/html/test_shib_protected_site/protected_dir/hidden.html`
    - `# chown -R apache:apache /var/www/html/test_shib_protected_site/`
1. Find the default "VirtualHost" definition in `/etc/httpd/conf.d/ssl.conf` (if present), and enclose it in "IfDefine" clause to not meddle with our custom VHost, as shown below:

    ```
      <IfDefine DontIgnoreDefaultVHost>
      <VirtualHost _default_:443>
  
        ...

      </VirtualHost>
      </IfDefine>
    ```

1. Create `/etc/httpd/conf.d/test_site.conf` file with contents provided below:

    ```
      <VirtualHost 0.0.0.0:443>
          DocumentRoot /var/www/html/test_shib_protected_site/
          ServerName [sp_dns_name]:443
      
          SSLEngine on
          SSLProtocol -ALL +TLSv1
          SSLCipherSuite EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA384:EECDH+ECDSA+SHA256:EECDH+aRSA+SHA384:EECDH+aRSA+SHA256:EECDH+aRSA+SHA384:EECDH:EDH+aRSA:HIGH:!MEDIUM
          SSLCertificateFile /etc/httpd/ssl/apache.crt
          SSLCertificateKeyFile /etc/httpd/ssl/apache.key
          UseCanonicalName On
          <Directory /var/www/html/test_shib_protected_site>
          AllowOverride All
          </Directory>

          <Location /protected_dir>
            AuthType shibboleth
            ShibRequestSetting requireSession 1
      #       require shib-session
            require valid-user
          </Location>
      </VirtualHost>
    ```
    
1. Restart the httpd service: `# service httpd restart`


#### Testing

Access `https://[sp_dns_name]/index.html` with your browser - you should see the welcome text of the public page you created before.

### Install and configure Shibboleth SP v3.x in CentOS 6

#### Installation

Run these commands to install the required packages:

```
# cd /etc/yum.repos.d
# wget http://download.opensuse.org/repositories/security:/shibboleth/CentOS_CentOS-6/security:shibboleth.repo
# yum install shibboleth
# service shibd start
# chkconfig shibd on
```

#### Configuration

Edit `/etc/shibboleth/shibboleth2.xml`:

  - In "ApplicationDefaults" element change "entityID" property to "https://[sp_dns_name]/shibboleth"
  - Within the "Sessions" element find "SSO" child element and change its "entityID" property to "https://[passport_dns_name]/idp/shibboleth"
  - Right after "Sessions" element find a section where "MetadataProvider" elements are grouped, and add element provided below:
    ```
            <MetadataProvider type="XML"
                url="https://[passport_dns_name]/idp/shibboleth"
                backingFilePath="[passport_dns_name].metadata.xml"
                maxRefreshDelay="7200"/>
    ```
  - Restart `shibd` service: `# service shibd restart`
  - Make sure it's started with no critical issues by checking `/var/log/shibboleth/shibd.log` and running `# service shibd status`

#### Testing combined Apache + Shibboleth SP setup

Access `https://[sp_dns_name]/protected_dir/hidden.html` with your browser - you should be sent to your Gluu Server (`[passport_dns_name]`) machine;  it will respond with an error page, as it's not yet prepared to serve such a request.

Make sure you've achieved the described result before proceeding further.

## Configure `[passport_dns_name]` host

### Install Passport (if needed)

Passport is available as an optional component during [Gluu Server installation](https://gluu.org/docs/ce/installation-guide/). If it's missing in your instance, you can add it by performing the following actions (requires Internet access):

1. Move into Gluu Server's container

1. `# cd /install/community-edition-setup/`

1. `wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/post-setup-add-components.py`

1. `# chmod +x post-setup-add-components.py` 

1. Run `# ./post-setup-add-components.py -addpassport`

1. Run `# runuser -l node -c "cd /opt/gluu/node/passport/&&PATH=$PATH:/opt/node/bin npm install -P"`

### Enable Passport

1. Enable the required custom scripts:    

    - In oxTrust, navigate to `Configuration` > `Custom scripts`          
    - Navigate to the `Person Authentication` tab, expand the script labelled `passport_saml`, check `enabled`, and click `Update`  
    - Navigate to the `UMA RPT Policies` tab, expand the script labelled `scim_access_policy`, check `enabled`, and click `Update`       
      
1. Enable Passport support:    

    - In oxTrust navigate to `Configuration` > `Organization configuration` > `System configuration`    
    - For `Passport support` choose `Enabled`    
    - Click `Update`    

### Configure SAML authentication strategy in Passport

Passport expects to find information about supported remote SAML IDPs in the configuration file at `/etc/gluu/conf/passport-saml-config.json`. Every supported external IDP should be added as a separate JSON object.

Copy the default file into a safe location in case you need it later, clear its contents and put the following structure into it:
 
```
{
  "idp1": {
    "entryPoint": "https://[remote_idp_dns_name]/idp/profile/SAML2/POST/SSO",
    "issuer": "urn:test:pass-saml:showcase",
    "identifierFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
    "authnRequestBinding": "HTTP-POST",
    "additionalAuthorizeParams": "",
    "skipRequestCompression": "true",
    "logo_img": "",
    "enable": "true",
    "cert": "MIIDbDCCAlQCCQCuwqx2PNP....SEE.BELOW.......YsMw==",
    "reverseMapping": {
      "email": "email",
      "username": "urn:oid:0.9.2342.19200300.100.1.1",
      "displayName": "urn:oid:2.16.840.1.113730.3.1.241",
      "id": "urn:oid:0.9.2342.19200300.100.1.1",
      "name": "urn:oid:2.5.4.42",
      "givenName": "urn:oid:2.5.4.42",
      "familyName": "urn:oid:2.5.4.4",
      "provider": "issuer"
    }
  }
}
```

To acquire the value for the "cert" property in the structure above, SSH into `[remote_idp_dns_name]` host, move into the Gluu Server's container and execute this command: `# cat /etc/certs/idp-signing.crt | grep -v '^---' | tr -d '\n'; echo`
It will return a single-string representation of the remote IDP's signing certificate you need.

Now restart Passport's service and make sure it starts with no errors and is running:
  - `# service passport restart`
  - `# service passport status`

Once configuration is successfully validated, Passport will automatically generate SAML SP metadata for the single IDP listed in `passport-saml-config.json` under `/opt/gluu/node/passport/server/idp-metadata/` and will publish it at a URL like `https://[passport_dns_name]/passport/auth/meta/idp/idp1` - you'll need this metadata for one of the next steps. This IDP will also be displayed on the selector pane located at the right on Passport's login page.

### Configure Trust Relationship between `[passport_dns_name]` and `[sp_dns_name]` hosts

1. Download metadata of the Shibboleth SP you configured before at `https://[sp_dns_name]/Shibboleth.sso/Metadata` and save it as `gluu_shibboleth_sp_metadata.xml`
1. Log in to oxTrust at `[passport_dns_name]`
1. Move to `SAML` > `Trust Relationships` page
1. Create a new trust relationship using the metadata you've just downloaded
1. Check "Configure Relying Party", add the "SAML2SSO" profile to the list and configure it as follows:
    - signResponses: conditional
    - signAssertions: never
    - signRequests: conditional
    - encryptAssertions: never
    - encryptNameIds: never
    
1. Release the "transientID", "email" and "Username" attributes

## Test the bond you've created between `[passport_dns_name]` and `[sp_dns_name]` hosts

So far the regular SAML Trust Relationship is formed between those two. To test it, wait a few minutes until IDP loads the updated configuration and access `https://[sp_dns_name]/protected_dir/hidden.html` again. You'll have to be redirected to `[passport_dns_name]` and land at the default oxAuth's login page this time. Log in as any user there, and you'll have to be sent back to `[sp_dns_name]` and be able to see the welcome text of the `hidden.html` page.

Don't proceed further until this flow is fully functional.

## Configure `[remote_idp_dns_name]` host

1. Create [Trust Relationship](https://gluu.org/docs/ce/admin-guide/saml/#create-a-trust-relationship) with Passport running at `[passport_dns_name]`:
    - Download metadata of the SP Passport created for this remote IDP published at `https://[passport_dns_name]/passport/auth/meta/idp/idp1` and save it as 'gluu_passport_sp_metadata.xml'
    - Log in to oxTrust at `[remote_idp_dns_name]`
    - Move to `SAML` > `Trust Relationships` page
    - Create a new trust relationship using the metadata you've just downloaded
    - Check "Configure Relying Party", add "SAML2SSO" profile to the list and configure it as follows:
        - signResponses: conditional
        - signAssertions: never
        - signRequests: conditional
        - encryptAssertions: never
        - encryptNameIds: never
    - Release "transientID", "email" and "Username" attributes
1. Move to `Users` > `Manage People` page, locate the user you intend to log in with during the test phase and make sure it has non-empty and unique values for "email" and "Username" attributes. Both of the values ideally must not match corresponding attributes for any user at the `[passport_dns_name]` (thus it's not recommended to use the default "admin" user as a test account)
1. Log out of the web UI to prevent the "admin" session from providing user attributes in future tests

## Test the end-to-end flow from `[sp_dns_name]` through `[passport_dns_name]` to `[remote_idp_dns_name]` (and back)

Two different browsers must be installed on your personal machine that you use to access all three mentioned hosts. Before proceeding with the final test, it's strongly recommended to clear all cookies still remaining in your browser(s) related to all three machines participating in this flow. Then follow these steps to enable Passport-SAML authentication method and test your completed setup:

1. In your first browser, log in to the oxTrust web UI of `[passport_dns_name]` as administrator and leave this session running. You'll need it as an emergency backdoor if anything goes wrong, to revert your authentication settings. Make sure this session won't be terminated due to inactivity!
1. In your second browser, log in to oxTrust web UI of `[passport_dns_name]` as administrator. From now on it will be your main working session
1. Move to `Configuration` > `Manage Authentication` > `Default Authentication Method`
1. Choose "passport_saml" for "Default acr" and click the "Update" button
1. Log out from this session (remember to keep you other browser's session running!) and wait for a minute
1. Access `https://[sp_dns_name]/protected_dir/hidden.html` again 

If everything is working as expected after step 6, you must be redirected to the `[passport_dns_name]` host for authentication. You must land at Passport's login page and see "idp1" authentication option in the selector pane to the right. When selected, it must send you to `[remote_idp_dns_name]` host where you'll have to log in as your test user, then you'll be sent back to `[passport_dns_name]` host and be logged in there automatically (it will auto-enroll an user entry for you). Finally you must be sent back to `[sp_dns_name]` host and be able to see the welcome text of the `hidden.html` page. 

In case it doesn't work, you probably will want to revert your authentication settings changes and resort to troubleshooting:

1. Use the still active admin session at `[passport_dns_name]` host in your first browser 
2. Move to `Configuration` > `Manage Authentication` > `Default Authentication Method`
3. Choose "auth_ldap_server" for "Default acr" and click the "Update" button

