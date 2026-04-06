
---
**The Code:**

```python
# Billy Bot is basically Alexa. All the responses currently require me to record a clip of my voice. This is because im a narcissist lol and want to talk to myself.
# All the lines that say 'play("smth.wav")' can be replaced with 'say("smth")' if you want to use the text to speech instead. I just prefer the sound of my own voice.

import speech_recognition as sr
import os
import random
import pygame
import requests
import pyttsx3
import datetime
from vosk import Model, KaldiRecognizer
import json
import queue
import threading
import time
from datetime import timedelta
from word2number import w2n
'''import tinytuya''' # I was going to add smart home control but it was a pain to set up cause I have to setup a tuya developer account and I couldnt be bothered. If you want to add it just uncomment this line and figure it out yourself

VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
if os.path.exists(VOSK_MODEL_PATH):
    vosk_model = Model(VOSK_MODEL_PATH)
    vosk_recogniser = KaldiRecognizer(vosk_model, 16000)
    vosk_available = True
    print("Vosk model loaded successfully.")
else:
    vosk_available = False
    print("Vosk model not found.")

q = queue.Queue()
def vosk_callback(indata, frames, timestamp, status):
    q.put(bytes(indata))

current_game = None
current_number = None
start_time = time.monotonic()
GNEWS_KEY = "aee18f6044bb6c15e78b1d8316cbca04"

recogniser = sr.Recognizer()
pygame.mixer.init()
speaker = pyttsx3.init()

def say(text):
    print("Billy: " + text)
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

def keep_alive():
    if current_game is None:
        path = os.path.join("voices", "silence.wav")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
    threading.Timer(180, keep_alive).start()

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

def get_uptime():
    uptime = str(timedelta(seconds=int(time.monotonic() - start_time)))
    play("uptime.wav")
    say(uptime)

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    play("thetimeis.wav")
    say(now)

def get_date():
    date = datetime.datetime.now()
    day = date.strftime("%A")
    month = date.strftime("%B")
    num = date.strftime("%d")
    year = date.strftime("%Y")
    play("todayis.wav")
    say(f"{day}, {month} {num}, {year}")

def get_day():
    day = datetime.datetime.now().strftime("%A")
    play("todayis.wav")
    say(day)

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

def birthday(year):
    if year == 16:
        target = datetime.datetime(2028, 2, 29)
        seconds = int((target - datetime.datetime.now()).total_seconds())
        play("birthday16.wav")
        say(str(seconds))
    elif year == 18:
        target = datetime.datetime(2030, 2, 28)
        seconds = int((target - datetime.datetime.now()).total_seconds())
        play("birthday18.wav")
        say(str(seconds))
    else:
        play("birthdayunknown.wav")

# THIS IS THE MOST BEAUTIFUL THING IVE EVER CREATED I DESERVE A NOBEL PRIZE FOR THIS FUNCTION. IT CAN UNDERSTAND ANY WAY OF SAYING A TIMER. TRY IT OUT, SAY "BILLY SET A TIMER FOR 2 HOURS 15 MINUTES AND 30 SECONDS" OR "BILLY REMIND ME IN 45 MINUTES" OR ANY OTHER VARIATION YOU CAN THINK OF, IT WILL WORK.
def timer(speech):
    words = speech.lower().split()
    total_seconds = 0
    last_number = None
    for word in words:
        try:
            last_number = w2n.word_to_num(word)
        except ValueError:
            if last_number is not None:
                if word in ["second", "seconds", "sec", "secs"]:
                    total_seconds += last_number
                    last_number = None
                elif word in ["minute", "minutes", "min", "mins"]:
                    total_seconds += last_number * 60
                    last_number = None
                elif word in ["hour", "hours", "hr", "hrs"]:
                    total_seconds += last_number * 3600
                    last_number = None
    if total_seconds == 0:
        play("timerror.wav")
        return
    t = threading.Timer(total_seconds, play, args=["buzzer.wav"])
    t.start()
    play("timer.wav")

def calculate(speech):
    speech = speech.replace("times", "*")
    speech = speech.replace("multiplied by", "*")
    speech = speech.replace("divided by", "/")
    speech = speech.replace("plus", "+")
    speech = speech.replace("minus", "-")
    speech = speech.replace("subtract", "-")
    words = speech.split()
    math_str = ""
    for word in words:
        try:
            math_str += str(w2n.word_to_num(word)) + " "
        except:
            if any(op in word for op in ["+", "-", "*", "/"]):
                math_str += word + " "
    try:
        result = eval(math_str.strip())
        play("answer.wav")
        say(str(result))
    except:
        play("matherror.wav")

def truth_dare():
    global current_game
    current_game = "truth_or_dare"
    play("truth_dare.wav")

def handle_truth_dare(speech):
    global current_game
    if "truth" in speech:
        truths = ["truth1.wav", "truth2.wav", "truth3.wav", "truth4.wav", "truth5.wav"]
        play(random.choice(truths))
        current_game = None
    elif "dare" in speech:
        dares = ["dare1.wav", "dare2.wav", "dare3.wav", "dare4.wav", "dare5.wav"]
        play(random.choice(dares))
        current_game = None
    else:
        play("wuss.wav")
        current_game = None

def start_number_guess():
    global current_game, current_number
    current_number = random.randint(1, 100)
    current_game = "number_guess"
    play("number_guess.wav")

def handle_number_guess(speech):
    global current_game, current_number
    try:
        guess = w2n.word_to_num(speech)
        if guess < current_number:
            play("higher.wav")
        elif guess > current_number:
            play("lower.wav")
        else:
            play("correct.wav")
            current_game = None
            current_number = None
    except:
        play("guesserror.wav")

def start_news():
    global current_game
    current_game = "news"
    play("newswhat.wav")

def handle_news(speech):
    global current_game
    try:
        response = requests.get(
            f"https://gnews.io/api/v4/search?q={speech}&token={GNEWS_KEY}&lang=en&max=1",
            timeout=5
        )
        data = response.json()
        article = data['articles'][0]
        play("newsintro.wav")
        say(article['title'])
        play("newsdesc.wav")
        say(article['description'])
        current_game = None
    except:
        play("newserror.wav")
        current_game = None

def respond(speech):
    speech = speech.lower()

    if "billy" not in speech:
        return True

    elif "actually" in speech and "weather" in speech:
        get_weather()

    elif "actually" in speech and "date" in speech:
        get_date()

    elif "actually" in speech and "news" in speech:
        start_news()

    elif "actually" in speech and any(word in speech for word in ["calculate", "times", "divided by", "plus", "minus", "multiplied"]):
        calculate(speech)

    elif any(word in speech for word in ["timer", "set a timer", "countdown", "remind me in", "reminder", "remind her", "thyme or", "thymor", "time oar", "thyme oar"]):
        timer(speech)

    elif any(word in speech for word in ["number", "guess", "guessing game"]):
        start_number_guess()

    elif "sixteenth" in speech:
        birthday(16)

    elif "eighteenth" in speech:
        birthday(18)

    elif any(word in speech for word in ["what time", "the time", "time is it"]):
        get_time()

    elif any(word in speech for word in ["what day", "the day", "day is it", "what's today"]):
        get_day()

    elif "uptime" in speech or "how long have you been" in speech:
        get_uptime()

    elif any(word in speech for word in ["truth or dare", "truth and dare"]):
        truth_dare()

    elif "joke" in speech:
        jokes = ["joke1.wav", "joke2.wav", "joke3.wav", "joke4.wav", "joke5.wav", "joke6.wav", "joke7.wav", "joke8.wav", "joke9.wav", "joke10.wav"]
        play(random.choice(jokes))

    elif any(word in speech for word in ["roast", "flame", "diss", "grill"]):
        roasts = ["roast1.wav", "roast2.wav", "roast3.wav", "roast4.wav", "roast5.wav"]
        play(random.choice(roasts))

    elif any(word in speech for word in ["hype", "pump", "motivate", "inspire", "gas me"]):
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

    elif any(word in speech for word in ["magic eight ball", "eight ball", "8 ball", "magic ate ball", "magic eight", "magic 8", "ate ball"]):
        eightball = ["eightball1.wav", "eightball2.wav", "eightball3.wav", "eightball4.wav", "eightball5.wav", "eightball6.wav", "eightball7.wav", "eightball8.wav", "eightball9.wav", "eightball10.wav"]
        play(random.choice(eightball))

    elif any(word in speech for word in ["flip a coin", "coin flip", "heads or tails"]):
        play(random.choice(["heads.wav", "tails.wav"]))

    elif any(word in speech for word in ["am i cooked", "is it over", "am i done"]):
        play(random.choice(["cooked_yes.wav", "cooked_no.wav"]))

    elif any(word in speech for word in ["should i", "give me a sign", "yes or no", "help me decide"]):
        play(random.choice(["yes.wav", "no.wav"]))

    elif any(word in speech for word in ["i'm sad", "im sad", "i am sad", "feeling sad", "i feel sad", "i'm upset", "im upset"]):
        play(random.choice(["sad1.wav", "sad2.wav", "sad3.wav"]))

    elif any(word in speech for word in ["i'm tired", "im tired", "i am tired", "so tired", "exhausted"]):
        play("tired.wav")

    elif any(word in speech for word in ["i'm hungry", "im hungry", "i am hungry", "starving", "famished"]):
        play(random.choice(["hungry1.wav", "hungry2.wav", "hungry3.wav"]))

    elif any(word in speech for word in ["i'm bored", "im bored", "i am bored", "nothing to do", "entertain me", "so bored"]):
        play(random.choice(["bored1.wav", "bored2.wav", "bored3.wav"]))

    elif any(word in speech for word in ["i love you", "love you", "i luv you"]):
        play("loveyou.wav")

    elif any(word in speech for word in ["i hate you", "hate you", "i don't like you"]):
        play("hateyou.wav")

    elif any(word in speech for word in ["you're stupid", "youre stupid", "you are stupid", "you're dumb", "youre dumb"]):
        play("stupid.wav")

    elif any(word in speech for word in ["you're smart", "youre smart", "you're amazing", "youre amazing", "you're the best", "youre the best"]):
        play("smart.wav")

    elif any(word in speech for word in ["are you real", "are you alive", "are you human", "are you a robot"]):
        play("areyoureal.wav")

    elif any(word in speech for word in ["better than siri", "are you better than siri"]):
        play("bettersiri.wav")

    elif any(word in speech for word in ["better than alexa", "are you better than alexa"]):
        play("betteralexa.wav")

    elif any(word in speech for word in ["what can you do", "what do you do", "your features"]):
        play("whatcanyoudo.wav")

    elif any(word in speech for word in ["what are you doing", "what are you up to", "whatcha doing"]):
        play("whatdoing.wav")

    elif any(word in speech for word in ["i'm back", "im back", "i am back", "i'm home", "im home"]):
        play("imback.wav")

    elif any(word in speech for word in ["i'm leaving", "im leaving", "i am leaving", "goodbye", "see you later", "i'm going"]):
        play("leaving.wav")

    elif any(word in speech for word in ["i miss you", "missed you"]):
        play("missyou.wav")

    elif any(word in speech for word in ["you're funny", "youre funny", "that was funny", "good one"]):
        play("funny.wav")

    elif any(word in speech for word in ["good morning", "morning", "rise and shine", "wake up", "mourn in", "mornin'"]):
        play(random.choice(["morning1.wav", "morning2.wav", "morning3.wav", "morning4.wav", "morning5.wav"]))

    elif any(word in speech for word in ["good night", "night", "going to bed", "going to sleep", "goodnight", "nite", "knight"]):
        play(random.choice(["goodnight1.wav", "goodnight2.wav", "goodnight3.wav", "goodnight4.wav", "goodnight5.wav"]))

    elif any(word in speech for word in ["how are you", "you good", "how you doing", "you alright", "how you been"]):
        play("feeling.wav")

    elif any(word in speech for word in ["who are you", "what's your name", "identify yourself", "why are you in my room"]):
        play("name.wav")

    elif any(word in speech for word in ["thank you", "thanks", "cheers", "good job", "well done"]):
        play("thanks.wav")

    elif any(word in speech for word in ["shut up", "be quiet", "shush", "zip it", "hush", "quiet", "silence", "hell up", "shutup"]):
        play(random.choice(["shutup1.wav", "shutup2.wav", "shutup3.wav", "shutup4.wav", "shutup5.wav"]))

    elif "emergency stop protocol" in speech:
        play("stop.wav")
        return False

    elif any(word in speech for word in ["hello", "hey", "hi", "yo", "sup", "wassup", "wagwan", "wsg", "wsp", "what's up", "whats up", "what's good", "what it do"]):
        play(random.choice(["greeting1.wav", "greeting2.wav", "greeting3.wav"]))

    else:
        play(random.choice(["unknown1.wav", "unknown2.wav", "unknown3.wav"]))

    return True

print("Billy is online. Say 'billy' to wake.")
play("startup.wav")
keep_alive()

running = True
while running:
    with sr.Microphone() as mic:
        print("Listening...")
        recogniser.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recogniser.listen(mic)

    try:
        speech = recogniser.recognize_google(audio, request_timeout=3)
        print("You said: " + speech)
        if current_game == "truth_or_dare":
            handle_truth_dare(speech)
        elif current_game == "number_guess":
            handle_number_guess(speech)
        elif current_game == "news":
            handle_news(speech)
        else:
            running = respond(speech)

    except sr.RequestError:
        print("Google unavailable, trying Vosk...")
        if vosk_available:
            audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            if vosk_recogniser.AcceptWaveform(audio_data):
                result = json.loads(vosk_recogniser.Result())
                speech = result.get("text", "")
                if speech:
                    print("You said (Vosk): " + speech)
                    if current_game == "truth_or_dare":
                        handle_truth_dare(speech)
                    elif current_game == "number_guess":
                        handle_number_guess(speech)
                    elif current_game == "news":
                        handle_news(speech)
                    else:
                        running = respond(speech)
                else:
                    print("Vosk couldn't hear that either")
            else:
                print("Vosk couldn't process audio")
        else:
            print("Vosk not available, no fallback")

    except sr.UnknownValueError:
        print("Couldn't hear that")
```

