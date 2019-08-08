# oxTrust APIs

## Overview

This page is a work in progress. While it's being constructed, temporary API documentation can be found [here](https://gluu.org/docs/oxtrustapi/)

!!! Important
    oxTrust API support is only guaranteed for customers with a [VIP subscription](https://www.gluu.org/pricing#vip).
    
## Available APIs

| API | Description |
| --- | ----------- |
| [addClientToUmaResource](#addclienttoumaresource) | |
| [addGroupMember](#addgroupmember)| |
| [addClientToUmaResource](#addclienttoumaresource)  | |
| [addGroupMember](#addgroupmember) | |
| [addRadiusClient](#addradiusclient) | |
| [addScopeToClient](#addscopetoclient) | |
| [addScopeToUmaResource](#addscopetoumaresource) | |
| [create](#create) | |
| [createAttribute](#createattribute) | |
| [createClient](#createclient) | |
| [createCustomScript](#createcustomscript) | |
| [createGroup](#creategroup) | |
| [createPassportProvider](#createpassportprovider) | |
| [createPerson](#createperson) | |
| [createScope](#createscope) | |
| [createSectorIdentifier](#createsectoridentifier) | |
| [createUmaResource](#createumaresource) | |
| [createUmaScope](#createumascope) | |
| [delete](#delete) | |
| [deleteAllProviders](#deleteallproviders) | |
| [deleteAllUmaScopes](#deleteallumascopes) | |
| [deleteAttribute](#deleteattribute) | |
| [deleteAttributes](#deleteattributes) | |
| [deleteClient](#deleteclient) | |
| [deleteClientScopes](#deleteclientscopes) | |
| [deleteClients](#deleteclients) | |
| [deleteCustomScript](#deletecustomscript) | |
| [deleteGroup](#deletegroup) | |
| [deleteGroupMembers](#deletegroupmembers) | |
| [deleteGroups](#deletegroups) | |
| [deletePeople](#deletepeople) | |
| [deletePerson](#deleteperson) | |
| [deleteProvider](#deleteprovider) | |
| [deleteRadiusClient](#deleteradiusclient) | |
| [deleteScope](#deletescope) | |
| [deleteScopes](#deletescopes) | |
| [deleteSectorIdentifier](#deletesectoridentifier) | |
| [deleteUmaResource](#deleteumaresource) | |
| [deleteUmaScope](#deleteumascope) | |
| [getAllActivesAttributes](#getallactivesattributes) | |
| [getAllAttributes](#getallattributes) | |
| [getAllInActivesAttributes](#getallinactivesattributes) | |
| [getAllScopes](#getallscopes) | |
| [getAllSectorIdentifiers](#getallsectoridentifiers) | |
| [getAttributeByInum](#getattributebyinum) | |
| [getCasConfig](#getcasconfig) | |
| [getClientByInum](#getclientbyinum) | |
| [getClientScope](#getclientscope) | |
| [getConfiguration](#getconfiguration) | |
| [getCurrentAuthentication](#getcurrentauthentication) | |
| [getCustomScriptsByInum](#getcustomscriptsbyinum) | |
| [getGroupByInum](#getgroupbyinum) | |
| [getGroupMembers](#getgroupmembers) | |
| [getOxAuthJsonSettings](#getoxauthjsonsettings) | |
| [getOxtrustJsonSettings](#getoxtrustjsonsettings) | |
| [getOxtrustSettings](#getoxtrustsettings) | |
| [getPassportBasicConfig](#getpassportbasicconfig) | |
| [getPersonByInum](#getpersonbyinum) | |
| [getProviderById](#getproviderbyid) | |
| [getRadiusClient](#getradiusclient) | |
| [getScopeByInum](#getscopebyinum) | |
| [getScopeClaims](#getscopeclaims) | |
| [getSectorIdentifierById](#getsectoridentifierbyid) | |
| [getServerConfig](#getserverconfig) | |
| [getServerStatus](#getserverstatus) | |
| [getSmtpServerConfiguration](#getsmtpserverconfiguration) | |
| [getUmaResourceById](#getumaresourcebyid) | |
| [getUmaResourceClients](#getumaresourceclients) | |
| [getUmaResourceScopes](#getumaresourcescopes) | |
| [getUmaScopeByInum](#getumascopebyinum) | |
| [listCertificates](#listcertificates) | |
| [listClients](#listclients) | |
| [listCustomScripts](#listcustomscripts) | |
| [listCustomScriptsByType](#listcustomscriptsbytype) | |
| [listGroups](#listgroups) | |
| [listPeople](#listpeople) | |
| [listProviders](#listproviders) | |
| [listRadiusClients](#listradiusclients) | |
| [listUmaResources](#listumaresources) | |
| [listUmaScopes](#listumascopes) | |
| [read](#read) | |
| [removeClientToUmaResource](#removeclienttoumaresource) | |
| [removeGroupMember](#removegroupmember) | |
| [removeScopeToClient](#removescopetoclient) | |
| [removeScopeToUmaResource](#removescopetoumaresource) | |
| [searchAttributes](#searchattributes) | |
| [searchGroups](#searchgroups) | |
| [searchGroups1](#searchgroups1) | |
| [searchGroups2](#searchgroups2) | |
| [searchScope](#searchscope) | |
| [searchSectorIdentifier](#searchsectoridentifier) | |
| [searchUmaResources](#searchumaresources) | |
| [searchUmaScopes](#searchumascopes) | |
| [status](#status) | |
| [status1](#status1) | |
| [testSmtpConfiguration](#testsmtpconfiguration) | |
| [update](#update) | |
| [update1](#update1) | |
| [updateAttribute](#updateattribute) | | 
| [updateAuthenticationMethod](#updateauthenticationmethod) | | 
| [updateClient](#updateclient) | | 
| [updateCustomScript](#updatecustomscript) | | 
| [updateGroup](#updategroup) | |
| [updateGroup1](#updategroup1) | |
| [updateOxauthJsonSetting](#updateoxauthjsonsetting) | | 
| [updateOxtrustJsonSetting](#updateoxtrustjsonsetting) | |
| [updateOxtrustSetting](#updateoxtrustsetting) | |
| [updatePassportBasicConfig](#updatepassportbasicconfig) | |
| [updatePassportProvider](#updatepassportprovider) | |
| [updateRadiusClient](#updateradiusclient) | |
| [updateScope](#updatescope) | |
| [updateSectorIdentifier](#updatesectoridentifier) | | 
| [updateServerConfiguration](#updateserverconfiguration) | |
| [updateSmtpConfiguration](#updatesmtpconfiguration) | |
| [updateUmaResource](#updateumaresource) | |
| [updateUmaScope](#updateumascope)| |


## API References

### addClientToUmaResource

### addGroupMember

### addRadiusClient

### addScopeToClient

### addScopeToUmaResource

### create

### createAttribute

### createClient

### createCustomScript

### createGroup

### createPassportProvider

### createPerson

### createScope

### createSectorIdentifier

### createUmaResource

### createUmaScope

### delete

### deleteAllProviders

### deleteAllUmaScopes

### deleteAttribute

### deleteAttributes

### deleteClient

### deleteClientScopes

### deleteClients

### deleteCustomScript

### deleteGroup

### deleteGroupMembers

### deleteGroups

### deletePeople

### deletePerson

### deleteProvider

### deleteRadiusClient

### deleteScope

### deleteScopes

### deleteSectorIdentifier

### deleteUmaResource

### deleteUmaScope

### getAllActivesAttributes

### getAllAttributes

### getAllInActivesAttributes

### getAllScopes

### getAllSectorIdentifiers

### getAttributeByInum

### getCasConfig

### getClientByInum

### getClientScope

### getConfiguration

### getCurrentAuthentication

### getCustomScriptsByInum

### getGroupByInum

### getGroupMembers

### getOxAuthJsonSettings

### getOxtrustJsonSettings

### getOxtrustSettings

### getPassportBasicConfig

### getPersonByInum

### getProviderById

### getRadiusClient

### getScopeByInum

### getScopeClaims

### getSectorIdentifierById

### getServerConfig

### getServerStatus

### getSmtpServerConfiguration

### getUmaResourceById

### getUmaResourceClients

### getUmaResourceScopes

### getUmaScopeByInum

### listCertificates

### listClients

### listCustomScripts

### listCustomScriptsByType

### listGroups

### listPeople

### listProviders

### listRadiusClients

### listUmaResources

### listUmaScopes

### read

### removeClientToUmaResource

### removeGroupMember

### removeScopeToClient

### removeScopeToUmaResource

### searchAttributes

### searchGroups

### searchGroups1

### searchGroups2

### searchScope

### searchSectorIdentifier

### searchUmaResources

### searchUmaScopes

### status

### status1

### testSmtpConfiguration

### update

### update1

### updateAttribute

### updateAuthenticationMethod

### updateClient

### updateCustomScript

### updateGroup

### updateGroup1

### updateOxauthJsonSetting

### updateOxtrustJsonSetting

### updateOxtrustSetting

### updatePassportBasicConfig

### updatePassportProvider

### updateRadiusClient

### updateScope

### updateSectorIdentifier

### updateServerConfiguration

### updateSmtpConfiguration

### updateUmaResource

### updateUmaScope
