#############################################################################
#push code.

cd ~/projects/findjob-code
git status
git add *
git commit -a
git push -u origin master


cd ~/projects/findjob-code
sudo bash -i
pip install -r requirements.txt
python setup.py install 
rm -fr build
exit


