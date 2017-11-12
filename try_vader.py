from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def getsentiment(filename):
    analyzer = SentimentIntensityAnalyzer()
    with open(filename, 'r') as myfile:
        text = myfile.read().replace('\n', '')
    vs = analyzer.polarity_scores(text)
    print vs['pos']
    print vs['neg']
    print vs['neu']
def main():
   getsentiment("/home/deepika/djando-project/speech_recg/mainapp/audio/Obama1/Obama1.txt")
main()
