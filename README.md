# Yet Another Blackjack Server (YABS)

This is an implementation of simple blackjack game in Python using Flask as HTTP server.
Main idea is to allow writing bots that will play against croupier.
At this moment this implementation allows only playing against croupier 1 vs 1.

# Rules
Goto: [rules](docs/rules.md)

# API
Goto: [api](docs/api.md)
    

##Virtualenvwrapper
Based on [documentation](https://virtualenvwrapper.readthedocs.io/en/latest/).

First time:
```
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv env3-blackjack -p python3
$ workon env3-blackjack
$ pip install -r requirements.txt
```

Then:
```
$ workon env3-blackjack
```


