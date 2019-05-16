# Logs
When it comes to troubleshooting issues in the Gluu Server--from service hiccups to outages--your [server logs](../reference/logs.md) are the best place to gather relevant information.

## Connectivity Issues?
### DNS names not resolving!
It is possible that even after configuring everything there is a `DNS` resolve error in Gluu Server.
The reason is the `DNS` used inside the chroot container; the `dns` used by the container is the Google DNS servers 
and the `DNS` for the host OS is not used. Therefore to fix this issue:

- Change the DNS inside the container by editing the `/etc/resolv.conf` file and adding the DNS used by your organization
## Locked Out?
### Forgot the admin password! 

Oh no, its been a few days since you booted your test Gluu Server, and
you can't remember the admin password. No worries, the Gluu Server
stores this information in the file
`/install/community-edition-setup/setup.properties.last` under the
property `ldapPass`. Retrieve the data using this command:

```
# grep ldapPass= /install/community-edition-setup/*.last
```

Of course for a production installation, you should remove this file.
You wouldn't want to have your admin password sitting on the filesystem!

## Add admin for Gluu server

Please follow these steps to restore your Gluu admin account (you will
probably need to substitute actual port, bind names and hostnames with
ones used by your installation):

1) Login into Gluu's chroot environment with the command below:

```
# service gluu-server login
```

2) Run this command:

```
#/opt/opendj/bin/ldapsearch -p 1636 -Z -X -D 'cn=directory manager' -w 'YOUR_BIND_PASSWORD' -b o=gluu gluuGroupType=gluuManagerGroup 1.1
```

and remember the displayed dn of the Gluu Manager Group for future use.

3) Run this command:

```
# /opt/opendj/bin/ldapsearch -p 1636 -Z -X -D 'cn=directory manager' -w 'YOUR_BIND_PASSWORD' -b o=gluu ou=people 1.1
```

and remember the displayed dn of the People ou for future use.

4) While staying in the chrooted environment, create the file
`~/add_user.ldif` using your favorite text editor, and copy the
following lines to it:

```
dn: inum=tempadmin,ou=people,o=@!F9CC.D762.4778.1032!0001!2C72.BB87,o=gluu
changetype: add
uid: tempadmin
objectClass: gluuPerson
objectClass: top
givenName: tempadmin
sn: tempadmin
inum: tempadmin
gluuStatus: active
userPassword: 1q2w3e
```

Please note the string's segment marked with bold: you will have to
substitute it with dn of your own People ou which you've acquired in
step 3).

5) Run this command:

```
# /opt/opendj/bin/ldapmodify -p 1636 -Z -X -D 'cn=directory manager' -w 'YOUR_BIND_PASSWORD' -f ~/add_user.ldif
```

This will create new user tempadmin with attributes provided via file
created in step 4).

6) Now create file `add_2_group.ldif` in your home ("~/") directory and
copy the following lines to it:

```
dn: inum=@!F9CC.D762.4778.1032!0001!2C72.BB87!0003!60B7,ou=groups,o=@!f9cc.d762.4778.1032!0001!2c72.bb87,o=gluu
changetype: modify
add: member
member: inum=tempadmin,ou=people,o=@!f9cc.d762.4778.1032!0001!2c72.bb87,o=gluu
```

Again, please note the strings' segment marked with bold: you will have
to substitute contents of the "dn:" string with dn of your own Gluu
Manager Group which you've acquired in step 2), and for "member:" string
you will have to use the dn of tempadmin user (the one you already
specified in the 1st line of the file in step 4).

7) Run this command:

```
# /opt/opendj/bin/ldapmodify -p 1636 -Z -X -D 'cn=directory manager' -w 'YOUR_BIND_PASSWORD' -f ~/add_2_group.ldif
```

This will add tempadmin user to the IdP managers group and you can then
login and assign another user to act as admin.

## Revert Authentication Method
It is not unlikely that you will lock yourself out of Gluu Server while testing the authentication script, if there is any problem in it. In such a case the following method can be used to revert back the older authentication method.

1. Run the following command to collect the `inum` for the Gluu Server installation.

