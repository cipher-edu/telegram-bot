#kutubxonani import(chaqirib olish) qilish
import telebot
from pprint import pprint
import nltk
from random import choice
import json
from gtts import gTTS # text dan mp3 qib beradi
from telebot import types

# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1746320763:AAFzEuCnz5FbFoZDiSfwkGf68hw32P7u6Nw", parse_mode=None)
find = ''
gintents = ''
gexamples = ''
ganswers = ''
lang = 'uz'

# from text to mp3

def get_mp3(text):
    tts = gTTS(text,lang=lang)
    tts.save('audios/'+text+'.mp3')

        
# file load from json

def file_open(arg):
    global BOT_CONFIG
    if (arg == 'uz'):
        with open('uz.json','r',encoding='UTF8') as f:            
            BOT_CONFIG = json.load(f)
    else:
        with open('ru.json','r',encoding='UTF8') as f:
            BOT_CONFIG = json.load(f)


# function for file upload and create

def file_save(arg):
    if (arg == 'uz'):
        with open('uz.json','w') as f:
            json.dump(BOT_CONFIG,f)
    else:
        with open('ru.json','w') as f:
            json.dump(BOT_CONFIG,f)


def filter(text):  #filter funksiyasi
    text = text.lower()
    text = [c for c in text if c in 'abdefghijklmnopqrstuvxzйцукенгшщзхъфывапролджэячсмитьбюё -']
    text = "".join(text) # alfabit harflaridan boshqa simvollarni uchiradi
    return text

def get_answer_by_intent(intent): # javob izlash funksiyasi
    global BOT_CONFIG
    answer = BOT_CONFIG["intents"][intent]["answers"]
    return choice(answer)

def add_answers(message):
    chat_id = message.chat.id
    answer_line = message.text
    answers = (answer_line).split(',')
    global BOT_CONFIG
    global gexamples
    global ganswers
    global gintents   
    ganswers = answers
    BOT_CONFIG["intents"][gintents] = { "examples" : [] , "answers" : [] }
    for item in gexamples:
        BOT_CONFIG["intents"][gintents]["examples"].append(item)
    for item in ganswers:
        BOT_CONFIG["intents"][gintents]["answers"].append(item)
    
    file_save('uz')
    text = 'Yangi intent muvofaqiyatli kiritildi sizni tabrikliyman!'
    bot.send_message(message.chat.id,text)

def add_examples(message):
    chat_id = message.chat.id
    examples_line = message.text
    examples = (examples_line).split(',')
    global gexamples
    gexamples = examples
    msg = bot.reply_to(message, 'Endi Javob variantlarini kiriting! masalan : salom assalom hello hi ')
    bot.register_next_step_handler(msg, add_answers)

    
def add_intents(message):
    chat_id = message.chat.id
    intent = str(message.text)
    global gintents
    gintents = intent
    msg = bot.reply_to(message, 'Endi intentni barcha ehtimolini kiriting!')
    bot.register_next_step_handler(msg, add_examples)
    

# biz hozir start comandasi va help comandasini qaytaishlaymiz

@bot.message_handler(commands=['start','help','intents'])
def handle_start_help(message):
    global lang
    file_open(lang)
    if(message.text == '/start'):
        bot.reply_to(message, "Suhbatlashamizmi???")    
    elif(message.text == '/help'):
        print("helpni bosdi")
        bot.reply_to(message, "qonday yordam kerak ")
    elif(message.text == '/intents'):
        text = "Yangi maqsadni nomini kiriting!"
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, add_intents)
    markup = types.ReplyKeyboardMarkup(row_width=2) 
    uz = types.KeyboardButton('uz')
    ru = types.KeyboardButton('ru')
    markup.add(uz, ru) 
    bot.send_message(message.chat.id, "Tilni tanlang", reply_markup=markup) 


    
@bot.message_handler(content_types=['audio','voice'])

def handle_text_audio(message):
    print(message)
    bot.reply_to(message, "Men telegram bot man va fayllar bilan ishlay olmayman!?")    
# ikkinchi dars python da textlar va spiskalar bilan ishlash

@bot.message_handler(content_types=['text'])
def get_intent(message):
    audio_ans = ''
    text = message.text
    text = filter(text)
    global BOT_CONFIG
    global find
    global lang
    if (message.text == 'uz'):
        lang = 'uz'
        file_open('uz')
    else:
        lang = 'ru'
        file_open('ru')
    for intent, value in BOT_CONFIG["intents"].items():
        for example in value["examples"]:
            example = filter(example)
            if (len(example) != 0):
                distance = nltk.edit_distance(text,example)/len(example)           
            if (example == text or distance <= 0.2):
                print(f" Sizni suxbatdoshiz  {intent} {distance}")
                audio_ans = get_answer_by_intent(intent)
                if (len(audio_ans) >= 0):
                    #bot.reply_to(message,  audio_ans)
                    get_mp3(audio_ans)
                    audio = open('audios/'+audio_ans+'.mp3', 'rb')
                    bot.send_audio(message.chat.id, audio)
                    find = 'topdi'
            
    
    if(find != 'topdi'):
        failer = choice(BOT_CONFIG["failer_phrases"])
        get_mp3(failer)
        #bot.reply_to(message,  failer)
        find = 'topdi'
        audio = open('audios/'+failer+'.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)

        
bot.polling()
