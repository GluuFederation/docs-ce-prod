# IIS SAML Configuration

## IIS Configuration in Windows 7

1. Start --> Control Panel --> Programs --> "Turn Windows features on or off"

2. Select (i) IIS (ii) Web Management Tools (iii) II6 Management Compatibility (iv) IIS Management Console (v) IIS Management Scripts and Tools (vi) IIS Management Service

3. Select (i) World Wide Web Services (ii) CGI (iii) ISAPI Filters (iv) ISAPI Extensions --> Press OK.
![IIS 7 Setup](../img/sp_setup/admin_sp_iis7setup.png)

4. Test IIS to see if it is installed in your system with "127.0.0.1" in the web browser. For our test case, we used IIS7.
![Test IIS](../img/sp_setup/admin_sp_iis7test.png)

## ISAPI Filter Configuration

1. Open IIS Manager (Start --> Administrative Tools --> Internet Information Service/IIS Manager)

2. Double click on "ISAPI and CGI Restrictions"
![ISAPI and CGI](../img/sp_setup/admin_sp_isapicgi.png)

3. Add a new Filter

  a. Click Actions --> Add (upper right corner)

  b. Select "\opt\shibboleth-sp\lib\shibboleth\isapi_shib.dll"

  c. Description: "Shibboleth"

  d. Click "Allow" (from the right hand side)

![ISAPI Path](../img/sp_setup/apache_sp_isapipath.png)

  e. Back to IIS Manager --> ISAPI Filters

![ISAPI Filters](../img/sp_setup/apache_sp_isapifilter.png)

        1. Click "Add" (upper right corner)

        2. Filter Name: Shibboleth

        3. Executable: "\opt\shibboleth-sp\lib\shibboleth\isapi_shib.dll"

![ISAPI Edit](../img/sp_setup/apache_sp_isapiedit.png)

  f. SSO file extension mapping

        1. Click on "Handler Mapping" from main page

![SP Handler](../img/sp_setup/admin_sp_handlermapping.png)

        2. Click "Add Script Map" from Action
![Script Map](../img/sp_setup/admin_sp_addscriptmap.png)

        3. Request Path :".sso"

        4. Executable should be pointed to "isapi_shib.dll"
![Executable](../img/sp_setup/admin_sp_executable.png)

  g. Restart IIS

  h. Check Status

  Check Status by typing in "http://127.0.0.1/Shibboleth.sso/Status" in the web browser. If it displays an XML document, then the Shibboleth SP Installation in Windows IIS7 in complete.
![Status Check](../img/sp_setup/admin_sp_checkstatus.png)

## Shibboleth SP Setup in Windows 2008 R2 with IIS7

1. Open up "Server Manager", scroll down and click on "Add Roles".

![Add Role](../img/sp_setup/iis_setup_addrole.png)

2. Hit "Next"

![Next](../img/sp_setup/iis_setup_next.png)

3. Select "Web Server (IIS)", hit "Next"

![Web Server](../img/sp_setup/iis_setup_webserver.png)

4. Select (i) CGI

(ii) ISAPI Extensions

(iii) ISAPI Filters

(iv) Management Tools

  (a) IIS Management Console

  (b) IIS Management Scripts and Tools

  (c) Management Service

(v) All IIS6 Management Compatibility

![Selection](../img/sp_setup/iis_setup_selection.png)

![Selection](../img/sp_setup/iis_setup_selection1.png)

5. Hit "Next", for the confirmation, check the list of plugins.

![Plugin](../img/sp_setup/iis_setup_plugin.png)

![Management Tools](../img/sp_setup/iis_setup_managementtools.png)

6. Hit "Install" and Windows 2008 will complete the installation. A confirmation window shall appear which resembles the screenshot below.

![Confirmation](../img/sp_setup/iis_setup_confirmation.png)

7.Test IIS7 setup from the Internet.

![Test](../img/sp_setup/iis_setup_test.png)

### Shibboleth SP 2.5.x Setup