`/opt/opendj/bin/ldapsearch -h localhost -p 1389 -D "cn=directory 
manager" -j ~/.pw -b "ou=appliances,o=gluu" -s one "objectclass=*" 
oxAuthenticationMode`

2. Create a `LDIF` file with the contents below:

```
dn: inum=@!1E3B.F133.14FA.5062!0002!4B66.CF9C,ou=appliances,o=gluu
changetype: modify
replace: oxAuthenticationMode
oxAuthenticationMode: internal
```

As an example, we shall call this file `changeAuth.ldif`.

**Note:** Replace the `inum` from the example above with the `inum` of the Gluu Server from the `ldapsearch` command.


3. Replace the the authentication mode using `ldapmodify` command.

`/opt/opendj/bin/ldapmodify -p 1636 -Z -X -D 'cn=directory manager' -w 'YOUR_BIND_PASSWORD' -f ~/changeAuth.ldif

## No admin access after Cache Refresh?
Add the password for your admin account to `~/.pw` and then use the commands below to add yourself as an admin.

```bash
# set this to your actual user name
export newgluuadmin='myusername'

# this is the file that will hold the info to be imported
export ldiffile='addManagers.ldif'

# run this and verify that the output is for your account
/opt/opendj/bin/ldapsearch -h localhost -p 1636 -D "cn=directory manager" -j ~/.pw -Z -X -b "o=gluu" "uid=$newgluuadmin" uid givenName sn cn

dn: inum=@!134D.3C3D.796E.FECE!0001!E022.CC3C!0000!A8F2.DE1E.D7FB,ou=people,o=@!134D.
 3C3D.796E.FECE!0001!E022.CC3C,o=gluu
uid: myusername
givenName: John
sn: Doe
cn: John Doe
```

Now you can run these commands to make the file above:

```bash
head -n1 /opt/opendj/ldif/groups.ldif > $ldiffile
echo 'changetype: modify' >> $ldiffile
echo 'add: member' >> $ldiffile
echo "member: $(/opt/opendj/bin/ldapsearch -h localhost -p 1636 -D "cn=directory manager" -j ~/.pw -Z -X -b "o=gluu" "uid=$newgluuadmin" uid givenName sn cn |grep -A1 dn |cut -d ' ' -f 2- | sed 'N;s/\n//')" >> $ldiffile
```

The resulting ldif will look like this:

```bash
dn: inum=@!134D.3C3D.796E.FECE!0001!E022.CC3C!0003!60B7,ou=groups,o=@!134D.3C3D.796E.FECE!0001!E022.CC3C,o=gluu
changetype: modify
add: member
member: inum=@!134D.3C3D.796E.FECE!0001!E022.CC3C!0000!A8F2.DE1E.D7FB,ou=people,o=@!134D.3C3D.796E.FECE!0001!E022.CC3C,o=gluu
```

Once the ldif looks right, run this to grant your account admin rights in Gluu:

```bash
/opt/opendj/bin/ldapmodify -h localhost -p 1636 -D "cn=directory manager" -j ~/.pw -Z -X -f addManagers.ldif
```

Log into the web interface and pick up where you left off :)

## Lock users?
### Lock Account using Custom Scripts
This section will help in locking a user account using custom scripts in solutions where it is
mandatory to limit access trials to a specific number i.e. lock user account if the user fails to
produce correct password 3 times.

Gluu Server makes it easy by using a single attribute to enable/disable user. The `gluuStatus` attribute
is used to enable/disable the user. This attribute holds the value `acive/inactive` and setting `gluuStatus=inactive`
any user can be locked from Gluu Server.

The following snippet will help you find the user by UID and set the `gluuStatus` attribute to inactive.

```
from org.xdi.oxauth.service import UserService
...
# Find user entry by UID
user_uid = credentials.getUser().getUserId()
find_user_by_uid = userService.getUser(user_uid)

# Update user entry and persist it
find_user_by_uid.setAttribute("gluuStatus", "inactive")
userService.updateUser(find_user_by_uid)
```

The users can be activated again by clicking on the update button in oxTrust.