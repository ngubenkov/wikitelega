import json
import requests
import time
import urllib
from dbhelper import DBHelper
from wikipedia import return_article

db = DBHelper()

TOKEN = "773633629:AAHAy4gQHwEmZmR4oKiiHzvKFQCAYNhk_gg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url): # connect to bot
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# def handle_updates(updates):
#     for update in updates["result"]:
#         text = update["message"]["text"]
#         chat = update["message"]["chat"]["id"]
#         items = db.get_items(chat)
#         if text == "/done":
#             keyboard = build_keyboard(items)
#             send_message("Select an item to delete", chat, keyboard)
#         elif text == "/start":
#             send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", chat)
#         elif text.startswith("/"):
#             continue
#         elif text in items:
#             db.delete_item(text, chat)
#             items = db.get_items(chat)
#             keyboard = build_keyboard(items)
#             send_message("Select an item to delete", chat, keyboard)
#         else:
#             db.add_item(text, chat)
#             items = db.get_items(chat)
#             message = "\n".join(items)
#             send_message(message, chat)

def handle_message(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
       # print(return_article(update["message"]["text"]))
        print(update["message"]["text"])
        message, sections = return_article(update["message"]["text"])

        if(message == "Stop"): # some unexpected shit handler
            print("HERE")
            send_message("Shit happened", chat)
            break

        elif(message == "Language barier"):
            send_message("Please use only english characters.(Will be update soon)", chat)
            print("Language barier")
            break
        elif(message == "/start"):
            send_message("Welcome to wiki chatbot. Here you can search for articles from Wikipedia,"
                               " just send a request of what are you looking for", chat)
            print("Welcome message")

        #joke for pasha
        elif (message == "Pasha"):
            print("Pasha's case")
            send_message("возможно вы имели ввиду Строчков павел из города Златоуст любит когда его долбят в анус", chat)
            print("Pasha handled")
        else:
            print("everything is fine")
            print("sections : {}".format(sections))
            print("message length : {}".format(len(message[:message.index(sections[0])])  )   )
            listOfendLines = find(message, '\n')
            message = message[:message.index(sections[0])] # get only first part of page before first section


            if listOfendLines[len(listOfendLines) - 1] > 4096: # if article text is greate than 4096 split on two messages
                for i in range(len(listOfendLines) - 1, 0, -1):
                    if listOfendLines[i] < 4096:
                        send_message(message[0:listOfendLines[i]], chat)
                        send_message(message[listOfendLines[i]:], chat)
                        break
            else:
                send_message(message[:message.index(sections[0])], chat)
            remove_keyboard(updates)

def find(s, ch): # find all char in string
    return [i for i, ltr in enumerate(s) if ltr == ch]

def remove_keyboard(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        send_message("", chat, build_keyboard("") )

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    #db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_message(updates)
            #handle_updates(updates)
        time.sleep(0.5)



if __name__ == '__main__':
    main()