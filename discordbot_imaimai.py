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
E1 = E2 = R1 = R2 = W1 = W2 = D1 = D2 = Nc1 = Nc2 = Nc3 = V1 = V2 = B1 = Nm1 = Nm2 = 0
OE = OR = OW = OD = ONc = OV = OB = ONm = 0
#クラス、アーキタイプ、カウントの一覧作成
arche_dict = {"E":{"Control_E":E1, "M-N_E":E2, "Other_E":OE},"R": {"Evolve_R":R1, "M-N_R":R2, "Other_R":OR},"W": {"Natura_W":W1, "Spell_W":W2, "Other_W":OW},"D": {"M-N_D":D1, "Evolve_D":D2, "Other_D":OD},"Nc": {"M-N_Nc":Nc1, "Machina_Nc":Nc2, "Natura_Nc":Nc3,  "Other_Nc":ONc},"V": {"M-N_V":V1, "Midrange_V":V2, "Other_V":OV},"B": {"M-N_B":B1,"Other_B":OB},"Nm": {"AF_Nm":Nm1, "M-N_Nm":Nm2, "Other_Nm":ONm}}
label = [list(arche_dict[key].keys()) for key in arche_dict]
arche_label = sum(label,[])
arche_summary = {}

#クラス、デッキタイプ分析
def deck_arche_analysis(sv_deck, sv_class):
    global E,R,W,D,Nc,V,B,Nm
    global E1,E2,R1,R2,W1,W2,D1,D2,Nc1,Nc2,Nc3,V1,V2,B1,Nm1,Nm2
    global OE,OR,OW,OD,ONc,OV,OB,ONm
    if sv_class == 1:
        E += 1
        if sv_deck.count("6lZu2") == 3:
            E1 += 1
            return list(arche_dict["E"].keys())[0]
        elif sv_deck.count("6wgKy") == 3:
            E2 += 1
            return list(arche_dict["E"].keys())[1]
        else:
            OE += 1
            return list(arche_dict["E"].keys())[2]
    elif sv_class == 2:
        R += 1
        if sv_deck.count("6td0o") == 3:
            R1 += 1
            return list(arche_dict["R"].keys())[0]
        elif sv_deck.count("6wgKy") == 3:
            R2 += 1
            return list(arche_dict["R"].keys())[1]
        else:
            OR += 1
            return list(arche_dict["R"].keys())[2]
    elif sv_class == 3:
        W += 1
        if sv_deck.count("6q8s2") == 3:
            W1 += 1
            return list(arche_dict["W"].keys())[0]
        elif sv_deck.count("6t_RI") == 3:
            W2 += 1
            return list(arche_dict["W"].keys())[1]
        else:
            OW += 1
            return list(arche_dict["W"].keys())[2]
    elif sv_class == 4:
        D += 1
        if sv_deck.count("6wgKy") == 3:
            D1 += 1
            return list(arche_dict["D"].keys())[0]
        elif sv_deck.count("6wcBA") == 3:
            D2 += 1
            return list(arche_dict["D"].keys())[1]
        else:
            OD += 1
            return list(arche_dict["D"].keys())[2]
    elif sv_class == 5:
        Nc += 1
        if sv_deck.count("6wgKy") == 3:
            Nc1 += 1
            return list(arche_dict["Nc"].keys())[0]
        elif sv_deck.count("6jJrc") > 1:
            Nc2 += 1
            return list(arche_dict["Nc"].keys())[1]
        elif sv_deck.count("6qy7I") == 3:
            Nc3 += 1
            return list(arche_dict["Nc"].keys())[2]
        else:
            ONc += 1
            return list(arche_dict["Nc"].keys())[3]
    elif sv_class == 6:
        V += 1
        if sv_deck.count("6wgKy") == 3:
            V1 += 1
            return list(arche_dict["V"].keys())[0]
        elif sv_deck.count("6v8gy") ==3:
            V2 += 1
            return list(arche_dict["V"].keys())[1]
        else:
            OV += 1
            return list(arche_dict["V"].keys())[2]
    elif sv_class == 7:
        B += 1
        if sv_deck.count("6wgKy") == 3:
            B1 += 1
            return list(arche_dict["B"].keys())[0]
        else:
            OB += 1
            return list(arche_dict["B"].keys())[1]
    elif sv_class == 8:
        Nm += 1
        if sv_deck.count("6zcK2") == 3:
            Nm1 += 1
            return list(arche_dict["Nm"].keys())[0]
        elif sv_deck.count("6wgKy") == 3:
            Nm2 += 1
            return list(arche_dict["Nm"].keys())[1]
        else:
            ONm += 1
            return list(arche_dict["Nm"].keys())[2]
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
        global E1,E2,R1,R2,W1,W2,D1,D2,Nc1,Nc2,Nc3,V1,V2,B1,Nm1,Nm2
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
                    if archetype in message:
                        dbsp_url = dbsp_header+deck_ij
                        deck_dict = get_deck(dbsp_url)
                        arche_summary[j_txt["participants"][i]] = deck_dict
                    else:
                        continue
            else:
                continue
                
        #カウンターの更新
        arche_dict = {"E":{"Control_E":E1, "M-N_E":E2, "Other_E":OE},"R": {"Evolve_R":R1, "M-N_R":R2, "Other_R":OR},"W": {"Natura_W":W1, "Spell_W":W2, "Other_W":OW},"D": {"M-N_D":D1, "Evolve_D":D2, "Other_D":OD},"Nc": {"M-N_Nc":Nc1, "Machina_Nc":Nc2, "Natura_Nc":Nc3,  "Other_Nc":ONc},"V": {"M-N_V":V1, "Midrange_V":V2, "Other_V":OV},"B": {"M-N_B":B1,"Other_B":OB},"Nm": {"AF_Nm":Nm1, "M-N_Nm":Nm2, "Other_Nm":ONm}}
        
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

        if archetype in message and is_final == "決勝トーナメント":
            df_arche_summary = pd.DataFrame(arche_summary)
            fig, ax = plt.subplots(figsize=(8,12))
            ax.axis("off")
            ax.axis("tight")
            ax.table(cellText=df_arche_summary.values,colLabels=df_arche_summary.columns,rowLabels=df_arche_summary.index,loc='center',bbox=[0,0,1,1], cellLoc="center")
            plt.savefig("list_" + archetype + "_" + compe_num + ".png")
            
            analysed_data = [discord.File("list_" + archetype + "_" + compe_num + ".png"),]
            await message.channel.send(compe_info)
            await message.channel.send(archetype)
            await message.channel.send(files=analysed_data)
        
        else:
            fig1 = plt.figure()
            plt.pie(class_count, labels=class_label, colors=class_colors, autopct="%.1f%%",pctdistance=1.35,wedgeprops={'linewidth': 2, 'edgecolor':"white"})
            fig1.savefig("class_pie_"+compe_num+".png")
            
            if "クラスのみ" in message.content:
                fig2 = plt.figure()
                x = np.array(list(range(len(class_label))))
                plt.bar(x, class_count, tick_label=class_label, color=class_colors)
                plt.ylabel("number of users")
                plt.xticks(rotation=90)
                plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
                for x, y in zip(x, class_count):
                    plt.text(x, y, y, ha='center', va='bottom')
            else:
                fig2 = plt.figure()
                x = np.array(list(range(len(arche_label))))
                plt.bar(x, arche_count, tick_label=arche_label, color=arche_colors)
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