---



---

# Billy Bot — Voice Assistant

_Basically Alexa but it's me talking to myself because I'm a narcissist. Runs 24/7 on a Raspberry Pi, listens for "billy", and responds in my own pre-recorded voice.

---

**1. What it is**

Billy Bot is a voice assistant that sits on my desk looking radical. It listens through a far field mic 24/7. When it hears the word "billy" it scans what I said for keywords and plays back a pre-recorded clip of my own voice as the response.

No AI, no Alexa, no subscriptions. Just Python doing exactly what I told it. The whole "intelligence" is a big list of if/elif statements I wrote myself. It sounds impressive because it responds in my actual voice, picks keywords out of full natural sentences, and does actually functional stuff like real weather, real date, real countdowns, a timer that understands "2 hours 15 minutes and 30 seconds", news search, maths, and games.
I made it all in python which is great cause in digi tech i was like "ohh whats the point of python blah blah blah" so yeah its kinda ironic but im lwk proud. And i think i cooked!!  It sounds impressive because it responds in my actual voice, picks keywords out of full natural sentences, and does actually functional stuff like real weather, real date, real countdowns, a timer that understands "2 hours 15 minutes and 30 seconds", news search, maths, and games. (made all by me btwwww)

The Pi uses about 5-8 watts so basically nothing.

