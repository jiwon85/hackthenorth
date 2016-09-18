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
    }
}

PATTERN = re.compile('[^a-zA-Z0-9\s]+')

SIMILARITY_THRESHOLD = 0.60 # Very arbitrary


def news_article_filter(article):
    # NOTE we can only check none nlp information
    # Test for english
    if article.meta_lang != 'en' and article.meta_lang != '':
        return False

    # Test for data completeness
    if article.text is None or article.title is None or article.text == '':
        return False

    # Test for news up to date (within a week)
    if article.publish_date is not None and \
        (NOW - article.publish_date.replace(tzinfo=None)).days > 21:
        return False

    return True


def process_news_article(news_site, article):
    try:
        article.parse()
    except:
        return None

    if not news_article_filter(article):
        return None

    try:
        article.nlp()
    except:
        return None

    ret = {
        'title': article.title,
        'date': article.publish_date,
        'summary': article.summary,
        'text': article.text,
        'article_url': article.url,
        'image_url': article.top_image,
        'video_url': article.movies[0] if article.movies is not None and len(article.movies) > 0 else None,
        'author': ','.join(article.authors) if article.authors is not None else None,
        'source': news_site,
        'category': categorize_news(news_site, article),
    }

    return ret

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
    paper.generate_articles(limit=200)
    paper.download_articles(threads=4)
    # paper.parse_articles()

    return paper


def fetch_news_site_articles(news_site, url):
    print('Start on ' + news_site + '.')
    ret = []
    paper = build_news_site_paper(news_site, url)

    for i, article in enumerate(paper.articles):
        print('Currently Process ' + news_site + '. Progress ' + str(i) + '/' + str(len(paper.articles)))

        try:
            processed_article = process_news_article(news_site, article)
            if processed_article is not None:
                ret.append(processed_article)
        except Exception as e:
            print(e)
            pass

    return ret

def get_topics(articles):
    def clean_text(text):
        return PATTERN.sub('', text)

    try:
        tfidf = TfidfVectorizer().fit_transform(
            map(lambda a: clean_text(a.get('text', '')), articles))

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
    # Delete all old records (this removes articles as well)
    Topic.objects.all().delete()

    # Insert topics
    for topic in topics:
        topic_category = categorize_topic(articles, topic['articles'])
        t = Topic(
            category_name=topic_category,
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
    print ('Generating all topics...')
    topics = get_topics(articles)
    print ('Dumping data...')
    dump_data(topics, articles)

def run(*args):
    try:
        job()
    except Exception as e:
        print(e)
        import ipdb; ipdb.set_trace()



# For news categorization
CATEGORIES = {
    'politics': set([
        'politics', 'politic', ''
    ]),
    'business': set([
        'business', 'finance', 'money', 'moneybeat',
        'economy'
    ]),
    'sports': set([
        'sport',
        'sports',
        'football'
    ]),
    'entertainment': set([
        'tv',
        'entertainment',
        'style',
        'celebrity',
    ]),
    'science': set([
        'earth',
        'science',
        'future',
        'technology',
        'tech',
        'gadgets'
    ])
}

WORDS_PATTERN = re.compile('[^a-zA-Z\s]+')
def categorize_news(site, article):
    # We know cnn news url contains the category in it
    url_words = (' '.join(PATTERN.sub(' ', article.url).split(' '))).split(' ')
    scores = {key: 0 for key in CATEGORIES.keys()}

    for word in url_words:
        for category, key_words in CATEGORIES.items():
            if word in key_words:
                scores[category] += 1
    category_found = None

    for category, score in scores.items():
        if score > 0:
            if category_found is None or score > scores[category_found]:
                category_found = category

    return category_found if category_found is not None else 'other'


def categorize_topic(articles, indices):
    category = 'other'
    for idx in indices:
        article = articles[idx]
        if article['category'] != category:
            category = article['category']
    return category
