import datetime
import re
import sys

import newspaper
from sklearn.feature_extraction.text import TfidfVectorizer

from api.models import ArticleInfo, Topic

NOW = datetime.datetime.now()

# News sources
NEWS_SOURCES = {
    'yahoo': {
        'url': 'https://www.yahoo.com/news/',
    },

    'cnn': {
        'url': 'http://www.cnn.com/',
    },
}
'''
'nytimes': {
    'url': 'http://www.nytimes.com/',
},

'huffingtonpost': {
    'url': 'http://www.huffingtonpost.com/the-news/',
},

'foxnews': {
    'url': 'http://www.foxnews.com/',
},

'nbcnews': {
    'url': 'http://www.nbcnews.com/',
},

'dailymail': {
    'url': 'http://www.dailymail.co.uk/home/index.html',
},

'washingtonpost': {
    'url': 'https://www.washingtonpost.com/',
},

'theguardian': {
    'url': 'https://www.theguardian.com/international',
},

'wsj': {
    'url': 'http://www.wsj.com/',
},
'''

PATTERN = re.compile('[^a-zA-Z0-9\s]+')

SIMILARITY_THRESHOLD = 0.60 # Very arbitrary


def news_article_filter(article):
    # NOTE we can only check none nlp information
    # Test for english
    if article.meta_lang != 'en' and article.meta_lang != '':
        return False

    # Test for data completeness
    if article.summary is None or article.title is None:
        return False

    # Test for news up to date (within a week)
    if article.publish_date is not None and \
        (NOW - article.publish_date.replace(tzinfo=None)).days > 21:
        return False

    return True


def process_news_article(news_site, article):
    if not news_article_filter(article):
        return None

    try:
        article.nlp()
    except:
        return None

    return {
        'title': article.title,
        'date': article.publish_date,
        'summary': article.summary,
        'text': article.text,
        'article_url': article.url,
        'image_url': article.top_image,
        'video_url': article.movies[0] if len(article.movies) > 0 else None,
        'author': ','.join(article.authors),
        'source': news_site,
    }

def build_news_site_paper(news_site, url):
    # Build the news paper source
    paper = newspaper.Source(url)
    # Currently no caching, we process the data
    # once for all in memory
    paper.clean_memo_cache()

    paper.download()
    paper.parse()
    paper.set_categories()
    paper.download_categories()
    paper.parse_categories()
    paper.set_feeds()
    paper.download_feeds()
    paper.generate_articles(limit=100)
    paper.download_articles(threads=4)
    paper.parse_articles()

    return paper


def fetch_news_site_articles(news_site, url):
    print('Start on ' + news_site + '.')
    ret = []
    paper = build_news_site_paper(news_site, url)

    for i, article in enumerate(paper.articles):
        print('Currently Process ' + news_site + '. Progress ' + str(i) + '/' + str(len(paper.articles)))

        processed_article = process_news_article(news_site, article)
        if processed_article is not None:
            ret.append(processed_article)

    return ret

def get_topics(articles):
    def clean_text(text):
        return PATTERN.sub('', text)

    try:
        tfidf = TfidfVectorizer().fit_transform(
            map(lambda a: clean_text(a['text']), articles))

        pairwise_similarity = tfidf * tfidf.T
    except:
        import pdb; pdb.set_trace()

    # Now generate topics
    similarity_array = pairwise_similarity.A

    topics = []
    for i, similairty_row in enumerate(similarity_array):
        # Find previous articles and see if they are under the same topic
        for j in range(i):
            if articles[j]['source'] == articles[i]['source']:
                # articles under the same source "should not" be on the same topic
                continue

            if similairty_row[j] > SIMILARITY_THRESHOLD:
                # Once we found the similar article, assign the topic of j to i
                topic = topics[articles[j]['topic']]
                topic['articles'].append(i)
                articles[i]['topic'] = topic['idx']

        if articles[i].get('topic') is None:
            # If we still have no topic yet, create it
            topic = {
                'articles': [i],
                'idx': len(topics)
            }
            topics.append(topic)

            articles[i]['topic'] = topic['idx']

    return topics


def dump_data(topics, articles):
    import pdb; pdb.set_trace()
    # Delete all old records (this removes articles as well)
    Topic.objects.all().delete()

    # Insert topics
    for topic in topics:
        t = Topic(
            hotness_score=len(topic['articles'])
        )
        t.save()

        # Insert articles
        for idx in topic['articles']:
            article = articles[idx]
            a = ArticleInfo(
                summary=article['summary'],
                article_url=article['article_url'],
                video_url=article['video_url'],
                image_url=article['image_url'],
                date=article['date'],
                author=article['author'],
                source=article['source'],
                title=article['title'],
            )
            a.topic = t
            a.save()


def job():
    articles = []
    for news_site, news_info in NEWS_SOURCES.items():
        url = news_info['url']
        news_site_articles = fetch_news_site_articles(news_site, url)
        print (news_site + ' has ' + str(len(news_site_articles)) + ' news')
        articles += news_site_articles

    topics = get_topics(articles)
    dump_data(topics, articles)

def run(*args):
    try:
        job()
    except Exception as e:
        import pdb; pdb.set_trace()