---

**2. How it works**

1. USB mic picks up sound
2. Sends to Google speech-to-text (free, needs internet)
3. If Google doesn't respond in 3 seconds → switches to Vosk (fully offline, runs on Pi)
4. Either way Python gets back a text string
5. Checks if "billy" is in the sentence, if not, ignores
6. Scans for keywords → plays matching clip
7. For functional commands → plays my voice intro then robot reads actual data
8. Every 3 minutes → plays a silent audio file to keep the Wonderboom (my speaker, i used a bluetuth speaker i had so i could afford the farfield mic. If you replicate this project u can use any speaker you want and if its a usb mic then remove the silent audio code) awake

---

**3. Parts**

<img width="702" height="921" alt="image" src="https://github.com/user-attachments/assets/8a20bc29-e814-49c7-a4a2-1748b52dc810" />

---
**4. Setting up the Pi**

**What "flashing" means:** Putting the operating system onto the SD card. Like installing Windows but automatic and takes 10 minutes.

**Step 1 — Download Raspberry Pi Imager** `https://www.raspberrypi.com/software/`

**Step 2 — Plug in SD card** Need USB microSD adapter (~$5 Officeworks).

**Step 3 — Flash it**

- Choose Device → Raspberry Pi 5
- Choose OS → Raspberry Pi OS (64-bit)
- Choose Storage → SD card
- Edit Settings:
    - Hostname: `billy`
    - Username + password
    - Wi-Fi name and password
    - Enable SSH
