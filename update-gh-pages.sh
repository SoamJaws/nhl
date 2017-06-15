#!/usr/bin/env bash

git pull origin master

HTML_CONTENT=$(./nhl html)
STASHED=false

git checkout gh-pages
if [[ "$?" != 0 ]]; then
	git stash
	git checkout gh-pages
	STASHED=true
fi

git pull origin gh-pages
echo "$HTML_CONTENT" > index.html

git add index.html
git commit -m "Updated stats"

git push origin gh-pages
git checkout -

if [[ "$STASHED" = true ]]; then
	git stash pop -q
fi
