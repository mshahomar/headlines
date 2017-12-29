from flask import Flask
from flask_moment import Moment
import feedparser


app = Flask(__name__)
moment = Moment(app)

NEWS_FEEDS = {
    "MKINI_TERKINI": "https://www.malaysiakini.com/my/news.rss",
    "MKINI_KOLUMNIS": "https://www.malaysiakini.com/my/columns.rss",
    "THESTAR_EDITOR": "https://www.thestar.com.my/rss/editors-choice/main/",
    "THESTAR_NATION": "https://www.thestar.com.my/rss/news/nation/" 
}


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


def get_news(publication):
    feed = feedparser.parse(NEWS_FEEDS[publication])
    first_article = feed['entries'][0]
    channel_title = feed['channel']
    
    return """
            <html>
                <body>
                    <h1>{0} Headlines</h1>
                    <a href={1} target="_blank"><b>{2}</b></a><br>
                    <i>{3}</id>
                    <p>{4}</p>
                </body>
            </html>
           """.format(channel_title.get("title"), first_article.get("link"), first_article.get("title"), first_article.get("published"), first_article.get("summary"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)