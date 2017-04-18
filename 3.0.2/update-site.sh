#! /bin/bash
git pull
mkdocs build
rm -rf latest/
rm -rf 3.0.2/
mv site/ 3.0.2/
echo -n "Enter task Performed >"
read text
echo "Entered Task: $text"

git add -A
git commit -m "updated site & - $text"
git push origin 3.0.2
