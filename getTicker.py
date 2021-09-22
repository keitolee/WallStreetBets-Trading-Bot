import praw
import wordsToAvoid
import collections

class redditTicker:
    def __init__(self, redUsername, redPassword):
        self.reddit = praw.Reddit(client_id='YgGbcqVeM-2aXA', client_secret='5gu_tAFJ9BCvAl8g70hemXr6nCByag', username=redUsername, password=redPassword,  user_agent='my_user_agent')
        self.subreddit = self.reddit.subreddit('wallstreetbets')
        self.new_wallstreetbets = self.subreddit.top("day")

    def getWSBTicker(self):
        tickerList = []

        for submission in self.new_wallstreetbets:
            if not submission.stickied:

                submission.comments.replace_more(limit=0)

                for comment in submission.comments.list():

                    wordsComments = comment.body.split()
                    cashtagsCommentsDollarSign = list(set(filter(lambda word: word.lower().startswith('$'), wordsComments)))
                    cashtagsCommentsCapital = list(set(filter(lambda word: word.isupper(), wordsComments)))

                    if len(cashtagsCommentsDollarSign) > 0:
                        isTicker = True

                        for item in cashtagsCommentsDollarSign:

                            sep = item.split('$')
                            if sep[1].isalpha() == False:
                                isTicker = False
                            
                        if isTicker == True:

                            for ticker in cashtagsCommentsDollarSign:
                                noDollarSign = ticker.replace("$", "")
                                tickerList.append(noDollarSign)

                    for word in cashtagsCommentsCapital:

                        if word.isalpha() == True and len(word) <= 4 and len(word) >= 3 and word not in wordsToAvoid.avoidWords: 
                            tickerList.append(word)

        occurrences = collections.Counter(tickerList)

        return occurrences.most_common(5)
