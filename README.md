# docs-ce-prod

**Branch 3.0.1 for Gluu Server CE 3.0.1 production docs   
  Branch 2.4.4 for Gluu Server CE 2.4.4 Production docs    
  Branch 3.0.2 for Gluu Server CE 3.0.2 yet to be released**    

This repo is holds all versions of CE docs and includes scripts to publish.  All docs are processed using mkdocs. This Repo is organized with branches for each version of the documentation.

## Clone
`$ git clone https://github.com/GluuFederation/docs-ce-prod.git`

## Check out specific branch
`$ git checkout <branchname>`

## Update (for those who have privileges)
```
/path/to/repo/branchname (branchname)
$ ./update-site-local-sh
```

Note: 
   "Master" is a branch for editing this `README.md`.  You will not see documentation files until you check out the specific branch.


Additional Details:
To make configiration changes on Apache httpd, edit the below file, only if required.

```
$ vi /etc/apache2/sites-available/docs.conf

```
