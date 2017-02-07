# Yet Another Blackjack Server (YABS)
This is yet another blackjack game server (well not really another, but sounds cool).
We just wanted to write a simple card game that will enable writing bot clients.
This implementation allows only playing againts croupier 1 vs 1 but still allows to have much fun out of it.

## [Rules](docs/rules.md)
## [API](docs/api.md)
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
## Run server
```bash
python blackjack.py
# -a Host address (default: localhost)
# -p Port number  (default: 5000)
# -d Verbose mode (default: false)
```
## Run bots
`// TODO`
## Team
Members of summer semester 2016/2017 [KNSI (Python)](http://knsi.pwr.wroc.pl) scientific circle.
- [Adam Bobowski](https://github.com/Bobowski)
- [Mateusz Burniak](https://github.com/matbur95)
- [Adam Dołżycki](https://github.com/adolzycki)
- [Krzysztof Nowak](https://github.com/Fadion96)
- [Marcin Ostrowski](https://github.com/rnarcin)
- [Krzysztof Strzelecki](https://github.com/Creestoph)
- [Piotr Szyma](https://github.com/thompson2908)
- [Monika Tworek](https://github.com/MonikaTworek)