- Save → Yes → Yes → wait ~10 mins

**Step 4 — Boot the Pi** SD card in Pi → USB mic in → power in → green light flickers ~30s then settles. No screen needed ever.

**Step 5 — Pair the Wonderboom** Once Pi is booted, SSH in and run:

```
bluetoothctl
power on
agent on
scan on
```

Find the Wonderboom MAC address in the list, then:

```
pair XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
```

Now it auto-connects on every boot.

**Step 6 — Set Bluetooth as default audio output**

```
sudo raspi-config
```

System Options → Audio → pick the Bluetooth device.

**Step 7 — SSH in from laptop**

```
ssh billy@billy.local
```

---

**5. Installing on the Pi**

```
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-pyaudio -y
pip3 install SpeechRecognition pygame requests pyttsx3 vosk sounddevice word2number
```

Test mic: `arecord -l` Test speaker: `speaker-test -t wav -c 2`

---

**6. Vosk model download**

Go to `https://alphacephei.com/vosk/models` → download `vosk-model-small-en-us-0.15.zip` (~40MB) → unzip → put folder in assistant folder. Folder name must match exactly.

---

**7. Silence.wav**

The keep_alive() function needs a silence.wav file to play every 3 minutes to keep the Wonderboom awake. Generate a 1 second silent wav file at `https://www.audiocheck.net/silenceaudiogenerator.php` or just record yourself being quiet for 1 second. Put it in the voices folder.

