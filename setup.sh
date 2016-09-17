pip install virtualenv
# Create the virtual env in a directory outside our github repo
cd ../
virtualenv venv_hackthenorth
source venv_hackthenorth/bin/activate

# Install packages
cd hackthenorth/
pip install -r req.txt

# Install news paper packages prereqs
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    # ...
    sudo apt-get install python-dev
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac OSX
    brew install libxml2 libxslt
    brew install libtiff libjpeg webp little-cms2
fi

pip install newspaper
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python2.7