1. Down the [Shibboleth SP 2.5.x](http://www.shibboleth.net/downloads/service-provider/latest/)

2. Start the installation, keep the default path, Select "Install ISAPI modules into IIS", IIS Script Extension must be ".sso" and Hit "Next".

![Shib Setup](../img/sp_setup/iis_setup_shibsetup.png)

3. After the completion of the installation, the system will ask to reboot the system; hit "Yes".

![Restart](../img/sp_setup/iis_setup_restart.png)

4. Test the Shibboleth SP installation from the SP VM using the URL "localhost/Shibboleth.sso/Status" in the address bar of the Web Browser.

![Status](../img/sp_setup/iis_setup_status.png)

### Trust Relationship in IdP

1. Create a Trust Relationship for the new SP in the IdP. It is necessary to upload the Public Certificate of the new SP in the IdP. Please note that the CN of the public certificate MUST BE the same as _Hostname_ of the SP. Hit "Add".

![Add TR](../img/sp_setup/iis_setup_addtr.png)

2. Download the IdP generated configuration files for Shib SP modification.

![Download](../img/sp_setup/iis_setup_download.png)

### SP Configuration

1. The files from the IdP must be placed in the SP Configuration.

2. Before placing them inside the SP Configuration please check

  (a) The "spcert.crt" file has the CN same as the SP hostname.

  (b) The "spcert.crt" and "spkey.key" has the same _md5sum_ value.

  (c) The IdP-metadata is perfectly placed inside the SP Configuration.

  (d) The downloaded "shibboleth2.xml" file has values resembling the file content below.

3. For testing purpose, we are going to protect a directory named "secure" with the IdP.  Create a folder/directory in the IIS Root Directory and restart Shibd and IIS.

![Secure](../img/sp_setup/iis_setup_secure.png)

### SSO Testing

1. Place the following URL in the web browser: "https://SP_Name/secure"

2. It will redirect the user to the IdP for authentication.

3. After the authentication is complete, the user will be shown the protected page. For this case, the page is the IIS7 index page.


	<SPConfig xmlns="urn:mace:shibboleth:2.0:native:sp:config"
    	  xmlns:conf="urn:mace:shibboleth:2.0:native:sp:config"
    	  xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    	  xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"    
    	  xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    	  logger="syslog.logger" clockSkew="180">

	  <!-- The OutOfProcess section contains properties affecting the shibd daemon. -->
    	  <OutOfProcess logger="shibd.logger">
    	  </OutOfProcess>

	  <!-- The InProcess section conrains settings affecting web server modules/filters. -->
    	  <InProcess logger="native.logger">
        	<ISAPI normalizeRequest="true" safeHeaderNames="true">
            	  <Site id="1" name="SP_HOSTNAME_WITHOUT_HTTP_OR_HTTPS"/>
        	</ISAPI>
    	  </InProcess>

	  <!-- Only one listener can be defined, to connect in-process modules to shibd. -->
    	  <TCPListener address="127.0.0.1" port="1600" acl="127.0.0.1"/>
    	  <!-- <UnixListener address="shibd.sock"/> -->

	  <!-- This set of components stores sessions and other persistent data in daemon memory. -->
    	  <StorageService type="Memory" id="mem" cleanupInterval="900"/>
    	  <SessionCache type="StorageService" StorageService="mem" cacheTimeout="3600" inprocTimeout="900" cleanupInterval="900"/>
    	  <ReplayCache StorageService="mem"/>
    	  <ArtifactMap artifactTTL="180"/>

	  <!-- To customize behavior, map hostnames and path components to applicationId and other settings. -->
    	  <RequestMapper type="Native">
        	<RequestMap applicationId="default">
            	    <Host name="SP_HOSTNAME_WITHOUT_HTTP_OR_HTTPS">
                	<Path name="secure" authType="shibboleth" requireSession="true"/>
            	    </Host>
          	</RequestMap>
    	  </RequestMapper>

	  <!--
    	  The ApplicationDefaults element is where most of Shibboleths SAML bits are defined.
    	  Resource requests are mapped by the RequestMapper to an applicationId that
    	  points into to this section.
    	  -->
	  <ApplicationDefaults id="default" policyId="default"
          	entityID="DAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx867"
          	REMOTE_USER="eppn persistent-id targeted-id uid mail"
          	signing="false" encryption="false" attributePrefix="AJP_">

		<!--
        	Controls session lifetimes, address checks, cookie handling, and the protocol handlers.
        	You MUST supply an effectively unique handlerURL value for each of your applications.
        	The value can be a relative path, a URL with no hostname (https:///path) or a full URL.
        	The system can compute a relative value based on the virtual host. Using handlerSSL="true"
        	will force the protocol to be https. You should also add a cookieProps setting of "; path=/; secure"
        	in that case. Note that while we default checkAddress to "false", this has a negative
        	impact on the security of the SP. Stealing cookies/sessions is much easier with this disabled.
        	-->
		<Sessions lifetime="28800" timeout="3600" checkAddress="false"
            	    handlerURL="https://SP_HOSTNAME/Shibboleth.sso" handlerSSL="false"
            	    exportLocation="http://localhost/Shibboleth.sso/GetAssertion" exportACL="127.0.0.1"
            	    idpHistory="false" idpHistoryDays="7" cookieProps="; path=/; secure; httpOnly">

		    <!--
            	    SessionInitiators handle session requests and relay them to a Discovery page,
            	    or to an IdP if possible. Automatic session setup will use the default or first
            	    element (or requireSessionWith can specify a specific id to use).
            	    -->

		    <!-- Default example directs to a specific IdPs SSO service (favoring SAML 2 over Shib 1). -->
            	    <SessionInitiator type="Chaining" Location="/Login" isDefault="true" id="gluu"
                    	    relayState="cookie" entityID="https://IDP_HOSTNAME/idp/shibboleth">
                       <SessionInitiator type="SAML2" acsIndex="1" template="bindingTemplate.html"/>
                       <SessionInitiator type="Shib1" acsIndex="5"/>
            	    </SessionInitiator>

		    <!--
            	    md:AssertionConsumerService locations handle specific SSO protocol bindings,
            	    such as SAML 2.0 POST or SAML 1.1 Artifact. The isDefault and index attributes
            	    are used when sessions are initiated to determine how to tell the IdP where and
            	    how to return the response.
            	    -->
		    <md:AssertionConsumerService Location="/SAML2/POST" index="1"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
            	    <md:AssertionConsumerService Location="/SAML2/POST-SimpleSign" index="2"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST-SimpleSign"/>
            	    <md:AssertionConsumerService Location="/SAML2/Artifact" index="3"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact"/>
            	    <md:AssertionConsumerService Location="/SAML2/ECP" index="4"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:PAOS"/>
            	    <md:AssertionConsumerService Location="/SAML/POST" index="5"
                	Binding="urn:oasis:names:tc:SAML:1.0:profiles:browser-post"/>
            	    <md:AssertionConsumerService Location="/SAML/Artifact" index="6"
                	Binding="urn:oasis:names:tc:SAML:1.0:profiles:artifact-01"/>

		    <!-- LogoutInitiators enable SP-initiated local or global/single logout of sessions. -->
            	    <LogoutInitiator type="Chaining" Location="/Logout" relayState="cookie">
                	<LogoutInitiator type="SAML2" template="bindingTemplate.html"/>
                	<LogoutInitiator type="Local"/>
            	    </LogoutInitiator>

		    <!-- md:SingleLogoutService locations handle single logout (SLO) protocol messages. -->
            	    <md:SingleLogoutService Location="/SLO/SOAP"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:SOAP"/>
            	    <md:SingleLogoutService Location="/SLO/Redirect" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"/>
            	    <md:SingleLogoutService Location="/SLO/POST" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
            	    <md:SingleLogoutService Location="/SLO/Artifact" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact"/>

		    <!-- md:ManageNameIDService locations handle NameID management (NIM) protocol messages. -->
            	    <md:ManageNameIDService Location="/NIM/SOAP"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:SOAP"/>
            	    <md:ManageNameIDService Location="/NIM/Redirect" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"/>
            	    <md:ManageNameIDService Location="/NIM/POST" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
            	    <md:ManageNameIDService Location="/NIM/Artifact" conf:template="bindingTemplate.html"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact"/>

		    <!--
            	    md:ArtifactResolutionService locations resolve artifacts issued when using the
            	    SAML 2.0 HTTP-Artifact binding on outgoing messages, generally uses SOAP.
            	    -->
            	    <md:ArtifactResolutionService Location="/Artifact/SOAP" index="1"
                	Binding="urn:oasis:names:tc:SAML:2.0:bindings:SOAP"/>

		    <!-- Extension service that generates "approximate" metadata based on SP configuration. -->
            	    <Handler type="MetadataGenerator" Location="/Metadata" signing="false"/>

            	    <!-- Status reporting service. -->
            	    <Handler type="Status" Location="/Status" acl="127.0.0.1"/>

            	    <!-- Session diagnostic service. -->
            	    <Handler type="Session" Location="/Session" showAttributeValues="false"/>

		</Sessions>

		<!--
        	Allows overriding of error template filenames. You can also add attributes with values
        	that can be plugged into the templates.
        	-->
        	<Errors supportContact="support@gluu.org"
            	    logoLocation="/shibboleth-sp/logo.jpg"
            	    styleSheet="/shibboleth-sp/main.css"/>

		<!-- Uncomment and modify to tweak settings for specific IdPs or groups. -->
        	<RelyingParty Name="IDP_HOSTNAME_WITHOUT_HTTP_OR_HTTPS" keyName="IDP_HOSTNAME_WITHOUT_HTTP_OR_HTTPS"/>

		<!-- Chains together all your metadata sources. -->
        	<MetadataProvider type="Chaining">
			<MetadataProvider type="XML" file="C:\opt\shibboleth-sp\etc\shibboleth\idp-metadata.xml"/>
        	</MetadataProvider>

		<!-- Chain the two built-in trust engines together. -->
        	<TrustEngine type="Chaining">
            		<TrustEngine type="ExplicitKey"/>
            		<TrustEngine type="PKIX"/>
        	</TrustEngine>

		<!-- Map to extract attributes from SAML assertions. -->
        	<AttributeExtractor type="XML" validate="true" path="attribute-map.xml"/>
        
        	<!-- Use a SAML query if no attributes are supplied during SSO. -->
        	<AttributeResolver type="Query" subjectMatch="true"/>

        	<!-- Default filtering policy for recognized attributes, lets other data pass. -->
        	<AttributeFilter type="XML" validate="true" path="attribute-policy.xml"/>

		<!-- Simple file-based resolver for using a single keypair. -->
			<!-- <CredentialResolver type="File" key="sp-key.pem" certificate="sp-cert.pem"/> -->

			<!-- TODO is password needed? -->
			<CredentialResolver type="File" key="C:\opt\shibboleth-sp\etc\shibboleth\spkey.key"
							certificate="C:\opt\shibboleth-sp\etc\shibboleth\spcert.crt" />

	    </ApplicationDefaults>

	    <!-- Each policy defines a set of rules to use to secure messages. -->
    	    <SecurityPolicies>
        	<!--
        	The predefined policy enforces replay/freshness, standard
        	condition processing, and permits signing and client TLS.
        	-->
		<Policy id="default" validate="false">
            		<PolicyRule type="MessageFlow" checkReplay="true" expires="60"/>
            		<PolicyRule type="Conditions">
                		<PolicyRule type="Audience"/>
                		<!-- Enable Delegation rule to permit delegated access. -->
                		<!-- <PolicyRule type="Delegation"/> -->
            		</PolicyRule>
            		<PolicyRule type="ClientCertAuth" errorFatal="true"/>
            		<PolicyRule type="XMLSigning" errorFatal="true"/>
            		<PolicyRule type="SimpleSigning" errorFatal="true"/>
        	</Policy>
    	    </SecurityPolicies>

	</SPConfig>
