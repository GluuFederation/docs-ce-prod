#How to back up Gluu CE Server

Gluu CE Server Back up can be performed using below methods.

* Using tar command to tar the Gluu Server Folder from the Host OS
* Using Gluu provided export and import scripts to back up ldif of the LDAP.

!!! NOTE: In this documentation,'2.4.x' is referred to the existing installed version of Gluu CE Server. 

##Tar command to Back up Gluu Server

###Steps to Back up Gluu CE server using tar

	1. Stop the server using below command
		a. #service gluu-server-2.4.x stop
	2. use tar command to take a back up
		b. # tar cvf gluu244-backup.tar /opt/gluu-server-2.4.4/
	
## Using Gluu Script to Back up Ldif of LDAP

### Steps to Back up Gluu CE Server using Gluu Export Scripts
	1. Login to Gluu chroot
		a. # service gluu-server-2.4.x login
	2. Fetch export script from Gluu 
		b. wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py
	3. Change permission of the script
		c. # chmod +x export24.py
	4. run the script
		d. # ./export24.py
The export script will generate a directory called  backup_24  which will have all the data backed up from the current installation. Check the log file generated in the directory for any errors.
