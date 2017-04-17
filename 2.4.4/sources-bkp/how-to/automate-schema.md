# Automating Schema for Custom Attribute
This how-to is created to guide through the process of automating a schema for a custom attribute.
The creation of a custom schema will automaticaly create the custom attribute and it can be populated 
from the backend easily through Cache Refresh mechanism without creating the custom attribute again in a 
new installation.

## Generating Schema
The schema for the custom attribute should be created as a `.ldif` file and added to the `/opt/opendj/config/schema/` folder.
The new schema shall be named `102-custom.ldif` as an example. 

* It is assumed that the attribute is already created and used by Gluu Server. If you have not created the custom attribute, please do so. The schema for dynamically created attributes are stored in the `100-user.ldif` file under `/opt/opendj/config/schema` folder by default. 

* The attribute metadata is stred inside the opendj LDAP tree under `ou-attributes, o=org-inum, o=gluu`. Please find the ldif entries that corresponds to the custom schema and export them into one file.

* Create a template using `%(x)s` where x is the name of the python key in a dictionary. For example: if there is one attribute, and a schema file is created named `102-custom.ldif` the contents would look like something below:
```
    dn: inum=%(org_inum)s!0005!%(attr1_id)s,ou=attributes,o=%(org_inum)s,o=gluu
    objectClass: gluuAttribute
    objectClass: top
    description: Specifies the person's affiliation
    displayName: eduPersonScopedAffiliation
    gluuAttributeEditType: admin
    gluuAttributeName: eduPersonScopedAffiliation
    gluuAttributeOrigin: eduPerson
    gluuAttributeType: string
    gluuAttributeViewType: admin
    gluuStatus: inactive
    inum: inum=%(org_inum)s!0005!%(attr1_id)s
    urn: oid:1.3.6.1.4.1.5923.1.1.1.9
```

* A python script can be used to update the right organization ID for the `.ldif` file. For example:

```
    #!/usr/bin/python

    import uuid

    f = open("102-custom.ldif.template")
    ldif = f.read()
    f.close()

    def getQuad():
        return str(uuid.uuid4())[:4].upper()

    d = {}
    d["org_inum"] = "@!43A9.4B45.403D.3B0A!0001!0D87.EAF2"
    d["attr1_id"] = "%s.%s" % (getQuad(), getQuad())

    new_ldif = ldif % d
    f = open("102-custom.ldif", "w")
    f.write(new_ldif)
    f.close()
```
**Note:** This guide is a introductory guide only, there might be some tweaks necessary custom solutions.

* Now you should be able to use the `102-custom.ldif` file to auto generate the custom attribute in future installations.
