  #!/usr/bin/env python
# -*- coding: utf-8 -*-
from bot import Bot


def main():
    bot = Bot('config.json')
    bot.start_bot()

if __name__ == '__main__':
    main()