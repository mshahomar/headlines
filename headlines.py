from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import urllib.parse as url_parse
import urllib.request as url_request
import feedparser
import json

from helper import get_app_id


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

OWM_APPID = get_app_id(".openweathermap")
OER_APPID = get_app_id(".openexchangerates")

NEWS_FEEDS = {
    "MKINI_TERKINI": "https://www.malaysiakini.com/my/news.rss",
    "MKINI_KOLUMNIS": "https://www.malaysiakini.com/my/columns.rss",
    "THESTAR_EDITOR": "https://www.thestar.com.my/rss/editors-choice/main/",
    "THESTAR_NATION": "https://www.thestar.com.my/rss/news/nation/",
    "TMI_ENGLISH": "https://www.themalaysianinsight.com/rss/all/",
    "TMI_BAHASA": "https://www.themalaysianinsight.com/bahasa/rss/all/",
    "FMT": "http://www.freemalaysiatoday.com/feed/"
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + OWM_APPID
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=" + OER_APPID

DEFAULTS = {"city": "Kuala Selangor", "publication": "MKINI_TERKINI", "currency_from": "MYR", "currency_to": "IRR"}

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

    # Get Currency data, and verify currency_from and currency_to
    currency_frm = request.args.get("currency_from")
    if not currency_frm:
        currency_frm = DEFAULTS["currency_from"]

    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS["currency_to"]
    rate = get_rates(currency_frm, currency_to)

    return render_template("index.html", articles=articles, weather=weather, 
            rate=rate, currency_from=currency_frm, currency_to=currency_to)


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

def get_rates(frm, to):
    all_currency = url_request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    
    return to_rate / frm_rate


if __name__ == "__main__":
    app.run(port=5000, debug=True)