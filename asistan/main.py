import random
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from playsound import playsound
import json
import requests
from gtts import gTTS
from youtube_search import YoutubeSearch

sayac = 0


def speak(text):
    tts = gTTS(text, lang='tr')
    rand = random.randint(1, 1000)
    file = 'audio-' + str(rand) + '.mp3'
    tts.save(file)

    function_sound(file)
    os.remove(file)


def function_sound(sound):
    playsound(sound)


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Merhaba,Günaydın")
        print("Merhaba,Günaydın")
    elif hour >= 12 and hour < 18:
        speak("Merhaba,Tünaydın")
        print("Merhaba,Tünaydın")
    else:
        speak("Merhaba,İyi Akşamlar")
        print("Merhaba,İyi Akşamlar")


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def takeCommand():
    required = 0
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            required = index
    r = sr.Recognizer()
    with sr.Microphone(device_index=required) as source:
        r.adjust_for_ambient_noise(source)
        print("Bir Şey Söyle!")
        audio = r.listen(source, phrase_time_limit=4)
    try:
        input = r.recognize_google(audio, language='tr-tr')
        print("Söylediğin: " + input)
        return str(input)
    except sr.UnknownValueError:
        return "None"
    except sr.RequestError as e:
        return "None"

def konus():
    statement = takeCommand().lower()
    return statement





speak("Lina Asistan Başlatılıyor...")
wishMe()

if __name__ == '__main__':
    sayac = 0
    sonuc = 1
    while True:

        statement = konus()
        if 'lina' in statement:
            speak("Nasıl,Yardımcı Olabilirim?")
            while True:
                if sayac == 1:
                    speak("Yardımcı Olabileceğim Başka bir şey var mı")
                    statement = konus()
                    if 'evet' == statement:
                        speak("Ne İstiyorsun?")
                        sayac = 1
                    if 'hayır' == statement:
                        speak("Kendine iyi bak,Hoşcakal")
                        sonuc = 0
                        sayac = 0
                if sonuc == 0:
                    break
                statement = konus()
                if "güle güle" in statement or "hoşcakal" in statement:
                    speak('Kendine iyi bak,Hoşcakal')
                    print('Kendine iyi bak,Hoşcakal')
                    sayac = 1
                    break

                if 'wikipedia' in statement:
                    speak('Wikipediada aranıyor')
                    wikipedia.set_lang("tr")
                    statement = statement.replace("wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)
                    speak("Sonuç Bulundu")
                    print(results)
                    speak(results)
                    sayac = 1

                elif 'youtube' in statement:
                    # speak("Hangi şarkıyı açmamı istersiniz?")

                    results = YoutubeSearch(statement, max_results=1).to_dict()
                    print(results)
                    print('https://www.youtube.com.tr' + results[0]['url_suffix'])
                    time.sleep(2)
                    speak("Açılıyor")
                    webbrowser.open('https://www.youtube.com.tr' + results[0]['url_suffix'])
                    results = results[0]['duration']
                    print(results)
                    results = int(results[0]) * 60 + int(results[2:4])
                    print(results)

                    time.sleep(results)
                    os.system("TASKKILL /F /IM opera.exe")

                    sayac = 1


                elif 'open google' in statement:
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("Google Açılıyor")
                    sayac = 1
                    time.sleep(5)
                elif "hava durumu" in statement:
                    api_key = "8ef61edcf1c576d65d836254e11ea420"
                    base_url = "https://api.openweathermap.org/data/2.5/weather?"
                    speak("Hangi Şehirde Yaşıyorsun")
                    city_name = konus()
                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = requests.get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        celsius = float(x['main']['temp'])
                        celsius = (celsius - 273.15)
                        celsius = round(celsius, 1)
                        speak("Sıcaklık" + str(celsius))
                        sayac = 1
                    else:
                        speak(" City Not Found ")
                        sayac = 1
                elif 'saat' in statement or 'saat kaç' in statement:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    sayac = 1
                    speak(f"Saat {strTime}")
                elif 'web' in statement:
                    statement = statement.replace("search", "")
                    webbrowser.open_new_tab(statement)
                    sayac = 1
                    time.sleep(5)


time.sleep(3)
