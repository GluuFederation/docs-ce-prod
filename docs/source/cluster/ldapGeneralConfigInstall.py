#!/usr/bin/python
 
import getpass, os
 
cmd                     = '/opt/opendj/bin/dsconfig'
globalCommand   = 'set-global-configuration-prop'
passwordCommand = 'set-password-policy-prop'
host                    = 'localhost'
port                    = '4444'
bindDN                  = 'cn=Directory Manager'
bindPW                  = None
 
globalProps             = {     'single-structural-objectclass-behavior' : 'accept',
                                        'etime-resolution' : 'nanoseconds',
                                        'idle-time-limit' : '"120000 ms"',
                                        'size-limit' : '0',
                                        'lookthrough-limit' : '0'
                                        }
 
defaultpwp              = '--policy-name "Default Password Policy"'
defaultpwpProps = {     'allow-pre-encoded-passwords' : 'true'
                                        }
 
 
# Get password
bindPW = getpass.getpass('Password for %r:' % bindDN)
 
# Set Global Server Properties
propsString = ''
for prop in globalProps.keys():
        propsString = propsString + ' --set %s:%s' % (prop, globalProps[prop])
print 'Setting Global properties...'
os.system("""%s %s -p %s -h %s -D %r -w %s%s -X -n"""
                % (cmd, globalCommand, port, host, bindDN, bindPW, propsString))
 
# Set Default Password Policy Properties
propsString = ''
for prop in defaultpwpProps.keys():
        propsString = propsString + ' --set %s:%s' % (prop, defaultpwpProps[prop])
print 'Setting Default Password Policy properties...'
os.system("""%s %s -p %s -h %s -D %r -w %s %s%s -X -n"""
                % (cmd, passwordCommand, port, host, bindDN, bindPW, defaultpwp, propsString))
