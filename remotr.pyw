import telebot, os, pyautogui, time

token = '#####'
user_id = [666]
bot = telebot.TeleBot(token)
stages = {}

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Check','Shutdown')
keyboard1.row('Screenshot')
keyboard1.row('Swap screen')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Confirm','Cancel')

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in user_id:
        bot.send_message(message.chat.id,'Authorized!',reply_markup=keyboard1)
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'check' and message.chat.id in user_id:
        bot.send_message(message.chat.id,'Success!')
    elif message.text.lower() == 'screenshot' and message.chat.id in user_id:
        pyautogui.screenshot('screenshot.jpg')
        img = open('screenshot.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    elif message.text.lower() == 'swap screen' and message.chat.id in user_id:
        pyautogui.hotkey('alt','tab')
        bot.send_message(message.chat.id,'Screen swaped!')
    elif message.text.lower() == 'shutdown' and message.chat.id in user_id:
        stages[message.chat.id] = 'asking'
        bot.send_message(message.chat.id,'Confirm shutdown', reply_markup=keyboard2)
    elif stages.get(message.chat.id) == 'asking' and message.chat.id in user_id:
        if message.text.lower() == 'confirm':
            del stages[message.chat.id]
            os.system('shutdown -s')
            bot.send_message(message.chat.id, 'Ok, shutdown!', reply_markup=keyboard1)
        elif message.text.lower() == 'cancel':
            del stages[message.chat.id]
            bot.send_message(message.chat.id, 'Canceled!', reply_markup=keyboard1)
        else:
            del stages[message.chat.id]
            bot.send_message(message.chat.id, 'Wrong command', reply_markup=keyboard1)
while True:
    try:
        bot.polling()
    except:
        time.sleep(10)
        continue