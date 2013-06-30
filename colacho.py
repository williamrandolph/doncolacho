"""Methods for dealing with the Colacho tweets."""

from time import sleep
import twitter, codecs, pickle

# Processing tweets

def printAsFn(text):
    """In Python 2.6, we need a function for printing, since 'print' is a 
    statement. This prints a string."""
    print(text)

# TODO rewrite to avoid the sleep after last aphorism
def delayProcessAphorism(process, aphorism, delay=5):
    """"Takes a process and an aphorism as a series of tweets and does the
    process to each tweet, with a five second delay."""
    for tweet in aphorism:
        process(tweet)
        sleep(delay)

# Dealing with the twitter API - using python-twitter module

def makeApi(username='williamrandolph'):
    appToken = pickle.load(open('app.pkl', 'rb'))
    consumerToken = pickle.load(open(username + '.pkl', 'rb'))
    return twitter.Api(
        consumerToken['key'],
        consumerToken['secret'],
        appToken['key'],
        appToken['secret'])

# TODO: handle errors from API... figure out what errors I might get.
def tweet(text):
    status = api.PostUpdate(text)

# loading tweets as data structure - really ugly, but it only has to be done
# rarely, so...

# TODO write better file loader / blocks of text? CSV?
def convertFileLineToAphorism(line, tweetedMax=0):
    splitline = line.split('\t')
    aphNumber = int(splitline[0])
    tweeted = (aphNumber < tweetedMax)
    return {'number': aphNumber,
            'tweeted': tweeted,
            'tweets': splitline[1:]}

def loadAphorismsFromFile(aphfilename, tweetedMax=0):
    aphfile = codecs.open(aphfilename, encoding='utf-8')
    aphorisms = {}
    for line in aphfile.readlines():
        aphtemp = convertFileLineToAphorism(line.replace('\n',''), tweetedMax)
        aphorisms[aphtemp['number']] = {'tweeted': aphtemp['tweeted'],
                                        'tweets': aphtemp['tweets']}
    aphfile.close()
    return aphorisms

def dumpDataStructure(aphorisms):
    f = open('aphorisms.pkl', 'wb')
    pickle.dump(aphorisms, f)
    f.close()

def loadAphorisms():
    f = open('aphorisms.pkl', 'rb')
    aphorisms = pickle.load(f)
    f.close()
    return aphorisms

# when last aphorism has been tweeted, I should do something smarter...
def firstUntweetedNum(aphorisms):
    for aphorism in aphorisms:
        if(not(aphorisms[aphorism]['tweeted'])):
            return aphorism
    return -1

# TODO move script into separate file

aphorisms = loadAphorismsFromFile("aphorisms3.csv", 254)
# aphorisms = loadAphorisms()
x = firstUntweetedNum(aphorisms)
# delayProcessAphorism(tweet, aphorisms[x]['tweets'])
delayProcessAphorism(printAsFn, aphorisms[x]['tweets'])
aphorisms[x]['tweeted'] = True
print("Tweeted: %d" % x)
dumpDataStructure(aphorisms)
