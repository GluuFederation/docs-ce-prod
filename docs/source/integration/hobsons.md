# SAML Trust Relationship with Hobsons Education Solutions Co

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

This guide has been prepared to connect the Hobsons Service Provider
(SP) with the Gluu Server for SP-initiated SSO. The connection is
established through the creation of a Trust Relationship using the Gluu
Server UI, oxTrust.

## Creating Hobsons Trust Relationship

* Log in to your Gluu Server using your admin credentials.

* Next, click on the SAML tab, and select the option Trust
Relationships. Then, click on the `Add Relationship` button.

![Add Relationship](../img/integration/admin_saml_create.png)

* The button `Add Relationship` will open the following page, the trust
relationship can be created easily using the following form.

![Add empty form](../img/integration/admin_saml_newTR.png)

	1. __Display Name__: This field contains the display name of the 
    Trust Relationship. In the example below we use “Test Hobsons-Radius TR”.

	2. __Description__: A small description of Hobsons can be input here.

	3. __Metadata Type__: Please select the uri from the dropdown menu.

	4. __SP Metadata URL__: The metadata uri provided by Hobsons goes here.

	5. __SP Logout URL__: This uri is meant to be supplied by the
    Hobsons staff. If you did not receiv any logout uri yet, leave it blank.

	6. __Released__: The two necessary attributes--`Transientid` and the
    `eduPersonPrincipalName`--were selected from the attribute list.

![hobsons-tr](../img/integration/hobsons-tr.jpg)

	7. Finally, click "Add" to finish creating the Trust Relationship.

## Configuring Hobsons Trust Relationship

Please ensure that the new Trust Relationship status is "active".
Otherwise click on the Trust Relationship, and activate it before
configuring it.

![hobsons-tr-active](../img/integration/hobsons-tr-active.jpg)

The configuration screen opens by clicking on the Hobsons Trust Relationship.

1. __Configure Metadata Filters__: Do not make any changes.

2. __Configure specific Relying Party__: Check this option and a link "Configure Relying Party" will appear.

3. __Configure Relying Party__: Click on the link, and a new window opens:

	* Select SAML2SSO from the list and click on the "Add" button.

	* Set "signResponses", "signAssertions", "signRequests" and
    "encryptAssertions" to `Conditional` from the drop-down menu.

	* Set "encryptNameIds" to `Never` from the drop-down menu, and click
    "Save".

![hobsons-tr-update](../img/integration/hobsons-tr-update.jpg)

4. Click "Update" to finish the configuration of the Trust Relationship.


