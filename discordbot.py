from discord.ext import commands
import os
import traceback
import discord
import re
import requests
import bs4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import numpy as np

token = os.environ['DISCORD_BOT_TOKEN']


client = discord.Client()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    elif message.content == 'イマイ':
        await message.channel.send('Hi.')
        
    else:
        return
        
client.run(token)
