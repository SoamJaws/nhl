#!/usr/bin/env bash

git pull --all

HTML_CONTENT=$(./nhl html)
git checkout gh-pages
echo "$HTML_CONTENT" > index.html

git add index.html
git commit -m "Updated stats"

git push origin gh-pages
git checkout -
