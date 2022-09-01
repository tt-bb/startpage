from flask import Flask, render_template
import requests
import random
from PyDictionary import PyDictionary
from random_word import RandomWords
#import os


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True


@app.route('/')
def index():
    # QUOTE OF THE DAY
    qod_url = f"https://zenquotes.io/api/today"
    qod_response = requests.get(qod_url)
    qod_response = qod_response.json()
    quote = qod_response[0]["q"]
    author = qod_response[0]["a"]

    # NEWS
    category = "technology"
    news_url = f"https://newsapi.org/v2/top-headlines?category={category}&pageSize=10&country=us&apiKey={news_key}"
    news_response = requests.get(news_url)
    news_response = news_response.json()

    # WEATHER
    lat = "50.620762"
    lon = "5.686150"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                  f"lat={lat}&lon={lon}&appid={weather_key}&units=metric"
    weather_response = requests.get(weather_url)
    weather_response = weather_response.json()
    weather = weather_response['weather'][0]['main']
    weather_icon = weather_response['weather'][0]['icon']
    temperature = weather_response['main']['feels_like']

    # WORD OF THE DAY
    dictionary = PyDictionary()
    rw = RandomWords()
    word = rw.get_random_word()
    print(word)
    definitions = dictionary.meaning(word)
    part_of_speech = random.choice(list(definitions.keys()))
    definition = random.choice(definitions[part_of_speech])

    return render_template("index.html", quote=quote, author=author,
                           news=news_response,
                           weather=weather, weather_icon=weather_icon, temperature=temperature,
                           word=word, type_word=part_of_speech, definition=definition
                           )



if __name__ == '__main__':
    app.run()