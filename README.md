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

## Installation
Its recommended to use virtualenv for meeting package requirements.
Script below will create `venv` directory inside current working directory and install all necessary dependencies.
```bash
#!/bin/bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
Before starting the application we have to activate venv.
```bash
source venv/bin/activate
```
Deactivating is done by simply writing `deactivate`.
