## LDAP Synchronization 
LDAP Synchronization, a.k.a. Cache Refresh, is the process of connecting one or more existing backend LDAP servers, like Microsoft Active Directory, with the Gluu Server's local LDAP server. Synching people and attributes from a backend server speeds up authentication transactions. It is possible to perform attribute transformations, changing the name of attributes, or even using an interception script to change the values. Transformations are stored in the Gluu LDAP service. 

!!! Note
    If you are synching user information from multiple backend servers (AD or LDAP) simultaneously, the backend tree structure should be identical.

### Video Tutorial
For a guided video overview of configuring Cache Refresh, please watch the following three videos:    
- [Part 1: What is 'Cache Refresh' and How Does it Work?](https://youtu.be/VnyCTUCRkic)     
- [Part 2: Configuring Cache Refresh in the Gluu Server](https://youtu.be/c64l_xmBbvw)    
- [Part 3: Managing Authentication After You've Setup Cache Refresh](https://youtu.be/fyAEwJuwqn4)    
       
### Things To Remember
The Gluu Server supports two LDAP modes: 

- Authentication 
- Identity mapping

Only sometimes it is the same LDAP server. To synchronize user accounts from an external LDAP directory server, you can use the built-in oxTrust features for Cache Refresh, which supports mapping identities from one or more source directory servers.

After configuring Cache Refresh, you should give it some time to run and populate the LDAP server. Here are some tips before you get started:

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
# /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w pass_of_ldap_ -b "ou=people,o=DA....,o=gluu" dn | grep "dn\:" | wc -l
```

* Try to login with one of these users. We assume that you have also
  setup your Gluu Server to use the correct LDAP server for
  authentication.

### Things To Know
The deployer needs to know various values of the backend AD to
configure Cache Refresh. For example, host & port, bindDN user information,
bindDN password, Objectclasses, attributes which will be
pulled etc.

In addition, the deployer needs to know generic information about the
Gluu Server's LDAP. By default, the deployer can use `localhost:1636`,
`cn=directory manager`, `password` chosen during installation,
`ou=people,o=site` as server information, `bindDN`, `bindDN password` and
`baseDN` respectively.

After collecting this information, the deployer can move forward with
the Cache Refresh setup.

![Cache Refresh Menu](../img/admin-guide/user/admin_cache_menu312.png)


* _Last Run:_ The date and time of the latest cache refresh cycle
  completion is shown here.

* _Updates at the Last Run:_ This shows the total number of users who
  have been updated in the last Cache Refresh cycle. For example an user
  who has any of his attribute updated will show up here.

* _Problem at the Last Run:_ This shows the number of users who have
  been rejected by the Gluu Server during the update. If there are any
  rejections, please contact Gluu Support for clarification and help.

![Last Run](../img/admin-guide/user/admin_cache_lastrun1.png)

### Customer Backend Key and Attributes
![Customer Backend Key](../img/admin-guide/user/admin_cache_backend.png)

* _Key Attribute:_ This is the unique key attribute of backend Active
  Directory/LDAP Server such as SAMAccountname for any Active Directory.

* _Object Class:_ This contains the Object Classes of the backend Active
  Directory/LDAP which has permission to talk to Gluu Server Cache Refresh
  such as person, organizationalPerson, user etc.

* _Source Attribute:_ This contains the list of attributes which will be
  pulled and read by the Gluu Server.

* _Custom LDAP Filter:_ If there is any custom search required, this
filtering mechanism can be used such as "sn=*" whereas the value of this
field ensures that every user must contain an attribute named SN.

### Source Backend LDAP Servers
![Source Backend](../img/admin-guide/user/admin_cache_sourcebackend312.png)

This section allows the Gluu Server to connect to the backend Active
Directory/LDAP server of the organization.

* _Name:_ Please input **source** as the value.

<!-- * _Use Anonymous Bind:_ Some customers do now allow username/password
  connections to their backend server. Enable this option if this applies
  to your organization. -->

* _Bind DN:_ This contains the username to connect to the backend
  server. You need to use full DN here. As for example,
  _cn=gluu,dc=company,dc=org_.

* _Max Connections:_ This value defines the maximum number of
  connections that are allowed to read the backend Active Directory/LDAP
  server. It is recommended to keep the value of 2 or 3.

*_Level:_ TBA
* _Server:_ This contains the backend Active Directory/LDAP server
  hostname with port i.e. backend.organization.com:389. If organization
  has a failover server, click **Add Server** and add more hostnames with
  port.

* _Base DN:_ This contains the location of the Active Directory/LDAP
  tree from where the Gluu Server shall read the user information.

* _Enabled:_ This check-box is used to save and push the changes. Do not
  use this unless the server administrator has entered all the required
  values.

* _Change Bind Password:_ This can be used for a new password or to
  change any existing password.

* _Use SSL:_ Use this feature if the backend server allows SSL
  connectivity.
  
If your organization has a multiple Active Directory/LDAP server, click
on **Add source LDAP server** and add the additional server information.
Please remember that a *failover server* is not a new server.

### Inum LDAP Server

![Inum LDAP Server](../img/admin-guide/user/admin_cache_inum312.png)

This section of the application allows the server administrator to
connect to the internal LDAP of the Gluu Server. As Gluu Server
administrator, you do not need to insert anything here in this section
as new Gluu Server versions automatically populates this for you (unless
you try to manually configure it anyway).

* _Refresh Method:_ The Gluu Server allows the Server Administrator to
  apply two types of Cache Refresh mechanism--(i) VDS Method and (ii) Copy
  Method.

  1. _VDS Method:_ Any organization with a database like *mysql* can use
  the VDS method. This option can be enabled via the drop-down menu in
  Refresh Method option.

![Refresh VDS](../img/admin-guide/user/admin_cache_refresh_vds.png)

  2. _Copy Method:_ If the organization has any kind of Active
  Directory/LDAP server, they are strongly recommended to use the *Copy
  Method* from the drop-down menu.

![Refresh Copy](../img/admin-guide/user/admin_cache_refresh_copy.png)

### Attributes Mapping

When the Copy method is selected, a section for Attribute mapping will
be exposed. In this section, the Gluu Server Administrator can map any
attribute from the backend Active Directory/LDAP to the LDAP cache of
the Gluu Server.

![Attribute Mapping](../img/admin-guide/user/admin_cache_mapattribute.png)

In the source attribute to destination attribute mapping field, you can
enter the source attribute value on the left, and the destination
attribute on the right. In other words, you can specify what the
attribute is on the backend in the left field, and what it should be
rendered as when it comes through the Gluu Server in the right field.

The Administrator can select any Cache Refresh Method according to the
backend Active Directory/LDAP server, but there are some essential
values for both types of cache refresh method. The values are given
below.

  * _Pooling Interval (Minutes):_ This is the interval value for running
    the Cache Refresh mechanism in the Gluu Server. It is recommended to 
    be kept higher than 15 minutes.

  * _Script File Name:_ The Gluu Server cache refresh can accept any
    kind of Jython Script which might help to calculate any custom/complex
    attribute i.e. eduPersonScopedAffiliation. For more information please
    contact Gluu Support.

  * _Snapshot Folder:_ Every cycle of Gluu Server Cache Refresh cycle
    saves an overall snapshot and problem-list record on a specified
    location. This is where the Gluu Server Administrator can specify the
    location. You can easily decide whether cache refresh synchronizes all
    users or not. Generally the rejected users are enclosed in the
    problem-list file. An overall report is displayed at the top of the
    cache refresh page with headings **Updated at the last run** and
    **Problems at the last run**.

  * _Snapshot Count:_ This defines the total number of snapshots that
    are allowed to be saved in the hard drive of the VM. It is recommended
    to be kept to 20 snapshots.

The Gluu Server 3.x introduced two upgraded sections here.

  * _Server IP Address:_ Include the IP of your Gluu Server here. This
    feature helps to run Cache Refresh mechanism perfectly in a clustered
    environment.

  * _Removed Script File Name location:_ New version of the Gluu Server
    allows the administrator to manage your custom scripts with more
    interactive section under configuration named Manage Custom Scripts.

  * _Update:_ This button is used to push the changes in the Gluu
    Server. Hit this button only when the values have been entered,
    completely.

  * _Update and Validate Script:_ This button is used to test the
    operation and integrity of any custom script such as a Jython Script.
