import codecs
import json

from sentiment.sentiment_analyer import getSentimentAnalyer
import yaml


def main():
    with open(r'./config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        print(config)
    print("Start")
    s = getSentimentAnalyer(config)
    # print(s.get_sentiment_dicts())
    # s.setSentence('我不覺得非常聰明"')
    # Positive score if article is positive
    # Negative score if article is negative
    # print(s.get_review_sentiment_score())
    with open(config['input'], 'r', encoding="utf-8") as reader:
        jf = json.loads(reader.read())
    articles = jf['articles']
    # print(articles)
    for article in articles:
        content = '{}'.format(article['content'])
        s.setSentence(content)
        article['score'] = str(s.get_review_sentiment_score())
        if float(article['score']) >= 0:
            article['sentiment'] = "positive"
        elif float(article['score']) < 0:
            article['sentiment'] = "negative"

    with codecs.open(config['output'], "w", encoding="utf-8") as fp:
        json.dump(articles, fp, indent=4, ensure_ascii=False)
    print("Done")


if __name__ == '__main__':
    main()
