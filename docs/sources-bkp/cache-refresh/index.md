# Overview
Cache Refresh is the process of connecting an existing backend LDAP server, like Microsoft Active Directory, with the Gluu Server's local LDAP server. Synching people and attributes from a backend server into the Gluu Server speeds up authentication transactions. It is possible to perform attribute transformations, changing the name of attributes, or even using an interception script to change the values. Transformations are stored in the Gluu LDAP service. 

## Video Tutorial
For a guided video overview of configuring Cache Refresh, please watch the following three videos:    
- [Part 1: What is 'Cache Refresh' and How Does it Work?](https://youtu.be/VnyCTUCRkic)     
- [Part 2: Configuring Cache Refresh in the Gluu Server](https://youtu.be/c64l_xmBbvw)    
- [Part 3: Managing Authentication After You've Setup Cache Refresh](https://youtu.be/fyAEwJuwqn4)    
       
## Things To Remember
The Gluu Server supports two LDAP modes: (1) authentication and (2)
identity mapping. Only sometimes it is the same LDAP server. To
synchronize user accounts from an external LDAP directory server, you
can use the built-in oxTrust features for ”Cache Refresh”, which support
mapping identities from n number of source directory servers.

After configuring Cache Refresh, you should give it some time to run,
and populate the LDAP server. Here are some tips before you get started:

* Enable 'Keep External Person' during CR setup. This will allow your
  default user 'admin' to log into Gluu Server after initial Cache 
  Refresh iteration. If you do not enable 'Keep External Person', your 
  'admin' user including all other test users will be gone after first 
  Cache Refresh iteration.

* Make sure you are using LDAP authentication, not VDS. You will only
  need VDS setting if you are using the Radiant Logic Virtual Directory
  Server.

* Check the snapshots folder to see if files are being created.

* Use the oxTrust admin to browse users.

* Use the command `ldapsearch` to check to see if results are starting
  to come in. The following command will search for the total number of
  users in the Gluu LDAP:

```
# /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w 'pass_of_ldap_ -b 'ou=people,o=DA....,o=gluu' dn | grep "dn\:" | wc -l
```

* Try to login with one of these users. We assume that you have also
  setup your Gluu Server to use the correct LDAP server for
  authentication.

## Things To Know
The deployer needs to know various values of his own backend AD to
configure this part. For example, host & port, bindDN user information,
bindDN password, Objectclasses, attributes whose information will be
pulled etc.

In addition, the deployer also needs to know generic information of his
Gluu Server's LDAP. By default, the deployer can use 'localhost:1636',
'cn=directory manager', 'password what he chose during installation',
'ou=people,o=site' as server information, bindDN, bindDN password and
baseDN respectively.

After collecting this information, the deployer can move forward with
the setup of the Cache Refresh engine.

## Configuring Cache Refresh From oxTrust
For a successful Cache Refresh setup, please complete the data fields in
both the 'Cache Refresh', 'Customer Backend Key/Attributes', and 'Source
Backend LDAP Servers' sections. It is not necessary enter data in the
'Inum LDAP Server' tab.

![Cache Refresh Menu](../img/oxTrust/admin_cache_menu.png)

* _Refresh Method:_ The Gluu Server allows the server administrator to
  apply two types of Cache Refresh mechanisms--(1) VDS Method, and (2) 
  Copy Method.

  1. _VDS Method:_ Use this if the backend is a database such as *mysql*.
![Refresh VDS](../img/oxTrust/admin_cache_refresh_vds.png)

  2. _Copy Method:_ It is strongly recommended to use this method if the backend data source is any kind of Active Directory or LDAP Server.
![Refresh Copy](../img/oxTrust/admin_cache_refresh_copy.png)

* _Source attribute to destination attribute mapping:_ The left entry field defines 
  the attributes from the backend data source. The right entry field 
  defines where it should be rendered/placed as it is delivered to the Gluu Server.
![cache-refresh8](../img/oxTrustConfiguration/CR/Cache_Refresh_8.png)

  * _Pooling Interval (Minutes):_ It is recommended to be
  kept higher than 15 minutes.

  * _Server IP Address:_ Enter the IP address of the Gluu Server in this field. The IP with which the Gluu Server was setup, should be used here.

  * _Snapshot Folder:_ Every cycle of the Gluu Server Cache Refresh cycle
  saves both an overall snapshot and a problem-list record on a specified
  location. This is where the Gluu Server administrator can specify the
  location.

  * _Snapshot Count:_ It is recommended
  to be keep the value to 20 snapshots.

  * _Keep external persons:_ Check this box to retain the `admin` user.

### Customer Backend Key and Attributes
![Customer Backend Key](../img/oxTrust/admin_cache_backend.png)

* _Key Attribute:_ This is the unique key attribute of backend Active
  Directory/LDAP Server such as `SAMAccountname` for any Active Directory.

* _Object Class:_ This contains the object classes of the backend Active
  Directory/LDAP which have permission to talk to the Gluu Server Cache
  Refresh such as person, organizationalPerson, user etc.

* _Source Attribute:_ This contains the list of attributes which will be
  pulled and read by the Gluu Server.

* _Custom LDAP Filter:_ If there is any custom search required, this
  filtering mechanism can be used such as `sn=*`. The value of this field
  ensures that every user must contain an attribute named SN.

### Source Backend LDAP Servers

![Source Backend](../img/oxTrust/admin_cache_sourcebackend.png)

This section allows the Gluu Server to connect to the backend Active
Directory/LDAP server of your organization.

* _Name:_ Please input **source** as the value.

* _Use Anonymous Bind:_ Some customers do now allow username/password
  connections to their backend server. Enable this option if this applies
  to your organization.

* _Bind DN:_ This contains the username of the backend
  server. You need to use full DN here. As for example,
  `cn=gluu,dc=company,dc=org`.

* _Use SSL:_ Use this feature if the backend server allows SSL connectivity.

* _Max Connections:_ This value defines the maximum number of
  connections that are allowed to read the backend Active Directory/LDAP
  server. It is recommended to keep the value 2 or 3.

* _Server:_ This contains the backend Active Directory/LDAP server
  hostname with port, i.e. `backend.organization.com:389`. If your
  organization has a failover server, click **Add Server** to add more
  hostnames with the according port.

* _Base DN:_ This contains the location of the Active Directory/LDAP
  tree of the backend data source.

* _Enabled:_ This check-box is to save and push the changes.

* _Change Bind Password:_ This can be used for a new password or to
  change any existing password.

If any organization has multiple Active Directory/LDAP server, click on
**Add source LDAP server** and add the additional server information.
Please remember that a *failover server* is not a new server.

## Cache Refresh Whitepages
The following file is prepared by a Gluu Engineer to make Cache refresh mechanism 
easy to understand. Please download and read it if this page is not clear.

* [Cache Refresh Whitepages](./GluuCache-Refresh.pdf)
[ldap]: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol "Lightweight Directory Access Protocol (LDAP), Wikipedia"
