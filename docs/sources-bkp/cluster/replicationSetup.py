#!/usr/bin/python
 
# This script enables replication between n number of servers as prompted. 
# Pay attention to the default values below and make sure they are set
# correctly. Also remember that replication can be tricky, so keep calm
# if things aren't going well.
#
# written by Nicholas Geyer <ng@gluu.org>
 
import os, getpass
 
# Default Values
cmd             = '/opt/opendj/bin/dsreplication'
subCommand      = 'enable'
adminPort       = '4444'
replPort        = '8989'
adminUID        = 'admin'
bindDN          = '"cn=Directory Manager"'
baseDN          = '"o=gluu"'
 
# Password for replication admin user.
adminPW         = getpass.getpass('Create a password for the replication admin: ')
 
# Get number of servers and verify that it is actually a number.
numServers      = raw_input('Enter number of OpenDJ servers: ')
while True:
        try:
                numServers = int(numServers)
                break
        except:
                numServers = raw_input('Please Enter a Positive Integer: ')
 
# Hostname and password of the first server.
mainHost        = raw_input('Enter the hostname of server 1: ')
mainPW          = getpass.getpass('Enter the Directory Manager password for %s:' 
                                                                % mainHost)
 
# Hostnames and passwords of of the rest of the servers, along with replication
# enable command.
for i in range(numServers-1):
        host    = raw_input('Enter the hostname of server %s: ' % (i+2))
        passwd  = getpass.getpass('Enter the Directory Manager password for %s:' 
                                                                % host)
        os.system("""%s %s -I %s -w '%s' -b %s -h %s -p %s -D %s --bindPassword1 \
                '%s' -r %s -O %s --port2 %s --bindDN2 %s --bindPassword2 '%s' -R %s \
                --secureReplication1 --secureReplication2 -X -n""" % (cmd, 
                        subCommand, adminUID, adminPW, baseDN, mainHost, adminPort,
                        bindDN, mainPW, replPort, host, adminPort, bindDN, passwd,
                        replPort))
print 'Enabling Replication Complete.'
