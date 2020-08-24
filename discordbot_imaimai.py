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
import pandas as pd
from matplotlib.font_manager import FontProperties

fontprop = FontProperties(fname="ipaexg.ttf")

#どばすぽのヘッダー部分
dbsp_header = "https://shadowverse-portal.com/deck/"

#どばすぽからデッキを取得
def get_deck(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    names = soup.select(r".el-card-list-info-name-text")
    counts = soup.select(r".el-card-list-info-count")
    deck = {name.text: int(count.text[1:]) for name, count in zip(names, counts)}
    return deck

#クラス、アーキタイプカウンターの初期化
E = R = W = D = Nc = V = B = Nm = 0
E1 = E2 = R1 = R2 = W1 = W2 = W3 = D1 = D2 = Nc1 = Nc2 = V1 = V2 = B1 = B2 = Nm1 = 0
OE = OR = OW = OD = ONc = OV = OB = ONm = 0
#クラス、アーキタイプ、カウントの一覧作成
arche_dict = {"E":{"リノセウスE":E1, "アマツE":E2, "その他E":OE},"R": {"進化R":R1, "連携R":R2, "その他R":OR},"W": {"スペルW":W1, "専門店W":W2, "秘術W":W3, "その他W":OW},"D": {"ディスカードD":D1, "ホエールD":D2, "その他D":OD},"Nc": {"冥府Nc":Nc1, "葬送Nc":Nc2,  "その他Nc":ONc},"V": {"コントロールV":V1, "狂乱V":V2, "その他V":OV},"B": {"エイラB":B1, "コントロールB":B2, "その他B":OB},"Nm": {"AFNm":Nm1, "その他Nm":ONm}}
label = [list(arche_dict[key].keys()) for key in arche_dict]
arche_label = sum(label,[])
arche_list = ", ".join(arche_label)

#クラス、デッキタイプ分析
def deck_arche_analysis(sv_deck, sv_class):
    global E,R,W,D,Nc,V,B,Nm
    global E1,E2,R1,R2,W1,W2,W3,D1,D2,Nc1,Nc2,V1,V2,B1,B2,Nm1
    global OE,OR,OW,OD,ONc,OV,OB,ONm
    if sv_class == 1:
        E += 1
        if sv_deck.count("6lZu2") == 3:
            E1 += 1
            return list(arche_dict["E"].keys())[0]
        elif sv_deck.count("6pQTI") == 3:
            E2 += 1
            return list(arche_dict["E"].keys())[1]
        else:
            OE += 1
            return list(arche_dict["E"].keys())[2]
    elif sv_class == 2:
        R += 1
        if sv_deck.count("6td16") > 1:
            R1 += 1
            return list(arche_dict["R"].keys())[0]
        elif sv_deck.count("6_B9A") == 3:
            R2 += 1
            return list(arche_dict["R"].keys())[1]
        else:
            OR += 1
            return list(arche_dict["R"].keys())[2]
    elif sv_class == 3:
        W += 1
        if sv_deck.count("6_djc") == 3:
            W1 += 1
            return list(arche_dict["W"].keys())[0]
        elif sv_deck.count("6q95g") == 3:
            W2 += 1
            return list(arche_dict["W"].keys())[1]
        elif sv_deck.count("6t_Rc") == 3:
            W3 += 1
            return list(arche_dict["W"].keys())[2]
        else:
            OW += 1
            return list(arche_dict["W"].keys())[3]
    elif sv_class == 4:
        D += 1
        if sv_deck.count("6yB-y") == 3:
            D1 += 1
            return list(arche_dict["D"].keys())[0]
        elif sv_deck.count("6_zhY") == 3:
            D2 += 1
            return list(arche_dict["D"].keys())[1]
        else:
            OD += 1
            return list(arche_dict["D"].keys())[2]
    elif sv_class == 5:
        Nc += 1
        if sv_deck.count("6n7-I") > 1:
            Nc1 += 1
            return list(arche_dict["Nc"].keys())[0]
        elif sv_deck.count("70OYI") == 3:
            Nc2 += 1
            return list(arche_dict["Nc"].keys())[1]
        else:
            ONc += 1
            return list(arche_dict["Nc"].keys())[2]
    elif sv_class == 6:
        V += 1
        if sv_deck.count("6rGOA") == 3:
            V1 += 1
            return list(arche_dict["V"].keys())[0]
        elif sv_deck.count("6v1MC") ==3:
            V2 += 1
            return list(arche_dict["V"].keys())[1]
        else:
            OV += 1
            return list(arche_dict["V"].keys())[2]
    elif sv_class == 7:
        B += 1
        if sv_deck.count("6nupS") == 3:
            B1 += 1
            return list(arche_dict["B"].keys())[0]
        if sv_deck.count("6nsN2") == 3:
            B2 += 1
            return list(arche_dict["B"].keys())[1]
        else:
            OB += 1
            return list(arche_dict["B"].keys())[2]
    elif sv_class == 8:
        Nm += 1
        if sv_deck.count("gZ1SK") == 3:
            Nm1 += 1
            return list(arche_dict["Nm"].keys())[0]
        else:
            ONm += 1
            return list(arche_dict["Nm"].keys())[1]

        
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
        global E1,E2,R1,R2,W1,W2,W3,D1,D2,Nc1,Nc2,V1,V2,B1,B2,Nm1
        global OE,OR,OW,OD,ONc,OV,OB,ONm
        E = R = W = D = Nc = V = B = Nm = 0
        E1 = E2 = R1 = R2 = W1 = W2 = W3 = D1 = D2 = Nc1 = Nc2 = V1 = V2 = B1 = B2 = Nm1 = 0
        OE = OR = OW = OD = ONc = OV = OB = ONm = 0
        arche_summary = {}
        archetype_name = "initialize"

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
        is_final = info[8].text
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
                    archetype = deck_arche_analysis(deck_ij, class_ij)
                    if archetype in message.content:
                        dbsp_url = dbsp_header+deck_ij
                        deck_dict = get_deck(dbsp_url)
                        arche_summary[j_txt["participants"][i]["nm"]] = deck_dict
                        archetype_name = archetype
                    else:
                        continue
            else:
                continue

        #カウンターの更新
        arche_dict = {"E":{"リノセウスE":E1, "アマツE":E2, "その他E":OE},"R": {"進化R":R1, "連携R":R2, "その他R":OR},"W": {"スペルW":W1, "専門店W":W2, "秘術W":W3, "その他W":OW},"D": {"ディスカードD":D1, "ホエールD":D2, "その他D":OD},"Nc": {"冥府Nc":Nc1, "葬送Nc":Nc2,  "その他Nc":ONc},"V": {"コントロールV":V1, "狂乱V":V2, "その他V":OV},"B": {"エイラB":B1, "コントロールB":B2, "その他B":OB},"Nm": {"AFNm":Nm1, "その他Nm":ONm}}
        #クラスのカウント、ラベル
        class_count = np.array([E, R, W, D, Nc, V, B, Nm])
        class_label = ["E", "R", "W", "D", "Nc", "V", "B", "Nm"]

        #アーキタイプのカウント、ラベル
        count = [list(arche_dict[key].values()) for key in arche_dict]
        arche_count = sum(count,[])
        label = [list(arche_dict[key].keys()) for key in arche_dict]
        arche_label = sum(label,[])

        #カラー
        class_colors = ["palegreen", "peachpuff", "mediumslateblue", "sienna","darkmagenta", "crimson", "wheat", "lightsteelblue"]
        arche_colors = ["palegreen"]*len(arche_dict["E"]) +["peachpuff"]*len(arche_dict["R"]) +  ["mediumslateblue"] * len(arche_dict["W"]) + ["sienna"] * len(arche_dict["D"]) + ["darkmagenta"] * len(arche_dict["Nc"]) + ["crimson"] * len(arche_dict["V"]) + ["wheat"] * len(arche_dict["B"]) + ["lightsteelblue"] * len(arche_dict["Nm"])

        if archetype_name in message.content and is_final == "決勝トーナメント":
            df_arche_summary = pd.DataFrame(arche_summary)
            df_arche_summary = df_arche_summary.fillna(0).astype("int")
            fig, ax = plt.subplots()
            ax.axis("off")
            ax.axis("tight")
            tb = ax.table(cellText=df_arche_summary.values,colLabels=df_arche_summary.columns,rowLabels=df_arche_summary.index,colWidths=[0.15]*len(df_arche_summary.columns),loc='center',bbox=[0,0,1,1], cellLoc="center", rowLoc="right")
            tb.auto_set_font_size(False)
            tb.set_fontsize(8)
            for i in range(len(df_arche_summary.columns)):
                tb[0,i].set_text_props(font_properties=fontprop, weight='bold', color="w")
                tb[0,i].set_facecolor('#2b333b')
            for k in range(1,len(df_arche_summary.index)+1):
                tb[k,-1].set_text_props(font_properties=fontprop, weight='bold', color="w")
                tb[k,-1].set_facecolor('#2b333b')
            plt.savefig("list_" + archetype_name + "_" + compe_num + ".png",bbox_inches="tight")

            await message.channel.send(compe_info)
            await message.channel.send(archetype_name)
            await message.channel.send(file=discord.File("list_" + archetype_name + "_" + compe_num + ".png"))

        else:
            fig1 = plt.figure()
            plt.pie(class_count, labels=class_label, colors=class_colors, autopct="%.1f%%",pctdistance=1.35,wedgeprops={'linewidth': 2, 'edgecolor':"white"})
            fig1.savefig("class_pie_"+compe_num+".png")

            if "クラスのみ" in message.content:
                fig2 = plt.figure()
                x = np.array(list(range(len(class_label))))
                plt.bar(x, class_count, color=class_colors)
                plt.ylabel("使用数",font_properties=fontprop)
                plt.xticks(x,class_label,rotation=90,font_properties=fontprop)
                plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
                for x, y in zip(x, class_count):
                    plt.text(x, y, y, ha='center', va='bottom')
            else:
                fig2 = plt.figure()
                x = np.array(list(range(len(arche_label))))
                plt.bar(x, arche_count, color=arche_colors)
                plt.ylabel("使用数",font_properties=fontprop)
                plt.xticks(x,arche_label,rotation=90,font_properties=fontprop)
                plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25, top=0.95)
                for x, y in zip(x, arche_count):
                    plt.text(x, y, y, ha='center', va='bottom')

            fig2.savefig("class_bar_"+compe_num+".png")
            analysed_data = [discord.File("class_pie_" + compe_num + ".png"),discord.File("class_bar_" + compe_num + ".png"),]
            await message.channel.send(compe_info)
            await message.channel.send(files=analysed_data)
            
    elif "おめでとう！！" in message.content:
        await message.channel.send(file=discord.File("omedetou.jpg"))
            
    elif "あそぶ" in message.content:
        await message.channel.send(file=discord.File("asobu.jpg"))
        
    elif "はわチャ" in message.content or "ハワチャ" in message.content:
        await message.channel.send(file=discord.File("はわチャ.jpg"))
        
    elif "幸せ" in message.content:
        await message.channel.send(file=discord.File("おかけん.png"))
        
    elif "ハワイマイ" in message.content:
        await message.channel.send(file=discord.File("hawaimai.jpg"))
        
    elif "ミスティング・ポポ" in message.content:
        await message.channel.send(file=discord.File("mysting_popo.png"))

    elif 'イマイ' in message.content:
        await message.channel.send('Hi.')

    elif message.content == "リスト":
        await message.channel.send(arche_list)

    elif "ミスター・ポポ" in message.content:
        await message.channel.send(file=discord.File("popo.jpg"))

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
