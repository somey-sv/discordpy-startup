from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

# インストールした discord.py を読み込む
import discord
import re
import requests
import bs4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import numpy as np

#どばすぽのヘッダー
dbsp_header = "https://shadowverse-portal.com/deck/"

#どばすぽからデッキを取得
def get_deck(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    names = soup.select(r".el-card-list-info-name-text")
    counts = soup.select(r".el-card-list-info-count")
    person = soup.select_one('.deck-summary-top-image')['alt']
    deck = {name.text: int(count.text[1:]) for name, count in zip(names, counts)}
    return deck, person

#クラス数をカウント
def deck_analysis(sv_class):

    global E,R,W,D,Nc,V,B,Nm

    if sv_class == 1:
        E+=1
    elif sv_class == 2:
        R+=1
    elif sv_class == 3:
        W+=1
    elif sv_class == 4:
        D+=1
    elif sv_class == 5:
        Nc+=1
    elif sv_class == 6:
        V+=1
    elif sv_class == 7:
        B+=1
    elif sv_class == 8:
        Nm+=1
    else:
        print("入力エラー")

E = R = W = D = Nc = V = B = Nm = 0

# メッセージ受信時に動作する処理
@bot.command()
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    elif "sv.j-cg.com" in message.content:

        #クラスカウンターの初期化
        global E,R,W,D,Nc,V,B,Nm
        E = R = W = D = Nc = V = B = Nm = 0

        #大会番号を取得
        compe = re.compile(r"\d\d\d\d")
        compe_num = compe.search(message.content).group()
        #大会のjsonファイルのURLを取得
        jcg_url = "https://sv.j-cg.com/compe/view/entrylist/" +  str(compe_num) + "/json"
        #大会情報のURLを取得
        info_url = "https://sv.j-cg.com/compe/"+str(compe_num)

        #大会情報を取得
        res_info = requests.get(info_url)
        res_info.encoding = res_info.apparent_encoding
        soup_info = bs4.BeautifulSoup(res_info.text, "html.parser")
        info = soup_info.select(".nobr")
        compe_info = [x.text for x in info]
        compe_info = " ".join(compe_info)

        #大会のjsonファイルを取得
        res_jcg = requests.get(jcg_url)
        res_jcg.encoding = res_jcg.apparent_encoding
        soup = bs4.BeautifulSoup(res_jcg.text, "html.parser")
        j_txt = json.loads(res_jcg.text)

        #クラス数の取得
        for i in range(len(j_txt["participants"])):
            if j_txt["participants"][i]["te"] == 0:
                continue
            elif j_txt["participants"][i]["te"] == 1:
                for j in range(2):
                    class_ij = j_txt["participants"][i]["dk"][j]["cl"]
                    deck_analysis(class_ij)
            else:
                continue

        classes_list = np.array([E, R, W, D, Nc, V, B, Nm])
        classes_label = ["E", "R", "W", "D", "Nc", "V", "B", "Nm"]
        colors = ["palegreen", "peachpuff", "mediumslateblue", "sienna","darkmagenta", "crimson", "wheat", "lightsteelblue"]

        fig1 = plt.figure()
        plt.pie(classes_list, labels=classes_label, colors=colors, autopct="%.1f%%",pctdistance=1.35,wedgeprops={'linewidth': 2, 'edgecolor':"white"})
        fig1.savefig("class_pie_" + compe_num + ".png")
        plt.close(fig1)

        fig2 = plt.figure()
        x = np.array(list(range(len(classes_label))))
        plt.bar(x, classes_list, tick_label=classes_label, color=colors)
        plt.ylabel("number of uses")
        for x, y in zip(x, classes_list):
            plt.text(x, y, y, ha='center', va='bottom')
        fig2.savefig("class_bar_" + compe_num + ".png")
        plt.close(fig2)

        analysed_data = [discord.File("class_pie_" + compe_num + ".png"),discord.File("class_bar_" + compe_num + ".png"),]
        await message.channel.send(compe_info)
        await message.channel.send(files=analysed_data)

    elif message.content == 'イマイ':
        await message.channel.send('Hi.')

bot.run(token)
