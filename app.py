import telebot
import random
from config import keys, TOKEN
from extensions import CryptoConverter,APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["voice"])
def answer_to_voice(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Ты что-то сказал?")
@bot.message_handler(commands=['start'])
def answer_to_start(message: telebot.types.Message):
    text = " Приветствую Вас. Я 'умный' бот. Я могу конвертировать валюту.\n \
Если Вы хотите перевести одну валюту в другую,\n \
по актуальному курсу и в любом колличестве, то \n \
Вам необходимо ввести запрос в следующем формате:\n \
<валюта> (которую хотим перевести) <валюта> (в которую\n \
хотим перевести) <колличество> через пробелы.\n \
Подробнее команда /help"
    bot.send_message(message.chat.id, text)
@bot.message_handler(commands=['help'])
def answer_to_start(message: telebot.types.Message):
    text = ' Пока я умею не много, но я учусь.\n \
Могу ответить на вопрос "Как дела? или "Как жизнь?". \n \
/values - выведет список известных мне валют'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Известные мне валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def answer_to_text(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Приветствую тебя ")
        bot.send_message(message.chat.id, f"дорогой {message.chat.first_name} {message.chat.last_name}")
    elif (message.text.lower() == "как дела") or (message.text.lower() == "как дела?") or (message.text.lower() == "как жизнь") or (message.text.lower() == "как жизнь?"):
        t = random.random()
        if t <= 0.4:
            bot.send_message(message.chat.id, "Всё пучком, пандемия только достала.")
            bot.send_message(message.chat.id, f"А у тебя, {message.chat.first_name}, как жизнь?")
        elif (t <= 0.6) and (t > 0.4):
            bot.send_message(message.chat.id, "Всё хорошо.")
        elif (t <= 0.8) and (t > 0.6):
            bot.send_message(message.chat.id, "Отлично. Будет ещё лучше.")
        elif (t <= 1) and (t > 0.8):
            if message.text.lower()[4] == "д":
                bot.send_message(message.chat.id, "Дела идут хорошо.")
            elif message.text.lower()[4] == "ж":
                bot.send_message(message.chat.id, "Жизнь лучше всех.")
    elif (message.text.lower() == "учить тебя будем") or (message.text.lower() == "учить тебя будем?"):
        bot.send_message(message.chat.id, "Конечно будем, хочу всё уметь.")
        bot.send_message(message.chat.id, f"{message.chat.first_name}, научи меня пожалуйста")
    elif (message.text.lower() == "хочешь быть умным") or (message.text.lower() == "хочешь быть умным?"):
        bot.send_message(message.chat.id, "Конечно хочу, у тупых нет ни фантазии, ни денег ")
    elif (message.text.lower() == "на что готов") or (message.text.lower() == "на что готов?"):
        bot.send_message(message.chat.id, "Как пионер, 'мать его', готов на всё")
    else:
        try:
            values = message.text.split(' ')
            if len(values) != 3:
                raise APIException("Слишком много или мало параметров.")
            in_values, out_values, amount = message.text.split(' ')

            text_out = CryptoConverter.conver(in_values, out_values, amount)
        except APIException as e:
            bot.reply_to(message,f"Ошибка пользователя.\n{e}")
        except Exception as e:
            bot.reply_to(message,f"Не удалось обработать команду.\n{e}")
        else:
            text = f'Ваши {amount} {in_values} будут равны {text_out} {out_values}'
            bot.send_message(message.chat.id,text)


bot.polling(none_stop=True)  # Запускаем бота. none_stop=True говорит, что бот должен стараться не прекращать работу при возникновении каких-либо ошибок