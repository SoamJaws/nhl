#!/usr/bin/env bash

git fetch --all
git pull --all

git checkout gh-pages
git rebase master

./nhl html > index.html

git add index.html
git commit -m "Updated stats gh-pages"

git push origin gh-pages
git checkout -
