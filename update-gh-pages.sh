#!/usr/bin/env bash

git pull --all

./nhl html > index.html
git stash
git checkout gh-pages
git stash pop

git add index.html
git commit -m "Updated stats"

#git push origin gh-pages
git checkout -
