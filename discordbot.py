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

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_message(message):
    await message.channel.send('Hi.')

bot.run(token)
