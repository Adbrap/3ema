# ----- initialistion des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import math
#from playsound import playsound


# ----- initialistion des modules -----#

# ----- initialistion des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE


w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialistion des couleurs du modules pystyle -----#

# ----- initialistion des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialistion des temps de recherches -----#

# ----- initialistion de l'API key et ticker -----#
api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
ticker = 'KGHG'
tiker_live = 'KGHG'


# ----- initialistion de l'API key et ticker -----#

# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#

def Finder_IETE(time1, time_name1, start1):
    # global proxies
    # while True:

    with my_lock:

        api_url_livePrice = f'http://api.polygon.io/v2/last/trade/{tiker_live}?apiKey={api_key}'
        data = requests.get(api_url_livePrice).json()
        df_livePrice = pd.DataFrame(data)

        # api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
        api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start1}/{end}?adjusted=true&limit=50000&apiKey={api_key}'

        data = requests.get(api_url_OHLC).json()
        df = pd.DataFrame(data['results'])
        la_place_de_p = 0

        for k in range(0, len(df_livePrice.index)):
            if df_livePrice.index[k] == 'p':
                la_place_de_p = k
        livePrice = df_livePrice['results'][la_place_de_p]
    dernligne = len(df['c']) - 1
    df.drop([dernligne], axis=0, inplace=True)

    # df = df.drop(columns=['o', 'h', 'l', 'v', 'vw', 'n'])
    # df = df.append({'o': NAN, 'h': NAN, 'l': NAN, 'v': NAN, 'vw': NAN, 'n': NAN, 'c': livePrice, 't': NAN}, ignore_index=True)
    df_new_line = pd.DataFrame([[NAN, NAN, NAN, NAN, NAN, NAN, livePrice, NAN]],
                               columns=['o', 'h', 'l', 'v', 'vw', 'n', 'c', 't'])
    df = pd.concat([df, df_new_line], ignore_index=True)
    df_data_date = []
    df_data_price = []
    for list_df in range(len(df)):
        df_data_date.append(df['t'].iloc[list_df])
        df_data_price.append(df['c'].iloc[list_df])
    data_date = pd.DataFrame(df_data_date, columns=['Date'])
    data_price = pd.DataFrame(df_data_price, columns=['Price'])
    df_wise_index = pd.concat([data_date, data_price], axis=1)

    place_liveprice = (len(df) - 1)

    for data in range(len(df_wise_index)):

        try:

            if df_wise_index['Price'].iloc[data] == df_wise_index['Price'].iloc[data + 1]:
                df = df.drop(df_wise_index['Date'].iloc[data + 1])
        except:

            # print('ok')
            aaa = 0

    # ----- creation des local(min/max) -----#
    local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
    local_max1 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min1 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

    local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

    # ----- creation des local(min/max) -----#

    # ----- suppresion des points morts de la courbe -----#
    test_min = []
    test_max = []

    # if local_min[0] > local_max[0]:
    #        local_max = local_max[1:]
    #        print('On a supprimer le premier point')
    #
    q = 0
    p = 0

    len1 = len(local_min)
    len2 = len(local_max)
    while p < len1 - 5 or p < len2 - 5:
        if local_min[p + 1] < local_max[p]:
            test_min.append(local_min[p])
            local_min = np.delete(local_min, p)

            p = p - 1
        if local_max[p + 1] < local_min[p + 1]:
            test_max.append(local_max[p])
            local_max = np.delete(local_max, p)

            p = p - 1
        p = p + 1

        len1 = len(local_min)
        len2 = len(local_max)

    highs = df.iloc[local_max, :]
    lows = df.iloc[local_min, :]
    highs1 = df.iloc[test_max, :]
    lows1 = df.iloc[test_min, :]

    decalage = 0

    # ----- suppresion des points morts de la courbe -----#
    A = float(df['c'].iloc[local_max[-3]])
    B = float(df['c'].iloc[local_min[-3]])
    C = float(df['c'].iloc[local_max[-2]])
    D = float(df['c'].iloc[local_min[-2]])
    E = float(df['c'].iloc[local_max[-1]])
    F = float(df['c'].iloc[local_min[-1]])
    G = float(livePrice)

    if C > E:
        differ = (C - E)
        pas = (local_max[-1] - local_max[-2])
        suite = differ / pas
    if C < E:
        differ = (E - C)
        pas = (local_max[-1] - local_max[-2])
        suite = differ / pas

    Write.Print("  >> RECHERCHE IETE  :", Colors.white, interval=0.000)
    Write.Print("  KGHG", Colors.green, interval=0.000)
    Write.Print(f"  {time1} {time_name1}", Colors.cyan, interval=0.000)
    Write.Print("  <<", Colors.white, interval=0.000)
    print('')

    data_A = []
    data_B = []
    data_C = []
    data_D = []
    data_E = []
    data_F = []
    data_G = []

    rouge = []
    vert = []
    bleu = []

    rouge.append(local_max[-3])
    rouge.append(local_min[-3])
    rouge.append(local_max[-2])
    rouge.append(local_min[-2])
    rouge.append(local_max[-1])
    rouge.append(local_min[-1])
    rouge.append(place_liveprice)

    vert.append(local_max[-3])
    vert.append(local_max[-2])
    vert.append(local_max[-1])
    vert.append(place_liveprice)

    i = 0
    for i in range(local_max[-4] - 1, len(df)):
        bleu.append(i)

    mirande2 = df.iloc[vert, :]
    mirande = df.iloc[rouge, :]
    mirande3 = df.iloc[bleu, :]

    if E > C:
        mirande2['c'].values[0] = mirande2['c'].values[1] - ((suite * (local_max[-2] - local_max[-3])))
        mirande2['c'].values[3] = mirande2['c'].values[2] + ((suite * (place_liveprice - local_max[-1])))
    if E < C:
        mirande2['c'].values[0] = mirande2['c'].values[1] + ((suite * (local_max[-2] - local_max[-3])))
        mirande2['c'].values[3] = mirande2['c'].values[2] - ((suite * (place_liveprice - local_max[-1])))
    if E == C:
        mirande2['c'].values[0] = df['c'].values[local_max[-2]]
        mirande2['c'].values[3] = df['c'].values[local_max[-1]]

    vert1 = {'c': vert}
    vert2 = pd.DataFrame(data=vert1)
    rouge1 = {'c': rouge}
    rouge2 = pd.DataFrame(data=rouge1)
    bleu1 = {'c': bleu}
    bleu2 = pd.DataFrame(data=bleu1)
    # --- premier droite ---#
    AI = [local_max[-3], mirande2['c'].iloc[0]]
    BI = [local_max[-2], mirande2['c'].iloc[1]]

    # --- deuxieme droite ---#
    CI = [local_max[-3], A]
    DI = [local_min[-3], B]
    # I = line_intersection((AI, BI), (CI, DI))

    # ----------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------#

    AJ = [local_max[-1], mirande2['c'].iloc[2]]
    BJ = [place_liveprice, mirande2['c'].iloc[3]]

    # --- deuxieme droite ---#
    CJ = [place_liveprice, G]
    DJ = [local_min[-1], F]
    # J = line_intersection((AJ, BJ), (CJ, DJ))

    # ----- verification qu'il n'y est pas de point mort dans la figure -----#
    pop = 0
    verif = 0

    for pop in range(0, len(test_min)):
        if test_min[pop] > local_max[-3] and test_min[pop] < place_liveprice:
            verif = verif + 1
    pop = 0
    for pop in range(0, len(test_max)):
        if test_max[pop] > local_max[-3] and test_max[pop] < place_liveprice:
            verif = verif + 1
    # ----- verification qu'il n'y est pas de point mort dans la figure -----
    ordre = False
    if local_max[-3] < local_min[-3] < local_max[-2] < local_min[-2] < local_max[-1] < local_min[-1]:
        ordre = True

    mini_pourcent = False
    if ((((C + E) / 2) - D) * 100) / D >= 2.8:
        mini_pourcent = True

    if (C - B) < (C - D) and (C - B) < (E - D) and (E - F) < (E - D) and (E - F) < (
            C - D) and B > D and F > D and B < C and F < E and A >= mirande2['c'].iloc[
        0] and verif == 0 and ordre == True and mini_pourcent == True:
        try:
            J = line_intersection((AJ, BJ), (CJ, DJ))
            I = line_intersection((AI, BI), (CI, DI))
            accept = True
        except:
            accept = False
        if accept == True:
            moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
            moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
            moyenne_des_epaule = ((E - F) + (J[1] - F)) + ((E - F) + (J[1] - F)) / 4
            moyenne_tete = ((C - D) + (E - D)) / 2

            tuche = 0
            noo = 0
            place_pc = 0
            point_max = J[0] + ((J[0] - I[0]))
            point_max = int(round(point_max, 0))
        if I[1] > B and J[
            1] > F and moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule2 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and moyenne_epaule2 >= moyenne_tete / 4 and accept == True and \
                df['c'].values[-2] <= J[1] + (moyenne_tete) / 4 and df['c'].values[-2] >= J[1] and df['c'].values[-1] <= \
                J[1] + (moyenne_tete) / 4 and df['c'].values[-1] >= J[1]:

            note = 0
            pourcentage_10_tete = (10 * (local_max[-1] - local_max[-2]))/100
            pourcentage_10_ep1 = (20 * (local_max[-2] - I[0])) / 100
            pourcentage_10_ep2 = (20 * (J[0] - local_max[-1])) / 100
            pourcentage_20_moy_epaule = (30 * moyenne_des_epaule) / 100

            debugage = []

            if local_min[-2] < (local_max[-2] + local_max[-1])/2 + pourcentage_10_tete and local_min[-2] > (local_max[-2] + local_max[-1])/2 - pourcentage_10_tete : # D doit etre au millieu (10% de marge)
                note = note + 3
                debugage.append(1)

            if local_min[-3] < (I[0] + local_max[-2])/2 + pourcentage_10_ep1 and local_min[-3] > (I[0] + local_max[-2])/2 - pourcentage_10_ep1: # B doit etre au millieu (10% de marge)
                note = note + 1
                debugage.append(2)

            if local_min[-1] < (J[0] + local_max[-1])/2 + pourcentage_10_ep2 and local_min[-1] > (J[0] + local_max[-1])/2 - pourcentage_10_ep2: # F doit etre au millieu (10% de marge)
                note = note + 1
                debugage.append(3)

            if moyenne_epaule1 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule1 > moyenne_des_epaule - pourcentage_20_moy_epaule and moyenne_epaule2 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule2 > moyenne_des_epaule - pourcentage_20_moy_epaule : # les epaules doivent etre de presque meme hauteur
                note = note + 1
                debugage.append(4)

            if B < F :
                if (((F - B) *100) / moyenne_tete) <= 30:
                    note = note + 2
                    debugage.append(5)


            if B > F:
                if (((B - F) *100) / moyenne_tete) <= 30:
                    note = note + 2
                    debugage.append(5)

            if B == F:
                note = note + 2
                debugage.append(5)

            if (local_max[-1] - local_max[-2]) > local_max[-2] - I[0] and (local_max[-1] - local_max[-2]) > J[0] - local_max[-1]: # tete plus large que les 2 epaules
                note = note + 0.5
                debugage.append(6)

            #if il y a pas de bruit:
                #note = note + 1.5
            dejatoucher = False
            if df['h'].iloc[-1] <= J[1] + (moyenne_tete) / 2: # regarde si la target a deja ete toucher en volatilité avant affichage
                dejatoucher = True
            #playsound('note.wav')
            moins3p = G - ((3*G)/100)
            plus_grand = round((J[1] + (moyenne_tete) / 2), 5)
            plus_petit = round(G, 5)
            pourcent_chercher = ((plus_grand - plus_petit) / plus_petit)*100
            pourcent_chercher = round(pourcent_chercher, 2)
            pourcent_perdu = ((round(G, 5)-round(F, 5))*100)/round(G, 5)
            pourcent_perdu = round(pourcent_perdu, 2)
            fig = plt.figure(figsize=(10, 7))
            # fig.patch.set_facecolor('#17abde'
            plt.plot([], [], ' ')
            plt.title(f'IETE : {tiker_live} | {time1} {time_name1} | +{pourcent_chercher}% | -{pourcent_perdu}% | {note}/10 | {debugage} | {dejatoucher}', fontweight="bold", color='black')
            mirande3['c'].plot(color=['blue'], label='Clotures')
            # mirande['c'].plot(color=['#FF0000'])
            mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
            plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
            plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3, color='black', label='75% objectif')
            plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange', label='50% objectif')
            plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
            plt.axhline(y=moins3p, linestyle='--', alpha=0.3, color='purple', label='-3% objectif')
            plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
            taille_diviser = (local_max[-1] - local_max[-2]) / (local_min[-2] - local_max[-2])
            # point_max = J[0]+((J[0] - I[0])/taille_diviser)
            point_max = J[0] + ((J[0] - I[0]))
            point_max = int(round(point_max, 0))
            # plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red',label='Max temps realisation')
            plt.legend()
            plt.text(local_max[-3], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(J[0], J[1] + (moyenne_tete) / 2, f"{round((J[1] + (moyenne_tete) / 2), 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(J[0], moins3p, f"{round(moins3p, 5)}", ha='left',style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-3], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[-2], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-2], D, f"D {round(D, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[-1], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-1], F, f"F  {round(F, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(place_liveprice, G, f"G  {round(G, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
            plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
            # test_valeur = df['c'].iloc[round(J[0]) + 1]
            # plt.text(round(J[0]), df['c'].iloc[round(J[0])], f"J+1 {test_valeur}", ha='left',style='normal', size=10.5, color='#00FF36', wrap=True)
            plt.scatter(len(df['c']) - 1, df['c'].values[-1], color='blue', label='liveprice')
            plt.scatter(len(df['c']) - 2, df['c'].values[-2], color='orange', label='cloture')
            plt.show()
            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
            # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'r')
            # compteur_nombre_image = int(file.read())
            # file.close()
            # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'w')
            # compteur_nombre_image = compteur_nombre_image + 1
            # file.write(f'{compteur_nombre_image}')
            # file.close(
            # plt.savefig(f'images/figure_{compteur_nombre_image}.png'
            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

            multiplicateur = 0
            if time_name1 == 'minute':
                multiplicateur = 60

            if time_name1 == 'hour':
                multiplicateur = 3600

            if time_name1 == 'day':
                multiplicateur = 86400

            temps_attente = time1 * multiplicateur
            time.sleep(temps_attente)
            data_A.append(A)
            data_B.append(B)
            data_C.append(C)
            data_D.append(D)
            data_E.append(E)
            data_F.append(F)
            data_F.append(G)
            data_A_ = pd.DataFrame(data_A, columns=['A'])
            data_B_ = pd.DataFrame(data_B, columns=['B'])
            data_C_ = pd.DataFrame(data_C, columns=['C'])
            data_D_ = pd.DataFrame(data_D, columns=['D'])
            data_E_ = pd.DataFrame(data_E, columns=['E'])
            data_F_ = pd.DataFrame(data_E, columns=['F'])
            data_G_ = pd.DataFrame(data_E, columns=['G'])
            df_IETE = pd.concat([data_A_, data_B_, data_C_, data_D_, data_E_, data_F_, data_G_], axis=1)
    print('----------------------------------------------------------------------', flush=True)
    time.sleep(0.5)


minute = "minute"
heure = "hour"
jour = "day"

th1 = Process(target=Finder_IETE, args=(15,minute,start_15m))
th2 = Process(target=Finder_IETE, args=(20,minute,start_15m))
th3 = Process(target=Finder_IETE, args=(25,minute,start_15m))
th4 = Process(target=Finder_IETE, args=(30,minute,start_30m))
th5 = Process(target=Finder_IETE, args=(35,minute,start_30m))
th6 = Process(target=Finder_IETE, args=(45,minute,start_30m))
th7 = Process(target=Finder_IETE, args=(1,heure,start_1h))
th8 = Process(target=Finder_IETE, args=(2,heure,start_1h))
th9 = Process(target=Finder_IETE, args=(4,heure,start_1h))
th10 = Process(target=Finder_IETE, args=(6,heure,start_6h))
th11 = Process(target=Finder_IETE, args=(10,heure,start_6h))
th12 = Process(target=Finder_IETE, args=(12,heure,start_6h))
th13 = Process(target=Finder_IETE, args=(1,jour,start_1d))
th14 = Process(target=Finder_IETE, args=(2,jour,start_1d))
th15 = Process(target=Finder_IETE, args=(3,jour,start_1d))







th1.start()
th2.start()
th3.start()
th4.start()
th5.start()
th6.start()
th7.start()
th8.start()
th9.start()
th10.start()
th11.start()
th12.start()
th13.start()
th14.start()
th15.start()

th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
th6.join()
th7.join()
th8.join()
th9.join()
th10.join()
th11.join()
th12.join()
th13.join()
th14.join()
th15.join()

















