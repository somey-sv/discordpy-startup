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
import os

#どばすぽのヘッダー部分
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

E = R = W = D = Nc = V = B = Nm = 0
E1 = E2 = R1 = R2 = W1 = W2 = D1 = D2 = Nc1 = V1 = V2 = B1 = Nm1 = Nm2 = 0
OE = OR = OW = OD = ONc = OV = OB = ONm = 0
arche_list = ["Control_E", "MN_E", "Other_E", "Evolve_R", "MN_R", "Other_R", "N_W", "Spell_W", "Other_W", "MN_D", "Evolve_D", "Other_D", "Nc", "Other_Nc", "MN_V", "Midrange_V", "Other_V", "MN_B","Other_B", "AF_Nm", "MN_Nm", "Other_Nm"]

def deck_arche_analysis(sv_deck, sv_class):
    global E,R,W,D,Nc,V,B,Nm
    global E1,E2,R1,R2,W1,W2,D1,D2,Nc1,V1,V2,B1,Nm1,Nm2
    global OE,OR,OW,OD,ONc,OV,OB,ONm
    if sv_class == 1:
        E += 1
        if sv_deck.count("6lZu2") == 3:
            E1 += 1
        elif sv_deck.count("6wgKy") == 3:
            E2 += 1
        else:
            OE += 1
    elif sv_class == 2:
        R += 1
        if sv_deck.count("6td0o") == 3:
            R1 += 1
        elif sv_deck.count("6wgKy") == 3:
            R2 += 1
        else:
            OR += 1
    elif sv_class == 3:
        W += 1
        if sv_deck.count("6q8s2") == 3:
            W1 += 1
        elif sv_deck.count("6t_RI") == 3:
            W2 += 1
        else:
            OW += 1
    elif sv_class == 4:
        D += 1
        if sv_deck.count("6wgKy") == 3:
            D1 += 1
        elif sv_deck.count("6wcBA") == 3:
            D2 += 1
        else:
            OD += 1
    elif sv_class == 5:
        Nc += 1
        Nc1 += 1
    elif sv_class == 6:
        V += 1
        if sv_deck.count("6wgKy") == 3:
            V1 += 1
        elif sv_deck.count("6v3oc") == 3 and sv_deck.count("6yypo") == 3:
            V2 += 1
        else:
            OV += 1
    elif sv_class == 7:
        B += 1
        if sv_deck.count("6wgKy") == 3:
            B1 += 1
        else:
            OB += 1
    elif sv_class == 8:
        Nm += 1
        if sv_deck.count("6zcK2") == 3:
            Nm1 += 1
        elif sv_deck.count("6wgKy") == 3:
            Nm2 += 1
        else:
            ONm += 1
    else:
        print("入力エラー")

TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("logged in as " + client.user.name)


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    elif "sv.j-cg.com" in message.content:

        #クラスカウンターの初期化
        global E,R,W,D,Nc,V,B,Nm
        global E1,E2,R1,R2,W1,W2,D1,D2,Nc1,V1,V2,B1,Nm1,Nm2
        global OE,OR,OW,OD,ONc,OV,OB,ONm
        E = R = W = D = Nc = V = B = Nm = 0
        E1 = E2 = R1 = R2 = W1 = W2 = D1 = D2 = Nc1 = V1 = V2 = B1 = Nm1 = Nm2 = 0
        OE = OR = OW = OD = ONc = OV = OB = ONm = 0

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
                    deck_ij = j_txt["participants"][i]["dk"][j]["hs"]
                    deck_arche_analysis(deck_ij, class_ij)
            else:
                continue

        classes_list = np.array([E, R, W, D, Nc, V, B, Nm])
        classes_label = ["E", "R", "W", "D", "Nc", "V", "B", "Nm"]
        arche_count = np.array([E1,E2,OE,R1,R2,OR,W1,W2,OW,D1,D2,OD,Nc1,ONc,V1,V2,OV,B1,OB,Nm1,Nm2,ONm])
        colors_class = ["palegreen", "peachpuff", "mediumslateblue", "sienna","darkmagenta", "crimson", "wheat", "lightsteelblue"]
        colors_arche = ["palegreen"]*3 +["peachpuff"]*3 +  ["mediumslateblue"] * 3 + ["sienna"] * 3 + ["darkmagenta"] * 2 + ["crimson"] * 3 + ["wheat"] * 2 + ["lightsteelblue"] * 3

        fig1 = plt.figure()
        plt.pie(classes_list, labels=classes_label, colors=colors_class, autopct="%.1f%%",pctdistance=1.35,wedgeprops={'linewidth': 2, 'edgecolor':"white"})
        fig1.savefig("class_pie_"+compe_num+".png")

        fig2 = plt.figure()
        x = np.array(list(range(len(arche_list))))
        plt.bar(x, arche_count, tick_label=arche_list, color=colors_arche)
        plt.ylabel("number of users")
        plt.xticks(rotation=90)
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.95)
        for x, y in zip(x, arche_count):
            plt.text(x, y, y, ha='center', va='bottom')
            
        fig2.savefig("class_bar_"+compe_num+".png")

        analysed_data = [discord.File("class_pie_" + compe_num + ".png"),discord.File("class_bar_" + compe_num + ".png"),]
        await message.channel.send(compe_info)
        await message.channel.send(files=analysed_data)

    elif message.content == 'イマイ':
        await message.channel.send('Hi.')



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
