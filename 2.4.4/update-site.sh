#! /bin/bash
git pull
mkdocs build
rm -rf docs/
rm -rf 2.4.4/
mv site/ 2.4.4/
echo -n "Enter task Performed >"
read text
echo "Entered Task: $text"

git add -A
git commit -m "updated site & - $text"
git push origin 2.4.4
