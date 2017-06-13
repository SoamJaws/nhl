echo -e "Starting to update gh-pages\n"

#copy data we're interested in to other place

#go to home and setup git
cd $HOME
git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis"

#using token clone gh-pages branch
git clone https://${GH_TOKEN}@github.com/SoamJaws/nhl.git

#go into directory and copy data we're interested in to that directory
cd nhl
git remote rm origin
git remote add origin https://${GH_TOKEN}@github.com/SoamJaws/nhl.git
git checkout gh-pages
git rebase master
./nhl html > index.html

#add, commit and push files
git add index.html
git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to gh-pages"
git push origin gh-pages
