# Billy Bot is basicallly alexa. All the responsences currently require me to record a clip of my voice. This is because im a narcisist lol and want to talk to myself. 
# All the lines that say 'play("smth.wav")' can be replaced with 'say("smth")' if you want to use the text to speech instead. I just prefer the sound of my own voice.

import speech_recognition as sr
import os
import random
import pygame
import requests
import pyttsx3
import datetime

recogniser = sr.Recognizer()
pygame.mixer.init()

speaker = pyttsx3.init()

def say(text):
    print("Cypher: " + text)
    speaker.say(text)
    speaker.runAndWait()

def play(filename):
    path = os.path.join("voices", filename)
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
    else:
        print("Missing clip: " + filename)

weather_descriptions = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "showers",
    81: "showers",
    82: "heavy showers",
    95: "thunderstorm"
}

def get_weather():
    try:
        weather_raw = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-27.4705&longitude=153.0260&current_weather=true", timeout=5)
        weather_data = weather_raw.json()
    
        sky = weather_descriptions.get(weather_data['current_weather']['weathercode'])
        temp = weather_data['current_weather']['temperature']
        wind = weather_data['current_weather']['windspeed']
        play("temperature.wav")
        say(str(temp))
        if weather_data['current_weather']['weathercode'] in weather_descriptions:
            play("sky.wav")
            say(sky)
        else:
            play("skyunknown.wav")
        play("wind.wav")
        say(str(wind))

    except:
        play("weathererror.wav")

def get_date():
    date = datetime.datetime.now()
    day = date.strftime("%A")
    month = date.strftime("%B")
    num = date.strftime("%d")
    year = date.strftime("%Y")
    
    play("todayis.wav")
    say(f"{day}, {month} {num}, {year}")

def birthday(year):
    if year == 16:
        birthday16 = datetime.datetime(2028, 2, 29)
        difference16 = birthday16 - datetime.datetime.now()
        total_seconds16 = int(difference16.total_seconds())
        play("birthday16.wav")
        say(str(total_seconds16))
        
    elif year == 18:
        birthday18 = datetime.datetime(2030, 2, 28)
        difference18 = birthday18 - datetime.datetime.now()
        total_seconds18 = int(difference18.total_seconds())
        play("birthday18.wav")
        say(str(total_seconds18))
    else:
        play("birthdayunknown.wav")    
