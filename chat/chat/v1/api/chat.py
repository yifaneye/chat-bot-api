# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from rivescript import RiveScript

from . import Resource

bot = RiveScript()
bot.load_directory("./v1/api/brain/")
bot.sort_replies()


class Chat(Resource):

    @staticmethod
    def get():
        message = g.args.get("message")
        print(f'You> {message}')
        reply = bot.reply("localuser", message)
        if reply == "[ERR: No Reply Matched]":
            reply = "Sorry, I can't understand. Please message me 'hi bot', 'how are you', 'where are you from', 'hi', 'my name is ...', 'i am happy', 'i am excited', 'i am thrilled'."
        print(f'Bot> {reply}')
        return {'reply': reply}, 200, None
