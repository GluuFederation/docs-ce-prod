# Gluu Server Backup

The Gluu Server should be backed up frequently--**we recommend at least one daily and one weekly backup of Gluu's data and/or VM.** 

There are multiple methods for backing up the Gluu Server. A few recommended strategies are provided below.

## VM Snapshot Backup

In the event of a production outage, a proper snapshot of the last working condition will help rapidly restore service. 

Most platform virtualization software and cloud vendors have snapshot backup features. For instance, Digital Ocean has Live Snapshot and Droplet Snapshot; VMWare has Snapshot Manager, etc. 

Snaphots should be taken for all Gluu environments (e.g. Prod, Dev, QA, etc.) and tested periodically to confirm consistency and integrity. 
 

## Tarball Method
Tarball the entire Gluu Server CE `chroot` folder using the `tar` command: 

1. Stop the server: `# service gluu-server-3.1.3 stop`
	
1. Use `tar` to take a backup: `# tar cvf gluu301-backup.tar /opt/gluu-server-3.1.3/`
	
1. Start the server again: `# service gluu-server-3.1.3 start`
	

## LDIF Data Backup
From time to time (daily or weekly) you will want to export the LDAP database to a standard LDIF format. If you have the data in plain text, it gives you some options for recovery that are not possible with a binary backup. 

In Gluu OpenDJ, you could stop the LDAP server and issue the following command (specifying the proper directory and file):

`/opt/opendj/bin/export-ldif -n userRoot -l /path/to/back/directory/<backup_file>.ldif`  

In Gluu OpenLDAP, you would do the following:

`/opt/symas/bin/slapcat -b "o=gluu" ` 

At runtime (if you don't want to stop the LDAP server), here is how you can dump data: 

`$ /opt/opendj/bin/export-ldif  --port 4444  --hostname localhost  --bindDN "cn=Directory Manager" --bindPassword [password_of_ldap_admin] --includeBranch o=gluu --backendID userRoot --ldifFile /tmp/backup_o_gluu_data.ldif  --trustAll`

Data can be imported with a command, like below: 

`$ /opt/opendj/bin/import-ldif --port 4444 --hostname localhost --bindDN "cn=Directory Manager" --bindPasswordFile /home/ldap/.pw --includeBranch o=gluu --backendID userRoot --ldifFile /tmp/backup_o_gluu_data.ldif --trustAll --clearBackend --rejectFile /tmp/rejected_data_why.ldif` 

<!--
## Script Method

1. Login to Gluu chroot
	a. # service gluu-server-3.1.3 login
2. Fetch export script from Gluu 
	b. wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py
3. Change permission of the script
	c. # chmod +x export24.py
4. run the script
	d. # ./export24.py

The export script will generate a directory called  backup_24  which will have all the data backed up from the 
current installation. Check the log file generated in the directory for any errors.
-->
