# Gluu Server Backup

The Gluu Server should be backed up frequently--**we recommend at least one daily and one weekly backup of Gluu's data and/or VM.** 

There are multiple methods for backing up the Gluu Server. A few recommended strategies are provided below.

## VM Snapshot Backup

In the event of a production outage, a proper snapshot of the last working condition will help rapidly restore service. 

Most platform virtualization software and cloud vendors have snapshot backup features. For instance, Digital Ocean has Live Snapshot and Droplet Snapshot; VMWare has Snapshot Manager, etc. 

Snaphots should be taken for all Gluu environments (e.g. Prod, Dev, QA, etc.) and tested periodically to confirm consistency and integrity. 

## Tarball Method
All Gluu Server files live in a single folder: `/opt`. The entire Gluu Server CE `chroot` folder can be archived using the `tar` command: 

1. Stop the server: `# service gluu-server-4.0 stop`
	
1. Use `tar` to take a backup: `# tar cvf gluu40-backup.tar /opt/gluu-server-4.0/`
	
1. Start the server again: `# service gluu-server-4.0 start`

## LDIF Data Backup
From time to time (daily or weekly), the LDAP database should be exported in a standard LDIF format. Having the data in plain text offers some options for recovery that are not possible with a binary backup. 

Instructions are provided below for exporting OpenDJ data. The below instructions address situations where unused and expired cache and session related entries are piling and causing issues with functionality. Read more about this [issue](https://www.gluu.org/blog/managing-cache-in-the-gluu-server/).

### OpenDJ 

Errors that this may help fix include but are not restricted to: 

- Out of Memory

If your Gluu Server is backed by OpenDJ, follow these steps to backup your data:

1. First check your cache entries by running the following command:

    ```bash
    /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' -T 'oxAuthGrantId=*' dn | grep 'dn:' | wc –l
    ```
    
1. Dump the data as LDIF

    - Log in to root:
		
    ```bash
    sudo su -
    ```

    - Log in to Gluu-Server-4.0:   

    ```bash
    service gluu-server-4.0 login
    ```

    - Stop Identity, oxAuth, and OpenDJ services:

    ```bash
    service identity stop
    ```

    ```bash
    service oxauth stop
    ```

    ```bash
    /opt/opendj/bin/stop-ds
    ```

    - If you are moving to a new LDAP, copy over your schema files from the following directory. Otherwise simply copy it for backup:

    ```bash
    /opt/opendj/config/schema/
    ```

    - Now export the LDIF and save it somewhere safe. You will not be importing this if you choose to apply any filters as below:

    ```bash
    /opt/opendj/bin/export-ldif -n userRoot -l exactdatabackup_date.ldif
    ```

    - Now exclude `oxAuthGrantId` so the command becomes:

    ```bash
    /opt/opendj/bin/export-ldif -n userRoot -l yourdata_withoutoxAuthGrantId.ldif --includeFilter '(!(oxAuthGrantId=*))'
    ```

    - You may also wish to exclude `oxMetric` so the command becomes:

    ```bash
    /opt/opendj/bin/export-ldif -n userRoot -l yourdata_withoutGrantIdMetic.ldif --includeFilter '(&(!(oxAuthGrantId=*))(!			(objectClass=oxMetric)))'
    ```

1. Now, **only if needed**, rebuild indexes:

    - Check status of indexes: 

    ```bash
    /opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
    ```

    Take note of all indexes that need to be rebuilt. **If no indexing is needed, move on to step 4.**

    - Start OpenDJ to build backend index :

    ```bash
    /opt/opendj/bin/start-ds
    ```

    - Build backend index for all indexes that need it accoring to previous status command, change passoword `-w` and index name accordingly. This command has to be run for every index separately: 

    ```bash
    /opt/opendj/bin/dsconfig create-backend-index --port 4444 --hostname localhost --bindDN "cn=directory manager" -w password --backend-name userRoot --index-name iname --set index-type:equality --set index-entry-limit:4000 --trustAll --no-prompt
    ```

    - Stop OpenDJ:

    ```bash
    /opt/opendj/bin/stop-ds
    ```

    - Rebuild the indexes as needed, here are examples : 

    ```bash
    /opt/opendj/bin/rebuild-index --baseDN o=gluu --index iname
    /opt/opendj/bin/rebuild-index --baseDN o=gluu --index uid
    /opt/opendj/bin/rebuild-index --baseDN o=gluu --index mail
    ```

    - Check status again :

    ```bash
    /opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
    ```

    - Verify indexes: 

    ```bash
    /opt/opendj/bin/verify-index --baseDN o=gluu --countErrors
    ```

1. Next import your previously exported ldif. Here, we are importing without  `oxAuthGrantId` . 
	
!!! Note
    You may import the exact export of your ldap `exactdatabackup_date.ldif`.Do not import your exact copy of your LDIF if you are following instructions to to clean your cache entries
	
    ```bash
    /opt/opendj/bin/import-ldif -n userRoot -l yourdata_withoutoxAuthGrantId.ldif
    ```
    
    If you moved to a new LDAP, copy back your schema files to this directory:

    ```bash
    /opt/opendj/config/schema/
    ```
    
1. Start Identity, oxAuth, and OpenDJ services:

    ```bash
    /opt/opendj/bin/start-ds
    ```

    ```bash
    service identity start
    ```

    ```bash
    service oxauth start
    ```

1. Finally, verify the cache entries have been removed:

    ```bash
    /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' -T 		'oxAuthGrantId=*' dn | grep 'dn:' | wc –l
    ```

You should be done and everything should be working perfectly. You may notice your Gluu Server responding slower than before. That is expected -- your LDAP is adjusting to the new data, and indexing might be in process. Give it some time and it should be back to normal.
