import time
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, ConversationHandler
import random
import os

PORT = int(os.environ.get("PORT", int("PORT NUMNER")))
TOKEN = "ENTER YOUR TOKEN HERE"

""" ------ Telegram --------------------------------------------------------------------- ---------------------------"""

bot = telegram.Bot(TOKEN)

""" ------ Initial data set up ------------------------------------------------------------------ -------------------"""
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN = range(7)
def start(update, context):
    update.message.reply_text("🥳🥳 Welcome, please enjoy the game. To see further description, please type /help ")

def help(update, context):
    update.message.reply_text("To call the game menu, press /game"
                              "\nFor any queries, please contract me @so_many_things_to_learn")

def game(update, context):
    update.message.reply_text("Pick one game to play",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Black Jack", callback_data="Black Jack"), InlineKeyboardButton("Coming Soon", callback_data="Coming Soon")],
            ]))
    return ONE

""" ------ Player info.  ------------------------------------------------------------------------ -------------------"""

def ply_info1(update, context):  #  Choose the player name
    global deck, ply_card, ply_pt, player_lst, a, b, c, d, e, f, chat_id, name_lst
    chat_id = update.effective_chat.id
    suit = ["♠", "♥", "♣", "♦"]
    number = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [(s + " " + n) for s in suit for n in number]

    name_lst = ["Game Terminator 💀", "Winning Machine 🤖", "Alien 👽",
                "Shit of gambling 💩", "To the moon 🚀", "To the ground 💥",
                "Gold Hand 🖐", "King of loser 👑", "Frozen wallet 🧊",
                "Charity lover 💵", "Sorry I don't have money 🙇‍♂️"]
    random.shuffle(name_lst)
    a, b, c, d, e, f = name_lst[0:6]
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.send_video(chat_id=chat_id, video=open('Brand name.mp4', 'rb'), supports_streaming=True)
    query.answer("Presented by Knight Gaming, wait for preparing the game")
    bot.send_video(chat_id=chat_id, video=open('opening.mp4', 'rb'), supports_streaming=True)
    query.message.reply_text("Welcome to BlackJack , now pick a name as player name",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton(a, callback_data=a), InlineKeyboardButton(b, callback_data=b)],
                                          [InlineKeyboardButton(c, callback_data=c), InlineKeyboardButton(d, callback_data=d)],
                                          [InlineKeyboardButton(e, callback_data=e), InlineKeyboardButton(f, callback_data=f)],
                                      ]))
    return TWO  # Go to Step TWO

def ply_info2(update, context):
    query = update.callback_query
    query.answer("Got it ")
    global name
    name = query.data
    time.sleep(2)
    query.message.reply_text("Pick player number",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton("3", callback_data=3), InlineKeyboardButton("4", callback_data=4), InlineKeyboardButton("5", callback_data=5)],
                                 [InlineKeyboardButton("6", callback_data=6), InlineKeyboardButton("7", callback_data=7), InlineKeyboardButton("8", callback_data=8)]
                           ]))
    return THREE

def stage_one(update, context):
    global player_lst, ply_pt, ply_card, stand_lst
    stand_lst = []
    ply_pt = {}
    ply_card = {}
    query = update.callback_query
    query.message.reply_text("〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪")
    query.answer("The game now starting...")

        # Forming name_lst
        #############################################
    num = query.data
    player_lst = [("Player" + str(i)) for i in range(int(num)-1)]
    random.shuffle(player_lst)
    player_lst.append(name)
        #############################################
    random.shuffle(deck)
    bot.send_video(chat_id=chat_id, video=open('wash_vis.mp4', 'rb'), supports_streaming=True)
    query.message.reply_text("〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪")
    query.message.reply_text("Dealer is now distributing cards...")
    time.sleep(6)

    for player in player_lst:
        if player == name:
            bot.send_video(chat_id=chat_id, video=open('open.mp4', 'rb'), supports_streaming=True)
        card_draw(player)
        query.message.reply_text(f"{player}: {ply_card[player]}, pts:{ply_pt[player]}")
    time.sleep(3)

    query.message.reply_text(f"Dealer is distributing card now...")
    bot.send_video(chat_id=chat_id, video=open("wash_invis.mp4", "rb"), supports_streaming=True)
    query.message.reply_text("〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪")
    for player in player_lst:
        if player != name:
            query.message.reply_text(f"{player}: {ply_card[player]}, ㊙️  pts:{ply_pt[player]} + ㊙️")
            card_draw(player)
            time.sleep(0.5)

        elif player == name:
            card_draw(player)
            time.sleep(0.5)
            bot.send_video(chat_id=chat_id, video=open('open.mp4', 'rb'), supports_streaming=True)
            query.message.reply_text(f"{player}: {ply_card[player]},        pts:{ply_pt[player]}")
    time.sleep(2)
    hit_stand1(update, context)
    return FOUR

