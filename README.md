# docs-ce-prod

**Branch 3.0.1 for Gluu Server CE 3.0.1 production docs   
  Branch 2.4.4 for Gluu Server CE 2.4.4 Production docs    
  Branch 3.0.2 for Gluu Server CE 3.0.2 yet to be released**    
  
One Production repo to publish all the version of CE. This Repo will be organized with branches for each version.

Purpose:

Purpose of this repo is to publish only the site built using mkdocs. And below are the commands to build a site and push/merge it with repo from local system to remote repository. These commands are already scripted and added to the version of the documents, which would create a site with the version number.


```
#! /bin/bash
$git pull origin <branchname>
$echo -n "Enter task Performed >"
$read text
$echo "Entered Task: $text"
$git add -A
$git commit -m "updated site & - $text"
$git push origin <branchname>
```

##Cloning a repo to local machine:

To clone a repo use the below command

`#git clone <repo url>`

Once the repository is completely cloned. Do a pull to make sure that the files are in sycn with the remote(repository on Github).

`#git pull origin <branchname>`

!!! Note: 
	"Master" is also a branch.

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
