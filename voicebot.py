import speech_recognition as sr
import pyttsx3 as p3
import pyautogui as pgui
import time
import threading
from fuzzywuzzy import fuzz
import datetime

opts = {
    "alias": ('ари', 'аристотель','ария','аре','ар','кари'), # Варианты обращения к боту
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси','переключи'), # Лишние частые слова
    "cmds": {
        "time": ('сейчас времени','который час','текущее время','времени','время'),
        "hi": ('привет','здравствуй','добрый день','здарова','hi','hello'),
        "stop": ('спать','спи','засни','выключись','выключение','сон','пока','досвидания','до встречи','пока пока'),
        "slideup": ('вперёд','переключи вперёд','следующий','следующий слайд','дальше',),
        "slidedown": ('назад','переключи назад','прошлый','предыдущий','прошлый слайд','предыдущий слайд'),
        "greeting": ('представься','кто ты')
    } # Варианты команд
}

#Объявление переменных
lock = threading.Lock()
r = sr.Recognizer()
m = sr.Microphone()
running = True

# Функция синтеза голоса
def speak(what):
    print(what)
    v = p3.init()
    v.say(what)
    v.runAndWait()

# 
def callback(r, audio):
    try:
        text = r.recognize_google(audio, language="ru-RU").lower() 
        print("[log] Вы сказали: " + text)

        if not text.startswith(opts["alias"]):
                print("[log] Это не команда")
                return
                
        cmd = text


        for i in opts['alias']:
            cmd = cmd.replace(i, "").strip()

        for i in opts['tbr']:
            cmd = cmd.replace(i, "").strip()

                

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
            print('[log] Речь не распознана')
    except sr.RequestError as e:
            print('[log] Неизвестная ошибка')

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
        for i in v:
            vrt = fuzz.ratio(cmd, i)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):

    global running

    if cmd == 'time':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'hi':
        speak("Добрый день")
    
    elif cmd == 'stop':
        speak("Досвидания")
        stop_listening(wait_for_stop=False)
        running = False

    elif cmd == 'slideup':
        pgui.press('right')

    elif cmd == 'slidedown':
        pgui.press('left')
    
    elif cmd == 'greeting':
         speak("Я голосовой помощник аари")


    else:
        print("[log]Команда не распознана")
        speak("Я не знаю такой команды")


with m as source:
    r.adjust_for_ambient_noise(source)

speak("Добрый день")
speak("Я вас слушаю")

stop_listening = r.listen_in_background(m, callback)
while running: time.sleep(0.1)