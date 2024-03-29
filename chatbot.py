import os
import nest_asyncio
import requests
nest_asyncio.apply()

import pyttsx3
import speech_recognition as sr
import pyautogui
from datetime import datetime
import time
import pywhatkit
from gpt4 import GPT
from send_email import send_email
from bing import Generate_Image
import random
from news import get_top_headlines, get_random_news
from weather import get_weather, get_description
from translate import translate_text
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver. common.by import By
import warnings
from selenium.webdriver.chrome. service import Service
from selenium. common. exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings. simplefilter("ignore")


url = f'https://cdn.botpress.cloud/webchat/v1/index.html?options=%7B%22config%22%3A%7B%22composerPlaceholder%22%3A%22Talk%20to%20Willow%22%2C%22botConversationDescription%22%3A%22Willow%20-%20Virtual%20Assistant%22%2C%22botId%22%3A%22704d11b2-af6b-4cf4-b87d-79df1dd2a255%22%2C%22hostUrl%22%3A%22https%3A%2F%2Fcdn.botpress.cloud%2Fwebchat%2Fv1%22%2C%22messagingUrl%22%3A%22https%3A%2F%2Fmessaging.botpress.cloud%22%2C%22clientId%22%3A%22704d11b2-af6b-4cf4-b87d-79df1dd2a255%22%2C%22webhookId%22%3A%22bb8de174-f7d8-4de4-a6b8-17807b37795f%22%2C%22lazySocket%22%3Atrue%2C%22themeName%22%3A%22prism%22%2C%22botName%22%3A%22Willow%20-%20Virtual%20Assistant%22%2C%22stylesheet%22%3A%22https%3A%2F%2Fwebchat-styler-css.botpress.app%2Fprod%2F273f0563-bca9-4dde-a9e4-347bf38e6be8%2Fv29652%2Fstyle.css%22%2C%22frontendVersion%22%3A%22v1%22%2C%22useSessionStorage%22%3Atrue%2C%22enableConversationDeletion%22%3Atrue%2C%22theme%22%3A%22prism%22%2C%22themeColor%22%3A%22%232563eb%22%2C%22chatId%22%3A%22bp-web-widget%22%2C%22encryptionKey%22%3A%22cSY1Y93aJomBvTulx0zuLAat4YgYVw6p%22%7D%7D'

chrome_driver_path = 'C:\\Users\\db2ha\\Chatbot\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--log-level=3') # Set Chrome Log Level
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get(url)
sleep(3)


TMDB_API_KEY = os.environ.get("fbc96dc2c3c0d97e2ecef1a70be2913a")

