from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import feedparser


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

publishers = list(publisher.title() for publisher in  NEWS_FEEDS.keys())



@app.route("/")
@app.route("/mkini/terkini")
def mkini_terkini():
    return get_news("MKINI_TERKINI")

@app.route("/mkini/kolumnis")
def mkini_kolumnis():
    return get_news("MKINI_KOLUMNIS")

@app.route("/thestar/editor")
def thestar_editor():
    return get_news("THESTAR_EDITOR")

@app.route("/thestar/nation")
def thestar_nation():
    return get_news("THESTAR_NATION")

@app.route("/tmi/en")
def tmi_english():
    return get_news("TMI_ENGLISH")

@app.route("/tmi/bm")
def tmi_bahasa():
    return get_news("TMI_BAHASA")

@app.route("/fmt")
def fmt():
    return get_news("FMT")


def get_news(publication):
    query = request.args.get("publication")
    print(query)
    if not query or query not in NEWS_FEEDS:
        publication
    else:
        publication = query
    
    feed = feedparser.parse(NEWS_FEEDS[publication])
    articles = feed['entries']
    channel = feed['channel']['title']
    
    return render_template("index.html", articles=articles, channel=channel)
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)