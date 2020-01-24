from sentiment.sentiment_analyer import getSentimentAnalyer
import yaml
def main():
    with open(r'./config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        print(config)
    print("Start")
    s = getSentimentAnalyer(config)
    print(s.get_sentiment_dicts())
    s.setSentence('我不覺得非常聰明"')
    # Positive score if article is positive
    # Negative score if article is negative
    print(s.get_review_sentiment_score())
    print("Done")


if __name__ == '__main__':
    main()