with open('dataset.json', 'r') as file:
    dataset = json.load(file)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def handle_query(query):
    for intent in dataset['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in query.lower():
                return random.choice(intent['responses'])
    return random.choice(dataset['intents'][-1]['responses'])

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.pause_threshold = 1
        voice = listener.listen(source)
    try:
        print("Recognizing....")
        query = listener.recognize_google(voice, language='en-us')
        print("You: " + query)
        return query.lower()
    except sr.UnknownValueError:
        talk('Sorry, i couldnot understand can you please repeat')
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {str(e)}")
        return ""
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

def open_application(app_name):
    try:
        print(f"Attempting to open {app_name}")
        pyautogui.hotkey('win', 's')  # Open Start menu search
        time.sleep(1)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        talk(f"Opening {app_name}")
    except Exception as e:
        print(f"Error opening the application: {str(e)}")
        talk(f"Sorry, I couldn't open {app_name}")

def close_application(app_name):
    try:
        print(f"Attempting to close {app_name}")
        pyautogui.hotkey('alt', 'f4')
        talk(f"Closing {app_name}")
    except Exception as e:
        print(f"Error closing the application: {str(e)}")
        talk(f"Sorry, I couldn't close {app_name}")

def send_whatsapp_message(number, message):
    pywhatkit.sendwhatmsg_instantly(f"+91{number}",message)

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key=fbc96dc2c3c0d97e2ecef1a70be2913a").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]
def set_reminder():
    talk("What shall I remind you about?")
    text = take_command()
    talk("In how many minutes? Please enter minutes")
    local_time = float(input())
    local_time = local_time * 60
    time.sleep(local_time)
    talk(f"Hey, here is your reminder about {text}")

def search_on_google(query):
    pywhatkit.search(query)

def recommend_song():
    # Initialize Spotipy client
    client_credentials_manager = SpotifyClientCredentials(client_id='a556f8c5497840d29a62695d9829fafd',
                                                          client_secret='3dce89ab0df34a1ab17849266c546b0a')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(q='year:2023', type='track', limit=10, offset=random.randint(0, 1000))

    if 'tracks' in results and 'items' in results['tracks']:
        items = results['tracks']['items']
        if items:
            random_song = random.choice(items)
            song_name = random_song['name']
            artist_name = random_song['artists'][0]['name']
            return f"I recommend the song {song_name} by {artist_name}"
    return "Sorry, I couldn't find any recommendations at the moment."

def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def click_on_chat_button():
    button = driver.find_element(By.XPATH, '/html/body/div/div/button').click()
    sleep(2)
    while True:
        try:
            loader = driver.find_element(
                By.CLASS_NAME, 'bpw-msg-list-loading')
            is_visible = loader.is_displayed()
            print('Initializing Willow ... ')

            if not is_visible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Willow is Initializing.')
            break
        sleep(1)

def sendQuery(text):
# Find and interact with the textarea element
    textarea = driver.find_element(By. ID, 'input-message')
    textarea.send_keys(text)
    sleep(1)

    send_btn = driver.find_element(By.ID, 'btn-send').click()
    sleep(1)

def isBubbleLoadervisible():
    print('Willow Is Typing ... ')
    while True:
        try:
            bubble_loader = driver.find_element(
                By.CLASS_NAME, 'bpw-typing-group')
            is_visible = bubble_loader.is_displayed()

            if not is_visible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Willow Is Sending Mesage ... ')
            break
        sleep(1)

chatnumber = 3

def retrieveData():
    print('Retrieving Chat ... ')
    global chatnumber
    sleep(1)
    xpath = f'/html/body/div/div/div/div[2]/div[1]/div/div/div[{chatnumber}]/div/div[2]/div/div/div/div/div/p'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    print("\nWillow: " + element.text)
    chatnumber += 2
    return element.text


def handle_commands(query):
    if 'hello' in query or 'hi' in query or 'hey' in query:
        talk('hello')
    elif 'i am fine' in query or 'good' in query or 'fine' in query or 'great' in query or 'i am good' in query or 'i am great' in query:
        talk(handle_query(query))
    elif 'not feeling well' in query or 'not well' in query or 'feeling sick' in query:
        talk(handle_query(query))
    elif 'thankyou' in query or 'okay thankyou' in query:
        talk('Glad to help! What should I do next?')

    elif 'time' in query or "What's the time?" in query or "Tell me the time" in query or "What time is it?" in query:
        current_time = get_time()
        talk(f"The current time is {current_time}")
    elif 'open' in query:
        app_name = query.replace('open', '')
        open_application(app_name)
    elif 'switch tab' in query:
        pyautogui.hotkey('ctrl', 'tab')
    elif 'close tab' in query:
        pyautogui.hotkey('ctrl', 'w')
    elif 'close' in query:
        pyautogui.hotkey('alt', 'f4')
        talk('done!')
    elif 'play' in query:
        song_name = query.replace('play', '')
        talk('sure, playing ' + song_name + ' on youtube')
        pywhatkit.playonyt(song_name)
    elif 'sleep' in query:
        talk('As you say, I am going to sleep now but whenever you need me just say wake up')
        sleep_mode = True
    elif 'write an email' in query or 'compose an email' in query:
        talk('sure, can i get the email of the receiver?')
        receiver = input('Enter email id of the receiver: ')
        talk('what should be the subject of email?')
        subject = take_command()
        talk('what should be the content? just provide some prompt')
        email_prompt = take_command()
        content = GPT('Write an email for ' + email_prompt)
        send_email(receiver, subject, content)
        talk(f'done, email sent successfully to {receiver}')
    elif 'generate an image' in query:
        talk('sure, what kind of image should i generate? give some prompt')
        prompt = take_command()
        Generate_Image(prompt)
        talk('Images generated sucessfully please check in output folder.')
    elif 'news' in query or 'tell news heaadlines' in query or 'news headlines' in query:  
        talk('Sure, from which category would you like to hear news?')
        category = take_command().lower()
        categories = ['general', 'sports', 'entertainment', 'health', 'business']
        if category in categories:
            articles = get_top_headlines(category)
            if articles:
                random_articles = get_random_news(articles)
                for i, article in enumerate(random_articles):
                    talk(article['title'])
                    if i < 2:  
                        talk("Moving on to the next headline.")
        else:
            talk('Sorry, I could not find news for the specified category.')
    elif 'weather' in query or 'todays weather' in query:
        talk('Sure, which city\'s weather do you want to know?')
        city = take_command()
        temperature, description = get_weather(city)
        talk(f"The current weather in {city} is {description} with temperature {temperature}°C")
    elif 'translate' in query:
        talk('What text would you like to translate?')
        text_to_translate = take_command()
        talk('Which language would you like to translate to?')
        target_language = take_command()
        translated_text = translate_text(text_to_translate, target_language)
        talk('Here is the translated text:')
        talk(translated_text)
    elif "Send a WhatsApp message" in query or 'whatsapp message' in query:
        talk('Sure, please enter the number')
        num = input()
        talk('What is the message?')
        msg = take_command()
        send_whatsapp_message(num,msg)
    elif 'tell me a joke' in query or "Give me something funny" in query or "Joke time!" in query:
        talk(f"Hope you like this on")
        joke = get_random_joke()
        talk(joke)
    elif 'give me an advice' in query or "I need some advice" in query or "Can you advise me on something?" in query:
        talk(f"Here's an advice for you")
        advice = get_random_advice()
        talk(advice)
    elif "trending movies" in query or "What are the trending movies?" in query or "List trending movies" in query or "Any popular movies currently?" in query:
            talk(f"Some of the trending movies are: {get_trending_movies()}")
            print(*get_trending_movies(), sep='\n')
    elif "Set a reminder" in query or "Create a reminder for me" in query or 'reminder' in query:
        talk('Sure!')
        set_reminder()
    elif "can you please search" in query:
        # Extract the task to search for from the query
        task = query.replace("can you please search", "").strip()
        talk('Sure, searching on google')
        search_on_google(task)
    elif "recommend a song" in query:
        recommendation = recommend_song()
        talk(recommendation)
    else:
        click_on_chat_button()
        qu = query
        sendQuery(qu)
        res = retrieveData()
        talk(res)

def greet_user():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        talk(f"Good Morning, my name is Willow! How can I assist you? ")
    elif (hour >= 12) and (hour < 16):
        talk(f"Good afternoon, my name is Willow! How can I assist you? ")
    elif (hour >= 16) and (hour < 19):
        talk(f"Good Evening, my name is Willow! How can I assist you? ")
    else:
        talk("Hello, my name is Willow! How can I assist you?")

greet_user()

while True:
    query = take_command().lower()
    handle_commands(query)
