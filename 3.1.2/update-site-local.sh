#! /bin/bash
git pull origin 3.1.2
echo -n "Enter task Performed >"
read text
echo "Entered Task: $text"

git add -A
git commit -m "updated site & - $text `date +'%Y-%m-%d %H:%M:%S'`"
git push origin 3.1.2
echo -n "Time Commited and Merged : `date +'%Y-%m-%d %H:%M:%S'`"
