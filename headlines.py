from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import feedparser
import json
from urllib import parse as url_parse
from urllib import request as url_request


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

NEWS_FEEDS = {
    "MKINI_TERKINI": "https://www.malaysiakini.com/my/news.rss",
    "MKINI_KOLUMNIS": "https://www.malaysiakini.com/my/columns.rss",
    "THESTAR_EDITOR": "https://www.thestar.com.my/rss/editors-choice/main/",
    "THESTAR_NATION": "https://www.thestar.com.my/rss/news/nation/",
    "TMI_ENGLISH": "https://www.themalaysianinsight.com/rss/all/",
    "TMI_BAHASA": "https://www.themalaysianinsight.com/bahasa/rss/all/",
    "FMT": "http://www.freemalaysiatoday.com/feed/"
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a5ebfde13305fd3c4a6ef3d2bef29a47"
DEFAULTS = {"city": "Kuala Selangor", "publication": "MKINI_TERKINI"}

publishers = list(publisher.title() for publisher in  NEWS_FEEDS.keys())


@app.route("/")
def home():
    # Get News Publication
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)

    # Get City for weather data
    city = request.args.get("city")
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)

    return render_template("index.html", articles=articles, weather=weather)


@app.route("/")
def get_news(search_query):
    if not search_query or search_query not in NEWS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = search_query.upper()
    feed = feedparser.parse(NEWS_FEEDS[publication])
        
    return feed['entries']
    
def get_weather(query):
    query = url_parse.quote(query)
    url = WEATHER_URL.format(query)
    data = url_request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None

    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], 
                  "temperature": parsed["main"]["temp"], 
                  "city": parsed["name"],
                  "country": parsed["sys"]["country"]
                  }
    
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)