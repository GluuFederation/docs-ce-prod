# docs-ce-prod

**Branch 3.0.1 for Gluu Server CE 3.0.1 production docs   
  Branch 2.4.4 for Gluu Server CE 2.4.4 Production docs    
  Branch 3.0.2 for Gluu Server CE 3.0.2 yet to be released**    

This repo is holds all versions of CE docs and includes scripts to publish.  All docs are processed using mkdocs. This Repo is organized with branches for each version of the documentation.

  
```
/path/to/repo
```

## Clone
`$ git clone https://github.com/GluuFederation/docs-ce-prod.git`

## Check out specific branch
`$ git checkout <branchname>`

Note: 
   "Master" is a branch for editing this `README.md`.  You will not see documentation files until you check out the specific branch.

Do required changes, after the changes are done, pull again to make sure that there hasn't been any recent changes between your last pull and push that you would be performing.
Now, push the changes to the remote using the above script.

The above script, will pull the changes thats done, add or remove file that has been removed or added to the repo. Commit the changes using `commit` command and push the change.

```
#! /bin/bash
$git pul
$echo -n "Enter task Performed >"
$read text
$echo "Entered Task: $text"
$git add -A
$git commit -m "updated site & - $text"
$git push origin <branchname>
```

Just in case, if you run into issues, saying you are not able to push and you are recommended to pull. or you commit is n number changes behind, use stash to command make your local head to level with the latest commit.

`#git stash`

This will make your local branch or head to the latest and then do a push.

!!!Warning: 
	Please take extreme care, while pushing and stashing.



## Cloning a particular folder from a Branch:

!!!Note:
	Below commands and content is for **reference only**
	
The built site is synced in the webserver created to publish the documentation website to public. To sync only the site folder(version number directory, ie. 3.0.2 or 3.0.1), follow the commands below.

 ```
 $mkdir <repo>
 $cd <repo>
 ```
 To clone specific folder or directory from a repo is called sparse-checkout.
 
 And below are the steps to achieve that. It is enough to init and add the origin once. It will automatically fetch all the branches
 However, merging of the branches should be done separately.
 
```
$git initgit remote add -f origin <repo url>
$git config core.sparseCheckout true
$echo "3.0.2/" >> .git/info/sparse-checkout
$echo "another/sub/tree" >> .git/info/sparse-checkout
$git pull origin <branch>(master or branch name)
```

Additional Details:
To make configiration changes on Apache httpd, edit the below file, only if required.

```
$ vi /etc/apache2/sites-available/docs.conf

```
To Clone a particular branch with your local:

```
$git clone <repo url> --branch <branch name>
```
`git stash` can be used if your header is far behind than the remote.
And you could use 'commit' command to merge with remote.
You would be using `stash` only if `pull` or `merge` fails.
