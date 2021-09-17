# TelegramBotPython

This is a Bot-Assistant based in Python `Telegram API`. 

You can see inline buttons, keyboard markups and conversation handler. 

Video:

[![Alt text](https://img.youtube.com/vi/Ug6lXqyniPs/0.jpg)](https://www.youtube.com/watch?v=Ug6lXqyniPs)


# Python virtual environment

To create a new python virtual environment use these commans:

```sh
python -m venv env # Create a virtual env
source backend/env/bin/activate # activate virtual env
```

and for deactivate the venvironment run `deactivate`

To install all packages run:
```sh
pip install -r requirements.py
```

# Test Project

First clone the repo with `git clone`.

You have to create a bot through BotFather, for more information visit https://core.telegram.org/bots to create bots and customize them.

When you have your bot `Api-Token`, you have to replace in `main.py`
```sh
API_TOKEN = 'HERE YOUR API-TOKEN'
```

To start the Bot run:
```sh
python main.py
```

Now you can use telegram to contact the send messages to the virtual assistant.



