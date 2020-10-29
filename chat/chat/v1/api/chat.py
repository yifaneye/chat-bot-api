# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os

from flask import g
from rivescript import RiveScript

from . import Resource

ERROR_MESSAGE = "[ERR: No Reply Matched]"
DEFAULT_REPLY = "Sorry, I can't understand. Please message me 'hi bot', 'how are you', 'where are you from', 'hi', 'my name is ...', 'i am happy', 'i am excited', 'i am thrilled'."

bot = RiveScript()
bot.load_directory(os.path.join(os.path.dirname(__file__), ".", "brain"))
bot.sort_replies()


class Chat(Resource):

    @staticmethod
    def get():
        message = g.args.get("message")
        print(f'You> {message}')
        reply = bot.reply("localuser", message)
        if reply == ERROR_MESSAGE:
            reply = DEFAULT_REPLY
        print(f'Bot> {reply}')
        return {'reply': reply}, 200, None