def respond(speech):
    speech = speech.lower()

    if "billy" not in speech:
        return True

    if "actually" in speech and "weather" in speech:
        get_weather()

    elif "actually" in speech and "date" in speech:
        get_date()

    elif "sixteenth" in speech:
        birthday(16)

    elif "eighteenth" in speech:
        birthday(18)

    elif "joke" in speech:
        jokes = ["joke1.wav", "joke2.wav", "joke3.wav", "joke4.wav", "joke5.wav", "joke6.wav", "joke7.wav", "joke8.wav", "joke9.wav", "joke10.wav"]
        play(random.choice(jokes))

    elif any(word in speech for word in ["roast", "flame", "insult", "bully", "mean", "bring me down", "diss", "grill"]):
        roasts = ["roast1.wav", "roast2.wav", "roast3.wav", "roast4.wav", "roast5.wav"]
        play(random.choice(roasts))

    elif any(word in speech for word in ["hyped", "hype", "pump", "motivate", "encourage", "motivation", "inspire"]):
        hypes = ["hype1.wav", "hype2.wav", "hype3.wav", "hype4.wav", "hype5.wav"]
        play(random.choice(hypes))

    elif any(word in speech for word in ["affirm me", "affirmation", "encourage me"]):
        affirmations = ["affirm1.wav", "affirm2.wav", "affirm3.wav", "affirm4.wav", "affirm5.wav", "affirm6.wav", "affirm7.wav", "affirm8.wav", "affirm9.wav", "affirm10.wav"]
        play(random.choice(affirmations))

    elif any(word in speech for word in ["insult me", "bully me", "be mean", "bring me down"]):
        deaffirmations = ["deaffirm1.wav", "deaffirm2.wav", "deaffirm3.wav", "deaffirm4.wav", "deaffirm5.wav", "deaffirm6.wav", "deaffirm7.wav", "deaffirm8.wav", "deaffirm9.wav", "deaffirm10.wav"]
        play(random.choice(deaffirmations))

    elif any(word in speech for word in ["how do i look", "fit check", "rate my fit", "rate the fit", "drip check", "outfit check", "am i dripped out"]):
        fitcheck = ["fitcheck1.wav", "fitcheck2.wav", "fitcheck3.wav", "fitcheck4.wav", "fitcheck5.wav"]
        play(random.choice(fitcheck))

    elif any(word in speech for word in ["magic eight ball", "eight ball", "8 ball", "magic ate ball", "magic ate", "magic eight", "magic 8", "eight ball", "8 ball", "ate ball"]):
        eightball = ["eightball1.wav", "eightball2.wav", "eightball3.wav", "eightball4.wav", "eightball5.wav", "eightball6.wav", "eightball7.wav", "eightball8.wav", "eightball9.wav", "eightball10.wav"]
        play(random.choice(eightball))

    elif any(word in speech for word in ["flip a coin", "coin flip", "heads or tails"]):
        play(random.choice(["heads.wav", "tails.wav"]))

    elif any(word in speech for word in ["am i cooked", "is it over", "am i done"]):
        play(random.choice(["cooked_yes.wav", "cooked_no.wav"]))

    elif any(word in speech for word in ["should i", "give me a sign", "yes or no", "I can't decide", "help me decide", "know", "yes"]):
        play(random.choice(["yes.wav", "no.wav"]))

    elif any(word in speech for word in ["good morning", "morning", "rise and shine", "wake up", "mourn in", "mornin'"]):
        play(random.choice(["morning1.wav", "morning2.wav", "morning3.wav", "morning4.wav", "morning5.wav"]))

    elif any(word in speech for word in ["night", "going to bed", "bed", "sleep", "knight", "nite", "goodnight"]):
        play(random.choice(["goodnight1.wav", "goodnight2.wav", "goodnight3.wav", "goodnight4.wav", "goodnight5.wav"]))

    elif any(word in speech for word in ["boredem", "bored", "entertain me", "nothing to do", "board"]):
        bored = ["bored1.wav", "bored2.wav", "bored3.wav"]
        play(random.choice(bored))

    elif any(word in speech for word in ["how are you", "you good", "how you doing", "you alright"]):
        play("feeling.wav")

    elif any(word in speech for word in ["who are you", "what's your name", "identify yourself", "why are you in my room"]):
        play("name.wav")

    elif any(word in speech for word in ["thank you", "thanks", "cheers", "good job"]):
        play("thanks.wav")

    elif any(word in speech for word in ["shut up", "be quiet", "shush", "zip it", "hush", "quiet", "silence", "hell up", "shutup"]):
        play(random.choice(["shutup.wav", "shutup2.wav", "shutup3.wav", "shutup4.wav", "shutup5.wav"]))

    elif "emergency stop protocol" in speech:
        play("stop.wav")
        return False

    elif any(word in speech for word in ["hello", "hey", "hi", "yo", "sup", "wassup", "wagwan", "wsg", "wsp", "what's up", "whats up", "what's good", "what it do"]):
        play(random.choice(["greeting.wav", "greeting2.wav", "greeting3.wav"]))

    else:
        unknowns = ["unknown1.wav", "unknown2.wav", "unknown3.wav"]
        play(random.choice(unknowns))

    return True

print("Billy is online. Say 'billy' to wake.") # basically "hey alexa"
play("startup.wav")

running = True
while running:
    with sr.Microphone() as mic:
        print("Listening...")
        recogniser.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recogniser.listen(mic)

    try:
        speech = recogniser.recognize_google(audio)
        print("You said: " + speech)
        running = respond(speech)

    except sr.UnknownValueError:
        print("Couldn't hear that")
    except sr.RequestError:
        print("Speech recognition down")
