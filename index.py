import os
import telebot
import urllib
import json
from random import choice

bot = telebot.TeleBot(os.environ["R13BOT_TOKEN"])
patentes = ["MD10 \U0001F62D", "PRATA 1 \U0001F62D", "PRATA 2 \U0001F62B", "PRATA 3 \U0001F62B", "PRATA 4 \U0001F62B", \
            "PRATA 5 \U0001F62B", "PRATA ELITE MESTRE \U0001F625", "OURO 1 \U0001F623", "OURO 2 \U0001F623", "OURO 3 \U0001F623", \
            "OURO 4 \U0001F62A", "AK 1 \U0001F62A", "AK 2 \U0001F60C", "AK CRUZADA \U0001F603", "XERIFE \U0001F60F", \
            "AGUIA 1 \U0001F60F", "AGUIA 2 \U0001F609", "SUPREMO \U0001F61C", "GLOBAL \U0001F60E"]
status = {0: "Offline", 1: "Online", 2: "Ocupado", 3: "Ausente", 4: "Soneca", 5: "looking to trade", 6: "looking to play."}
steamIDs = {"RuanMoura": 76561198155425708, "matheustrajano7": 76561198093050321, \
            "pedrocaJipoca": 76561198070681658, "felipecsporto": 76561198076687114}

@bot.message_handler(commands=['start', 'help'])
def send_start_message(message):
    bot.reply_to(message, "Olá eu sou o 'R13BOT'\n"
                          "Envie o comando /people pra saber quais "
                          "pessoas estão no espaço nesse momento.")


@bot.message_handler(commands=['people'])
def send_people(message):
    bot.reply_to(message, get_reply_message())


def get_reply_message():
    n_people, people = get_people()
    message = "Existem " + str(n_people) + " pessoas no espaço neste momento, são elas: \n\n"
    for person in people:
        message += person["name"] + " na espaçonave " + person["craft"] + "\n\n"
    
    return message


def get_people():
    req = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(req)

    obj = json.loads(response.read())

    return obj["number"], obj["people"]


@bot.message_handler(commands=['steamStatus'])
def steam_status(message):
    bot.reply_to(message, str_status(message))


def str_status(message):
    try:
        player = get_steam_player(message)
        personaname = player.get("personaname")
        if bool(player.get("gameextrainfo")):
            gameextrainfo = player.get("gameextrainfo")
            return f"{personaname.title()} esta jogando {gameextrainfo}"
        else:
            personastate = status[player.get("personastate")]
            return f"{personaname.title()} esta {personastate}"
    except AttributeError:
        return player

def get_steam_player(message):
    try:
        STEAM_API_KEY = os.environ["STEAM_API_KEY"]
        steamId = message.text.split(' ')
        if len(steamId) == 1:
            if message.from_user.username in steamIDs:
                steamId.append(steamIDs[message.from_user.username])
            else:
                raise AttributeError("Parametros não passados!")
        req = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamId[1]}"
        response = urllib.request.urlopen(req)

        obj = json.loads(response.read())

        if not obj["response"]["players"]:
            raise TypeError('SteamID invalido!')
        
        player = obj["response"]["players"][0]

        return player

    except AttributeError as err:
        return err
    except TypeError as err:
        return err
    except:
        return "Nao foi possivel concluir a ação \U0001F635"


@bot.message_handler(commands=['patente'])
def sort_ptt(message):
    bot.reply_to(message, str(message.from_user.first_name) + " sua patente é " + choice(patentes))


def search_ruan_baiano(msg):
    try:
        return "ruan" in msg.text.lower() or "baiano" in msg.text.lower()
    except:
        return False


@bot.message_handler(func=search_ruan_baiano)
def echo_mensao(message):
    bot.reply_to(message, "@RuanMoura")


@bot.message_handler(func=lambda m: m.from_user.username == "felipecsporto")
def echo_felipe(message):
    bot.reply_to(message, "Cala a boca talarico")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print(message)


bot.polling()
