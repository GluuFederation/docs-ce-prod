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

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### addGroupMember

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### addRadiusClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### addScopeToClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### addScopeToUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### create

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createAttribute

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createCustomScript

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createGroup

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createPassportProvider

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createPerson

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createSectorIdentifier

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### createUmaScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### delete

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteAllProviders

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteAllUmaScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteAttribute

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteAttributes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteClientScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteClients

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteCustomScript

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteGroup

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteGroupMembers

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteGroups

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deletePeople

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deletePerson

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteProvider

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteRadiusClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteSectorIdentifier

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### deleteUmaScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAllActivesAttributes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAllAttributes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAllInActivesAttributes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAllScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAllSectorIdentifiers

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getAttributeByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getCasConfig

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getClientByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getClientScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getConfiguration

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getCurrentAuthentication

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getCustomScriptsByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getGroupByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getGroupMembers

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getOxAuthJsonSettings

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getOxtrustJsonSettings

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getOxtrustSettings

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getPassportBasicConfig

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getPersonByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getProviderById

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getRadiusClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getScopeByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getScopeClaims

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getSectorIdentifierById

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getServerConfig

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getServerStatus

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getSmtpServerConfiguration

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getUmaResourceById

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getUmaResourceClients

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getUmaResourceScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### getUmaScopeByInum

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listCertificates

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listClients

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listCustomScripts

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listCustomScriptsByType

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listGroups

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listPeople

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listProviders

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listRadiusClients

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listUmaResources

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### listUmaScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### read

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### removeClientToUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### removeGroupMember

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### removeScopeToClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### removeScopeToUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchAttributes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchGroups

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchGroups1

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchGroups2

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchSectorIdentifier

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchUmaResources

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### searchUmaScopes

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### status

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### status1

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### testSmtpConfiguration

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### update

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### update1

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateAttribute

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateAuthenticationMethod

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateCustomScript

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateGroup

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateGroup1

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateOxauthJsonSetting

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateOxtrustJsonSetting

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateOxtrustSetting

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updatePassportBasicConfig

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updatePassportProvider

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateRadiusClient

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateSectorIdentifier

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateServerConfiguration

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateSmtpConfiguration

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateUmaResource

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |

### updateUmaScope

**URL**

**HTTP Method**

**Response Type**

| Field | Data Type |
|---    | --- |
| | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| | |