def hit_stand1(update, context):    # First round on hit_stand #  need to press for serveral time if you select stand initailly 
    if len(stand_lst) == len(player_lst):
        judge(update, context)
    else:
        for player in player_lst:
            if player != name:
                if ply_pt[player] < 15:
                    hit(update, player)
                elif ply_pt[player] >= 15:
                    stand(update, player)
            elif player == name:
                if player not in stand_lst:
                    query = update.callback_query
                    bot.send_video(chat_id=chat_id, video=open("command.mp4", "rb"), supports_streaming=True)
                    query.message.reply_text(f"{name}, hit or stand?      Current pts: {ply_pt[player]}",
                                             reply_markup=InlineKeyboardMarkup([
                                                 [InlineKeyboardButton("Hit", callback_data="Hit"),
                                                  InlineKeyboardButton("Stand", callback_data="Stand")],
                                             ]))
        return FOUR

def reply_action(update, context):
    query = update.callback_query
    if query.data == "Hit":
        query.answer("Command received")
        hit(update, name)
        hit_stand1(update, context)

    elif query.data == "Stand":
        query.answer("Command received")
        stand(update, name)
        hit_stand1(update, context)

def hit(update, player):
    query = update.callback_query
    card = deck.pop()
    ply_card[player] += ", " + card
    card_to_pt(player, card)
    query.message.reply_text(f"{player}, hits {card}")

def stand(update, player):
    query = update.callback_query
    if player not in stand_lst:
        stand_lst.append(player)
        query.message.reply_text(f"{player}, stand")

def card_draw(player):
    card = deck.pop()
    if player not in ply_card:
        ply_card[player] = card
    elif player in ply_card:
        ply_card[player] += ", " + card
    card_to_pt(player, card)

def card_to_pt(player, card):
    if player not in ply_pt:
        ply_pt[player] = 0
    card_num = card.split(" ")[-1]
    if card_num.isdigit():
        pt = int(card_num)
    else:
        if card_num == "A":
            pt = 11
        else:
            pt = 10
    ply_pt[player] += pt

def judge(update, context):
    punishment_lst = []
    name_p_list = ["punishment man",  "punishment woman"]
    query = update.callback_query
    query.message.reply_text("〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪〓♪")
    query.message.reply_text("Players, please open your cards!")

    foul_lst = []
    max_lst = []
    for k, v in ply_pt.items():
        if v > 21:
            foul_lst.append(k)
            punishment_lst.append(k)
        else:
            max_lst.append(v)

    max_ = max(max_lst)
    winner_lst = [k for k, v in ply_pt.items() if v == max_]
    if punishment_lst:
        query.message.reply_text(f"Unfortunately, following player(s): {punishment_lst}, bust! Loser is being punishment")
        query.message.reply_text(f" Winner(s) is(are) : {winner_lst} ! Congratulation!!!! ☺☺.")
        if len(punishment_lst) == 1:
            bot.send_video(chat_id=chat_id, video=open('punishment man.mp4', 'rb'), supports_streaming=True)
        elif len(punishment_lst) > 1:
            bot.send_video(chat_id=chat_id, video=open('punishment man.mp4', 'rb'), supports_streaming=True)
            bot.send_video(chat_id=chat_id, video=open('punishment woman.mp4', 'rb'), supports_streaming=True)

    else:
        query.message.reply_text(f" Winner(s) is(are): {winner_lst} ! Congratulation!!!! ☺☺")

    for player in player_lst:
        query.message.reply_text(f"{player}:   {ply_card[player]}     pt: {ply_pt[player]}")
    query.message.reply_text(f"Game finished")


def cancel(update, context):
    ConversationHandler.END()
    quit()

""" ------ dispatchers   ------------------------------------------------------------------------ -------------------"""
updater = Updater(TOKEN)
dp = updater.dispatcher
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("game", game)],
    states={
        ONE: [CallbackQueryHandler(ply_info1, pattern="Black Jack")],
        TWO: [CallbackQueryHandler(ply_info2)],
        THREE: [CallbackQueryHandler(stage_one)],
        FOUR: [CallbackQueryHandler(reply_action)],
            },
    fallbacks=[CommandHandler("cancel", cancel)],
)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(conv_handler)

""" ------ running bot program  ----------------------------------------------------------------- -------------------"""
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url="https://name of your app create.herokuapp.com/" + TOKEN)
updater.idle()
