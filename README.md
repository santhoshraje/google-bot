# Robust Bot

<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
</a>

Telegram bot with cool features like:
 - Multithreading support
 - Scheduling support
 - RSS engine
    - Periodically receive trending searches from Google
      - Supported countries:
        - Singapore
 
 ## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development, testing and deployment purposes.

### Prerequisites
```
pip install -r requirements.txt
```

### Usage

#### Script

from example.py:
```
from bot import Bot

def main():
    # path to config file. remember to input your telegram bot token
    bot = Bot('config.json')
    # start the bot
    bot.start_bot()

if __name__ == '__main__':
    main()
```

run the script:

```
python example.py
```
script will run until you stop it with CTRL + C / CMD + C

#### Bot 

Subscribe to Google tending searches:
```
/trending
```

## Deployment

You may host the bot on any server that has python 3 installed

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

