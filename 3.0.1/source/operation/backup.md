# Gluu Server Backup

The method of backing up Gluu Server CE is given below:

* Tarball Method: using `tar` command to tarball the entire 
Gluu Server CE `chroot` folder

<!-- * Script Method : using the provided export and 
import scripts to back up ldif of the LDAP. -->

## Tarball Method

1. Stop the server using below command
	a. # service gluu-server-3.0.1 stop
2. use tar command to take a backup
	b. # tar cvf gluu301-backup.tar /opt/gluu-server-3.0.1/
3. Start the server again
	a. # service gluu-server-3.0.1 start
	
<!--
## Script Method

1. Login to Gluu chroot
	a. # service gluu-server-3.0.1 login
2. Fetch export script from Gluu 
	b. wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py
3. Change permission of the script
	c. # chmod +x export24.py
4. run the script
	d. # ./export24.py

The export script will generate a directory called  backup_24  which will have all the data backed up from the 
current installation. Check the log file generated in the directory for any errors.
-->
