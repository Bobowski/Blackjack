# Yet Another Blackjack Server (YABS)
This is yet another blackjack game server (well not really another, but sounds cool).
We just wanted to write a simple card game that will enable writing bot clients.
This implementation allows only playing againts croupier 1 vs 1 but still allows to have much fun out of it.

## [Rules](docs/rules.md)
## [API](docs/api.md)
## Team
`// TODO`
## Run server
`// TODO`
## Run bots
`// TODO`

##Virtualenvwrapper
Based on [documentation](https://virtualenvwrapper.readthedocs.io/en/latest/).

First time:
```bash
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv env3-blackjack -p python3
$ workon env3-blackjack
$ pip install -r requirements.txt
```

Then:
```bash
$ workon env3-blackjack
```


