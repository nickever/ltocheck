#!/usr/bin/env bash

# Installer for ltocheck. Please run this from the ltocheck dir

echo "Installing terminal packages"

DIR="$( pwd )"

# Install Homebrew
echo "Homebrew..."
which -s brew
if [[ $? != 0 ]] ; then
    echo "...installing"
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    echo "...already installed, updating"
    brew update
fi

# Install python 3.x (default with macOS is 2.6.9)
echo "Python..."
which -s /usr/local/bin/python
if [[ $? != 0 ]] ; then
    echo "...installing"
    brew install python
else
    echo "...already installed, updating"
    brew upgrade python
fi

# Install ltocheck v1.x
echo "ltocheck..."
which -s /usr/local/bin/ltocheck
if [[ $? != 0 ]] ; then
    echo "...installing"
    sudo pip3 install -e "${DIR}" || sudo pip install -e "${DIR}"
else
    echo "...already installed"
fi

echo "DONE"
