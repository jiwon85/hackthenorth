import newspaper

# News sources
NEWS_SOURCES = [
    'https://www.yahoo.com/news/',
    'http://www.cnn.com/',
    'http://www.nytimes.com/',
    'http://www.huffingtonpost.com/the-news/',
    'http://www.foxnews.com/',
    'http://www.nbcnews.com/',
    'http://www.dailymail.co.uk/home/index.html',
    'https://www.washingtonpost.com/',
    'https://www.theguardian.com/international',
    'http://www.wsj.com/',
]

def fetch_news_article(article):
    article.download()
    article.parse()
    article.nlp()

    return {
        'title': article.title,
        '',
        'text': article.summary,
    }

def fetch_news_site_articles(url):
    ret = []
    paper = newspaper.build(url)
    for article in paper.articles:
        ret.append(fetch_news_article)

def group_by_articles():
    pass

def dump_data():
    pass

def job():
    articles = []
    for news_site in NEWS_SOURCES:
        articles += fetch_news_site_articles(url)
    news_items = group_by_artices(articles)
    dump_data(news_items, articles)

def main(argv):
    job()

if __name__ == "__main__":
    main(sys.argv)
