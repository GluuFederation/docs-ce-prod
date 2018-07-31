#!/usr/bin/python

import os
import time
import glob
import re
import shutil
import json
import base64
from pyDes import *

import ldap
import ldap.modlist as modlist
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

def parse_setup_properties(prop_file='/install/community-edition-setup/setup.properties.last'):
    setup_prop = dict()
    content = open(prop_file).readlines()
    for l in content:
        ls = l.strip()
        if ls:
            if not ls[0] == '#':
                eq_loc = ls.find('=')

                if eq_loc > 0:
                    k = ls[:eq_loc]
                    v = ls[eq_loc+1:]
                    v=v.replace('\\=','=')
                    v=v.replace("\\'","'")
                    v=v.replace('\\"','"')
                    if v == 'True':
                        v = True
                    elif v == 'False':
                        v = False
                    setup_prop[k] = v

    return setup_prop
    
def get_ldap_admin_password():    
    salt_file = open('/etc/gluu/conf/salt').read()
    salt = salt_file.split('=')[1].strip()
    ox_ldap_properties_file = '/etc/gluu/conf/ox-ldap.properties'
    for l in open(ox_ldap_properties_file):
        if l.startswith('bindPassword'):
            s = l.split(':')[1].strip()
            engine = triple_des(salt, ECB, pad=None, padmode=PAD_PKCS5)
            cipher = triple_des(salt)
            decrypted = cipher.decrypt(base64.b64decode(s), padmode=PAD_PKCS5)
            return decrypted

class GluuUpdater:
    def __init__(self):
        self.setup_properties = parse_setup_properties()

        if self.setup_properties.get('ldap_type'):
            self.ldap_type = self.setup_properties['ldap_type']
        else:
            self.ldap_type = 'openldap'
    
        self.ldap_host = 'localhost'
        
        if self.ldap_type == 'opendj':
            self.ldap_bind_dn = self.setup_properties['opendj_ldap_binddn']
        elif self.ldap_type == 'openldap':
            self.ldap_bind_dn = self.setup_properties['ldap_binddn']
            
        self.ldap_bind_pw = get_ldap_admin_password()
        self.inumOrg = self.setup_properties['inumOrg']
        self.hostname = self.setup_properties['hostname'] 

    def ldappConn(self):
        self.conn = ldap.initialize('ldaps://{0}:1636'.format(self.ldap_host))
        self.conn.simple_bind_s(self.ldap_bind_dn, self.ldap_bind_pw)
        

    def updatePassport(self):

        if not os.path.exists('/etc/certs/passport-sp.key'):
            print "Creating passport certificates"
            os.system('/usr/bin/openssl genrsa -des3 -out /etc/certs/passport-sp.key.orig -passout pass:secret 2048')
            os.system('/usr/bin/openssl rsa -in /etc/certs/passport-sp.key.orig -passin pass:secret -out /etc/certs/passport-sp.key')
            os.system('/usr/bin/openssl req -new -key /etc/certs/passport-sp.key -out /etc/certs/passport-sp.csr -subj /C={0}/ST={1}/L={2}/O={3}/CN={4}/emailAddress={5}'.format(
                            self.setup_properties['countryCode'],
                            self.setup_properties['state'],
                            self.setup_properties['city'],
                            self.setup_properties['orgName'],
                            self.setup_properties['orgName'],
                            self.setup_properties['admin_email']
                        ))
            os.system('/usr/bin/openssl x509 -req -days 365 -in /etc/certs/passport-sp.csr -signkey /etc/certs/passport-sp.key -out /etc/certs/passport-sp.crt')
            os.system('chown root:gluu /etc/certs/passport-sp.key.orig')
            os.system('chmod 440 /etc/certs/passport-sp.key.orig')
            os.system('chown root:gluu /etc/certs/passport-sp.key')
            os.system('chown node:node /etc/certs/passport-sp.key')
        
        
        print "Converting Passport Strategies to new style"
        #convert passport strategies to new style
        result = self.conn.search_s('o=gluu',ldap.SCOPE_SUBTREE,'(objectClass=oxPassportConfiguration)')
        dn = result[0][0]
        new_strategies = {}
        strategies = []
        change = False
        for pp_conf in result[0][1]['gluuPassportConfiguration']:
            pp_conf_js = json.loads(pp_conf)
            strategies.append(pp_conf_js['strategy'])
            if not pp_conf_js['strategy'] in new_strategies:
                if pp_conf_js['fieldset'][0].has_key('value'):
                    
                    if not '_client_' in pp_conf_js['fieldset'][0]['value']:
                        strategy={'strategy':pp_conf_js['strategy'], 'fieldset':[]}
                        for st_comp in pp_conf_js['fieldset']:
                            strategy['fieldset'].append({'value1':st_comp['key'], 'value2':st_comp['value'], "hide":False,"description":""})        
                        new_strategies[pp_conf_js['strategy'] ] = json.dumps(strategy)
                        change = True
                else:
                    new_strategies[pp_conf_js['strategy'] ] = pp_conf

        if change:
            new_strategies_list = new_strategies.values()
            self.conn.modify_s(dn, [( ldap.MOD_REPLACE, 'gluuPassportConfiguration',  new_strategies_list)])


        print "Modifying User's oxExternalUid entries ..."

        result = self.conn.search_s('o=gluu',ldap.SCOPE_SUBTREE,'(&(objectClass=gluuPerson)(oxExternalUid=*))')

        for people in result:
            dn = people[0]
            for oxExternalUid in people[1]['oxExternalUid']:
                strategy_p = oxExternalUid.split(':')
                new_oxExternalUid = []
                change = False
                if strategy_p[0] in strategies:
                    change = True
                    str_text = 'passport-{0}:{1}'.format(strategy_p[0],strategy_p[1]) 
                    new_oxExternalUid.append(str_text)
                else:
                    new_oxExternalUid.append(oxExternalUid)

                if change:                
                    self.conn.modify_s(dn, [(ldap.MOD_REPLACE, 'oxExternalUid',  new_oxExternalUid)])
        
updaterObj = GluuUpdater()
updaterObj.ldappConn()
updaterObj.updatePassport()