---

**8. Folder layout**

```
assistant/
├── assistant.py
├── billy_text_test.py
├── vosk-model-small-en-us-0.15/
│   └── (loads of files, don't touch)
└── voices/
    ├── silence.wav
    └── (~163 other clips)
```

On Pi:

```
/home/[username]/billy/
├── assistant.py
├── vosk-model-small-en-us-0.15/
└── voices/
```

Create on Pi:

```
mkdir billy && mkdir billy/voices
```

Copy from USB:

```
cp -r /media/[username]/[USB]/assistant/. ~/billy/
```

---

**9. Auto-start on boot**

```
crontab -e
```

Add at bottom:

```
@reboot sleep 10 && python3 /home/[username]/billy/assistant.py
```

Ctrl+X → Y → Enter.

---

**10. What Billy can do**

**Functional (say "actually"):**

- weather → real Brisbane weather, temp, sky, wind
- date → full date
- news → asks topic, searches gnews, reads headline (PLEASE PLEASE PLEASE GET YOUR OWN API KEY PLEASE DONT USE MY NEWS TOKENS PLEASE)
- calculate → maths out loud ("actually times five by eight")

**Time stuff:**

- "what time is it" → current time
- "what day is it" → just the day
- "how long have you been running" → uptime

**Countdowns:**

- "billy sixteenth" → (this will be different for everyone)
- "billy eighteenth" → (this will be different for everyone)

**Timer:**

- "billy set a timer for 2 hours 15 minutes and 30 seconds" → actually works for any combination (im really proud of this)

**Games:**

- truth or dare → listens for truth/dare response
- number guessing → 1-100 with higher/lower

**Decisions:**

- coin flip, magic 8 ball, yes/no, am I cooked

**Conversational:**

- greetings, goodnight, good morning, how are you, who are you
- i love you, i hate you, you're stupid, you're smart, are you real
- better than Siri/Alexa, what can you do, i'm back, i'm leaving
- i'm sad (supportive), i'm tired, i'm hungry, i miss you, i'm bored

**Personality:**

- jokes (10), roasts (5), hypes (5), affirmations (10), deaffirmations (10)
- fit check (5), bored (3), unknown (3), shutup (5)
- truth (5), dare (5), sad (3), hungry (3)
- morning (5), goodnight (5), greeting (3)

**Emergency:** "billy emergency stop protocol"

---

**11. Dual speech recognition**

```
Good internet → Google (3s timeout) → text → respond()
Bad internet  → Google fails → Vosk (offline) → text → respond()
```

Vosk model folder must be in same directory as assistant.py. If not found, Billy prints "Vosk not available" and uses Google only without crashing.

---

**12. Keep alive system**

The Wonderboom auto-shuts off after a few minutes of no audio. The keep_alive() function runs every 3 minutes and plays silence.wav to trick the speaker into staying on. It checks if a game is running before playing so it doesn't interrupt anything.

---

**13. Recording list**

163 clips total and I'm not giving you my voice so have fun recording these all. Alternatively, I have already set up a function called "say()" so if u cant be bothered, just replace play("whatever".wav) with say("whatever you want it to say") and it will use a tts voice like siri.

---

**14. Difficulty**

3/10 Technical — no wiring, no sensors, plug in USB mic and run a script I already wrote.

---

**15. Upgrade path**

- **Resemblyzer** — voiceprint so only my voice triggers it. Free.
- **Groq free API** — AI fallback for unknown commands. Free.
- **RGB lights** — tinytuya, Smart Life LED control. Need to sort Tuya developer account but I almost threw my keyboard the first time.
- **Dashboard screen** — small HDMI screen showing time/weather/countdown. ~$25-40. (I actually ordered the parts it was like 11 bucks)
- **GitHub** — github.com/Biggy-Billy/billy-bot

---

**17. To-do list (needs Python and is just kind of an extension to the upgrades section)**

- [ ] Wordle → random 5 letter word
- [ ] Sunrise/sunset → already have Open-Meteo, just different parameters
- [ ] News upgrades → remember last topic, ask follow up questions
- [ ] Resemblyzer voiceprint → only responds to my voice
- [ ] Groq AI fallback → unknown commands go to AI instead of unknown.wav
- [ ] RGB light control → tinytuya once Tuya account is sorted

---
