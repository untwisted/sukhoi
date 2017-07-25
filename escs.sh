##############################################################################
# clone, sukhoi, github.
cd ~/projects
git clone git@github.com:iogf/sukhoi.git sukhoi-code
##############################################################################
# push, sukhoi, github.
cd ~/projects/sukhoi-code
git status
git add *
git commit -a
git push 
##############################################################################
# create the develop branch, sukhoi.
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# merge master into development, sukhoi.
cd ~/projects/sukhoi-code
git checkout development
git merge master
git push
##############################################################################
# merge development into master, sukhoi.
cd ~/projects/sukhoi-code
git checkout master
git merge development
git push
git checkout development
##############################################################################
# check diffs, sukhoi.
cd ~/projects/sukhoi-code
git diff
##############################################################################
# delete the development branch, sukhoi.
git branch -d development
git push origin :development
git fetch -p 
##############################################################################
# undo, changes, sukhoi, github.
cd ~/projects/sukhoi-code
git checkout *
##############################################################################
# create, a new branch locally from an existing commit, from, master.
git checkout master
cd ~/projects/sukhoi-code
git checkout -b old_version fcebcd4f229cb29cac344161937d249785bf83f8
git push --set-upstream origin old_version

git checkout old_version
##############################################################################
# delete, old version, sukhoi.
git checkout master
git branch -d old_version
git push origin :old_version
git fetch -p 
##############################################################################
# create, toc, table of contents, sukhoi.
cd ~/projects/sukhoi-code
gh-md-toc BOOK.md > table.md
vy table.md
rm table.md
##############################################################################
# install, sukhoi.
sudo bash -i
cd /home/tau/projects/sukhoi-code
python2 setup.py install
rm -fr build
exit
##############################################################################
# build, sukhoi, package, disutils.
cd /home/tau/projects/sukhoi-code
python2.6 setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# share, put, place, host, package, python, pip, application, sukhoi.

cd ~/projects/sukhoi-code
python2 setup.py sdist register upload
rm -fr dist
##############################################################################
# port to py3 code.

cd ~/projects/sukhoi-code

# Apply them.
2to3  -w .

find . -name "*.bak" -exec rm -f {} \;




