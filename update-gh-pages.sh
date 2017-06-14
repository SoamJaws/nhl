#!/usr/bin/env bash

git pull origin master

HTML_CONTENT=$(./nhl html)
git checkout gh-pages
git pull origin gh-pages
echo "$HTML_CONTENT" > index.html

git add index.html
git commit -m "Updated stats"

git push origin gh-pages
git checkout -
