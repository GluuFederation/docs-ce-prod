# Inbound identity using Apple Sign In

This tutorial offers a step-by-step guide to integrate Apple Sign In, an Apple feature that enables iOS and Mac users to sign in to apps and website using their Apple ID.

While steps covered in the [Inbound identity using OIDC and OAuth](../authn-guide/inbound-oauth-passport/) are enough to integrate any OIDC or OAuth compliant server, making Apple fit into the framework requires a lot more work due to the amount of configurations required by Apple and certain atypical behaviors of the authorization server itself. This guide was written to help you streamline the process.

## Pre-requisites

- No previous knowledge of [passport](../auth-guide/passport/) (the key Gluu server component for inbound identity) is required to follow this document, however, it is assumed your Gluu server has Passport already [enabled](../auth-guide/inbound-oauth-passport/#enable-passport).

- Ideally, your Gluu instance has to be publicly accessible to Internet. This is due to Apple URL verification processes. If this is a problem for your organization, it is possible to workaround it using proxy techniques. 

- It's not necessary to have a valid production SSL cert in your Gluu instance

- An [Apple developer account](https://developer.apple.com/programs/enroll/) is required

## Creating an Apple application

There are a number of configurations that must be performed using your Apple developer account before the actual integration takes place. [This](https://github.com/ananay/apple-auth/blob/master/SETUP.md) tutorial does a great job at explaining the steps required. As you go with it, ensure you collect the following elements:

- A service ID
- A team ID
- A key ID and a key file 

You will be prompted to enter a redirect URL. Please provide `https://<your-gluu-domain>/passport/server/auth/apple/callback`.

For domain verification purposes you will be given a file that it is supposed to be accessible at `https://<your-gluu-domain>/.well-known/apple-developer-domain-association.txt`. To do so follow the steps below:

1. SSH to your Gluu server
1. Copy the file to `/opt/gluu/jetty/oxauth/custom/static` inside chroot
1. In chroot, locate the Apache config file. In most cases it is `/etc/apache2/sites-available/https_gluu.conf`
1. At the bottom, near to a directive like `ProxyPass /.well-known/openid-configuration` add a new one this way:

    ```
    ProxyPass /.well-known/apple-developer-domain-association.txt http://localhost:8081/oxauth/ext/resources/apple-developer-domain-association.txt
    ```

1. Save the file and [restart](../operation/services.md#restart) Apache, eg. `# service apache2 restart`
1. Ensure the file is correctly loaded. Open a browser, and hit `https://<your-gluu-domain>/.well-known/apple-developer-domain-association.txt`

## Low level configurations

SSH to your Gluu server and copy the **key file** to `/etc/certs` inside chroot. 

### Install nicokaiser's passport-apple strategy

!!! Note:
    Skip this section if your Gluu version is 4.1 or higher

Next, let's add the passport strategy that allows us to "talk" to Apple identity provider:

1. Ensure the VM has Internet access. 
1. Backup passport folder, eg. `tar -zcf backup.tar.gz /opt/gluu/node/passport`
1. [Stop](../operation/services.md#stop) passport, eg. `# systemctl stop passport`
1. Switch to node user: `su - node`
1. Add the node executable to path: `$ export PATH=$PATH:/opt/node/bin`
1. `cd` to `/opt/gluu/node/passport`
1. Install the strategy, eg. `npm install @nicokaiser/passport-apple --save`. No errors should arise here, at most, warnings.
1. Switch back to root: `exit`
1. [Start](../operation/services.md#start) passport, eg. `# systemctl start passport`

### Add/Patch javascript files

!!! Note:
    Skip this section if your Gluu version is 4.1 or higher
    
Apple doesn't redirect the users' browsers to the callback URL (`redirect_uri`) once they login sucessfully, but makes a POST to the URL. This is not an expected behavior for and Oauth2 authorization server, so it requires adding support for this kind of custom behavior.

1. `cd` to `/opt/gluu/node/passport/server`
1. Replace files `providers.js` and `routes.js` using those found [here](https://raw.githubusercontent.com/GluuFederation/gluu-passport/version_4.1/server/providers.js) and [here](https://raw.githubusercontent.com/GluuFederation/gluu-passport/version_4.0.1/server/routes.js) respectively.
1. Copy this [file](https://github.com/GluuFederation/gluu-passport/raw/master/server/mappings/apple.js) to `/opt/gluu/node/passport/server/mappings`.


## Add Apple Sign In to supported identity providers

In this section we'll onboard Apple to the list of known providers for inbound identity.

1. Login to oxtrust UI with an administrative user
1. Go to `Passport` > `Providers` and click on `Add new provider`
1. For provider ID, enter `apple`. If you want to use a different ID, you'll have to change the redirect URL in your Apple developer account to conform
1. Enter a Display Name (eg. Apple Sign In)
1. For type choose `oauth`
1. For strategy enter `@nicokaiser/passport-apple`
1. For mapping enter `apple` (it references file `apple.js` previously added)
1. Supply a logo location if desired. More info [here](../authn-guide/passport/#about-logo-images). If you Gluu server version is 4.1 or higher, you can simply use `img/apple.png`.
1. Enter the **service ID* in `client ID` field
1. Enter a dummy value for `Client Secret`. Atypically, Apple Sign In does not require a secret, however, do not remove this property. 
1. Add a new property `keyID` and fill its value with the **key id** you collected [earlier](#creating-an-apple-application)
1. Add a new property `teamID` and fill its value with the **team ID**
1. Add a new property `key` supplying the path to the key file, eg. `/etc/certs/AuthKey_blah_blah.p8`
1. Add a new property `scope` with value `["name", "email"]`
1. Click on `Add`

## Test

Almost done...

Set passport's logging level to debug. You can revert to info or other when you are done with your tests. In oxTrust go to `Passport` > `Basic configuration` and change `Log level`.

You can use any OIDC app protected by Gluu in order to test. To do so, ensure to pass `passport_social` for `acr_values` in your authentication request. You can already leverage oxTrust to do this: go to `Configuration` > `Manage authentication` and set `oxTrust acr` to `passport_social`. Then logout.

Attempt to login to the application. You will see "Apple Sign In" listed on the right hand panel. Click on it to trigger the flow. You will be taken to the Apple web site to enter your credentials and then returned to the application with access to it.

Something went wrong?

- Double check all configurations were applied accurately
- Check `passport.log` (find it at `/opt/gluu/node/passport/logs`)
- Open a support ticket
