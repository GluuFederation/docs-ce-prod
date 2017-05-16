# docs-ce-prod
**3.0.1 Production Docs**

One Production repo to publish all the version of CE. This Repo will be organized with branches for each version.

Purpose:
And this site is created as "PRIVATE" so that to improvise the security on the documentation site we would be publishing. This would reduce outsiders forking or pulling our repositories for thier own site or purpose.

Purpose of this repo is to publish only the site built using mkdocs. And below are the commands to build a site and push/merge it with repo from local system to remote repository. These commands are already scripted and added to the version of the documents, which would create a site with the version number.


```
#! /bin/bash
$git pul
$mkdocs build
##$rm -rf latest/
$rm -rf 3.0.2/
$mv site/ 3.0.2/
$echo -n "Enter task Performed >"
$read text
$echo "Entered Task: $text"
$git add -Agit commit -m "updated site & - $text"
$git push origin master
```

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
You wouldbe using `stash` only if `pull` or `merge` fails.
