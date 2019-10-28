# Passport attributes mapping

## Overview

A mapping is a mechanism that defines how profile data released by an external provider (eg. a SAML IDP) is saved to local Gluu LDAP.

In Passport 3.1.x, attribute mappings worked in a declarative manner, where administrators potentially had to supply information at different places: custom scripts (via config properties), JSON files, and sometimes in Javascript (Node.js) code. Starting with version 4.0, mappings were moved to Javascript files entirely.

Physically, a mapping is stored in a node module file with a single function that receives as input a profile object and returns an object whose properties (ie. dictionary keys) are the names of Gluu LDAP attributes. The value(s) of each key will contain the data that will be persisted to LDAP.

As an example, consider the following node module `myMapping.js`:

```
module.exports = profile => {
	return {
		uid: profile.username,
		mail: profile.emails[0].value,
		displayName: profile.displayName,
	}
}
```

Here, the `profile =>` syntax is equivalent to `function (profile)`, namely a function with a single parameter named `profile`. This function returns an object with properties `uid`, `mail`, and `displayName` taking values from `profile` object. This routine dictates which data will be persisted at destination as we'll shortly see.

A configured identity provider uses exactly one mapping but one mapping can be used by any number of providers. Mappings are stored in directory `/opt/gluu/node/passport/server/mappings` of Gluu chroot. When you specify the mapping for a given provider in oxTrust, you supply the filename (excluding the extension).

## How mappings work

When users authenticate at an external provider, the corresponding [passport strategy](../authn-guide/passport.md#strategies) (node library) creates an object based on the data received. It normally applies some simple logic to extract common attributes such as display name, last name, e-mail, etc. 

The designated mapping function will be called using the object built by the strategy as the argument, then the resulting output will be sent to the corresponding custom script (`passport_social` or `passport_saml`), where the actual insertion or update of the user entry takes place in LDAP. From there, the flow proceeds so the end-user can get access to the final destination (OIDC RP or SP).

Most Passport strategies simplify the profile data and apparently few of the original information will be available for applying the mapping function. If you want access to the full data (released by the external provider), you have to inspect `_json` property of the profile object. For example:

```
module.exports = profile => {
	return {
		...
		local_attribute: profile._json.some_remote_attribute
		...
	}
}
```

## Custom object classes

Since properties of the returned object map directly to LDAP attributes, you **must** also supply object classes in case some attributes do not belong to `gluuPerson`. As an example, if you plan to set `mobile` attribute, you have to set `objectClass` values explicitly:

```
module.exports = profile => {
	return {
		objectClass: ["gluuPerson", "gluuCustomPerson"],
		mobile: ...
		...
	}
}
```

For instance, in order to set `eduPersonPrincipalName` attribute, you must provide `["gluuPerson", "eduPerson"]` for `objectClass`.


!!! Note:
    If all attributes simply belong to `gluuPerson` there is no need to explicitly set `objectClass`.

## About assigning mappings

When integrating a new external provider for inbound identity in oxTrust, an existing mapping has to be associated with that provider. Based on the type of provider, the UI will make a recommendation for this field. Administrators must determine if the suggestion fits their needs or if a separate new mapping has to be created. 

## Creating and debugging a mapping

While configuring an external provider, it is handy to see a mapping in action. Adding print statements in the mapping function is an easy way to inspect data going in and out. Here is an example:

```
module.exports = profile => {
	console.log(JSON.stringify(profile))
	return {
		uid: profile.username,
		mail: profile.emails[0].value,
		displayName: profile.displayName
	}
}
```

The above simply prints the profile object in JSON notation. Note that any number of (valid Javascript) statements can be added before the `return` keyword.

Save the file in `/opt/gluu/node/passport/server/mappings`, restart Passport and trigger the authentication flow in the browser for the attribute mapping to take place. To see the printed output, tail the `/opt/gluu/node/passport/server/logs/start.log` file.

Once debugging is finished, all log statements should be removed or commented out.

!!! Note
    If you are not able to see any printed messages, there might be an issue in a previous step of the flow. Check the [logs](../authn-guide/passport.md#logging) to troubleshoot.


## Applying attributes transformation

One benefit of the attribute mapping approach used in Passport is that custom logic can be introduced. The function to code can be simple as those found in out-of-the-box mappings or arbitrarily complex. Administrators can do any sort of transformations to incoming attributes so that they match their needs in detail.

Common use cases include meeting length or format restrictions for destination attributes in LDAP. As an example suppose the attribute `birthdate` is present in the input profile. If this date is represented as an integer (relative to the "unix epoch"), it is clear a transformation is needed so that it can be stored in `birthdate` LDAP attribute which follows the [generalized time](https://ldapwiki.com/wiki/GeneralizedTime) syntax. Here is how this can be achieved:

```
module.exports = profile => {
	let d = new Date()
	d.setTime(profile.birthdate)

	let	year = d.getUTCFullYear(),
		month = d.getUTCMonth() + 1,
		day = d.getUTCDate()

	month = (month < 10 ? "0" : "") + month
	day = (day < 10 ? "0" : "") + day
	
	return {
		...
		birthdate: year + month + day + "00Z"
		...
	}
}
```

Note that being a node module, any third-party library can be imported to aid the processing. The library must be installed in `/opt/gluu/jetty/node/passport` as a prerequisite.
