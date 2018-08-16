# Gluu Server Patches

## Code White Patch
### August 16, 2018

came to know of a critical vulnerability in Jboss Richfaces library. All versions of the component Richfaces (including the latest v4.5.17.Final) are affected by the vulnerability, which is an EL injection leading to Remote Code Execution. The CVE assignment to MITRE for it is CVE-2018-12532. The CVE can be seen on the [MITRE](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12532) site as well as [NIST](https://nvd.nist.gov/vuln/detail/CVE-2018-12532). 

This vulnerability is basically a bypass of CVE-2015-0279. CVE-2015-0279 hardens the org.richfaces.resource.MediaOutputResource class by blocking expressions containing parantheses (https://github.com/richfaces/richfaces/blob/4.5.17.Final/components/a4j/src/main/java/org/richfaces/resource/MediaOutputResource.java#L67-L69). The new vulnerability lies in the fact that EL additionally made use of custom variable mappers internally to resolve the variable name in case it's not found in the main expression, but variable mappers themselves can contain EL code just the same. Variable mappers are implemented through the varMapper field of org.apache.el.MethodExpressionImpl in Tomcat EL api (which Jetty is also using).

The general flow looks like this, the application derializes the "do" parameter (the 'source') at org.richfaces.resource.ResourceUtils#decodeBytesData, passes the object through some other calls and eventually calls a MethodExpression.invoke on a field in the object (the 'sink') at org.richfaces.resource.MediaOutputResource#encode. There is however a protection in place restricting deserialization to certain classes (https://github.com/richfaces/richfaces/blob/4.5.17.Final/core/src/main/java/org/richfaces/util/LookAheadObjectInputStream.java#L133), but as the VariableMapperImpl class is also whitelisted there, we then have full control over the varMapper field in the MethodExpressionImpl instance, which essentially means arbitrary EL injection.

As oxTrust/Identity utilizes Jboss Richfaces, this allows an unauthorized user to perform unauthorized Remote Code Execution. Knowing this, we've created a richfaces updater script that removes the affected class from the `identity.war` file, negating the impact of this vulnerability. That being said, oxTrust should never be internet facing
