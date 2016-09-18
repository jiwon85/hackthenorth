if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install python3
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo apt-get install python-virtualenv
    sudo apt-get install python3-pip
fi

pip3 install virtualenv
# Create the virtual env in a directory outside our github repo
cd ../
virtualenv -p python3 venv_hackthenorth
source venv_hackthenorth/bin/activate

# Install packages
cd hackthenorth/
pip3 install -r req.txt

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

pip3 install ipython
pip3 install newspaper3k
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
