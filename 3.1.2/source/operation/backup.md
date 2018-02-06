# Gluu Server Backup

The Gluu Server should be backed up frequently--**we recommend at least one daily and one weekly backup of Gluu Server's data and/or VM.** 

There are multiple methods for backing up the Gluu Server. A couple recommended strategies are provided below.

## VM Snapshot Backup

VM Snapshot backup is highly recommended. A proper snapshot of 'last working condition' can help organization to become operational in little amount of time if any disastrous situation happen in production environment. Organization should keep VM snapshot periodically for Dev and QA if development and qualtiy assurance work continues. 

All platform virtualization softwares or cloud vendors has this feature available. Such as 'Live Snapshot' and 'Droplet Snapshot' are available for DigitalOcean or VMWare has 'Spanshot Manager' etc. 

It's a good practice to check the status of snapshots periodically to confirm it's consistency and integrity.   

## Tarball Method
Tarball the entire Gluu Server CE `chroot` folder using the `tar` command: 

1. Stop the server: `# service gluu-server-3.1.2 stop`
	
1. Use `tar` to take a backup: `# tar cvf gluu301-backup.tar /opt/gluu-server-3.1.2/`
	
1. Start the server again: `# service gluu-server-3.1.2 start`
	

## LDIF Data Backup
From time to time (daily or weekly) you will want to export the LDAP database to a standard LDIF format. If you have the data in plain text, it gives you some options for recovery that are not possible with a binary backup. 

In Gluu OpenDJ, you could stop the LDAP server and issue the following command (specifying the proper directory and file):

`/opt/opendj/bin/export-ldif -n userRoot -l /path/to/back/directory/<backup_file>.ldif`  

In Gluu OpenLDAP, you would do the following:

`/opt/symas/bin/slapcat -b "o=gluu" ` 

At runtime (if you don't want to stop the LDAP server), you can always use the `ldapsearch` command: 

`$ /opt/opendj/bin/export-ldif -n userRoot -l backup.ldif`


<!--
## Script Method

1. Login to Gluu chroot
	a. # service gluu-server-3.1.2 login
2. Fetch export script from Gluu 
	b. wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py
3. Change permission of the script
	c. # chmod +x export24.py
4. run the script
	d. # ./export24.py

The export script will generate a directory called  backup_24  which will have all the data backed up from the 
current installation. Check the log file generated in the directory for any errors.
-->
